#! /usr/bin/env python3

import base64
import datetime
import os

from fastapi import FastAPI, status, Depends, Request, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import requests
import jwt

from sqlalchemy.orm import Session
import starlette.requests
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect

import models
import schemas
import utils
from database import SessionLocal, engine
from authlib.jose import jwk

models.Model.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items.",
    },
]

app = FastAPI(
    title="Mgmt API", docs_url="/docs",
    description="Our own little API to speed things up!",
    openapi_tags=tags_metadata
)

pub_key = "\n".join([l.lstrip() for l in open('key.pub', 'r').read().split("\n")])
priv_key = "\n".join([l.lstrip() for l in open('key.priv', 'r').read().split("\n")])
__INTERNAL_TOKEN__ = 'c6ajUzKXJSdMBErkARNxBySPXVUFlaTfKAA6UCJjF3m97fP61IB36ZphsNWZ9t4'


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Unauthorized, Bearer header needed")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Unauthorized")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        try:
            payload = jwt.decode(jwt_token, pub_key, algorithms=["RS256"])
        except Exception as e:
            print(e)
            raise HTTPException(status_code=403, detail="Unauthorized")
        header = jwt.get_unverified_header(jwt_token)
        jwk_header = header.get('jwk', None)
        if jwk_header is not None and jwk != '/jwk.json':
            dummy_parse_jwk(jwk_header)

        if payload:
            return True

        return False

    @classmethod
    def decode_jwt(cls, jwt_token: str) -> dict:
        try:
            payload = jwt.decode(jwt_token, pub_key, algorithms=["RS256"])
        except Exception as e:
            print(e)
            raise HTTPException(status_code=403, detail="Unauthorized")

        return payload

    @staticmethod
    def is_admin(jwt_token: str) -> bool:
        payload = JWTBearer.decode_jwt(jwt_token)
        if not payload.get("is_admin", False):
            return False

        return True


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_jwt(username, is_admin):
    payload = {
        "username": username,
        "is_admin": is_admin,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=600),
        "data": base64.b64encode(os.urandom(64)).decode('utf-8')  # happy hunting ;)
    }

    headers = {
        "jwk": "/jwk.json"
    }

    return jwt.encode(payload, priv_key, headers=headers, algorithm="RS256")


@app.get("/jwk.json")
def get_jwk():
    return jwk.dumps(pub_key, kty='RSA')


@app.get("/")
def root():
    """
    Nothing interesting here...
    """
    return JSONResponse({"API": {"version": "0.1.0a"}})


@app.get("/heartbeat", response_model=schemas.PingResponseModel)
def heartbeat():
    """
    Returns heartbeat status
    """
    return JSONResponse({"Heartbeat": {"Timestamp": datetime.datetime.now(), "Ping": "Pong"}})


@app.post("/register", response_model=schemas.RegisterResponseModel, status_code=status.HTTP_201_CREATED,
          tags=['users'])
def register_user(request_data: schemas.RegisterRequest, db: Session = Depends(get_db)):
    """
    User registration

    - **username**: required, username
    - **email**: required, valid email
    - **password**: required, password
    """
    username = request_data.username.strip()
    email = request_data.email.strip()
    password = request_data.password

    records = db.query(models.User).filter(models.User.username == username).all()
    if records:
        raise HTTPException(status_code=418, detail={"error": "User exists"})

    records = db.query(models.User).filter(models.User.email == email).all()
    if records:
        raise HTTPException(status_code=418, detail={"error": "Email already in database"})

    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password has to be 8 chars at least")

    tmp_user = models.User(
        username=username, email=email, password=utils.make_password(password)
    )
    db.add(tmp_user)

    try:
        db.commit()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail={"error": "Something went terribly wrong :("})

    return JSONResponse({"Status": "ok", "info": "user created"})


@app.post("/login", response_model=schemas.JWTResponseModel, status_code=status.HTTP_200_OK, tags=['users'])
def login_user(request_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    User login, returns JWT

    - **username**: required, username
    - **password**: required, password
    """

    username = request_data.username
    tmp_pass = request_data.password

    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail={"Error": "Unauthorized"})

    if not utils.check_password(tmp_pass, user.password):
        raise HTTPException(status_code=401, detail={"Error": "Unauthorized"})

    jwt_token = create_jwt(user.username, user.is_admin)
    headers = {"Token": jwt_token}

    return JSONResponse(headers)


@app.put("/change_password", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK, tags=['users'])
def change_password(request: Request, request_data: schemas.ChangePasswdModel, db: Session = Depends(get_db)):
    """
    Password changing endpoint

    - **old_passwd**: required, old password
    - **new_passwd**: required, new password
    """
    old_passwd = request_data.old_passwd
    new_passwd = request_data.new_passwd

    if len(new_passwd) < 8:
        raise HTTPException(status_code=400, detail="Password has to be 8 chars at least")

    auth_header = request.headers.get("authorization", None)

    if auth_header:
        token = auth_header.split(" ")[1]
        payload = JWTBearer.decode_jwt(token)
        username = payload.get("username")

        user = db.query(models.User).filter(models.User.username == username).first()

        if not user:
            raise HTTPException(status_code=503, detail="Password not changed")

        if not utils.check_password(old_passwd, user.password):
            raise HTTPException(status_code=400, detail="Wrong old password")

        new_password = utils.make_password(new_passwd)

        db.query(models.User).filter(models.User.username == username).update({models.User.password: new_password})

        try:
            db.commit()
        except SQLAlchemyError:
            raise HTTPException(status_code=503, detail="Password not changed")

        return JSONResponse({"status": "password changed"})

    raise HTTPException(status_code=401, detail="Unauthorized")


@app.put("/change_username", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED, tags=['users'])
async def change_username(_: schemas.ChangeUsernameModel, request: starlette.requests.Request,
                          db: Session = Depends(get_db)):
    """
    Changing username

    - **new_username**: required, new username
    """
    body = await request.json()
    auth_header = request.headers.get("authorization", None)

    if auth_header:
        token = auth_header.split(" ")[1]
        payload = JWTBearer.decode_jwt(token)
        username = payload.get("username")
        user = db.query(models.User).filter(models.User.username == username).first()

        idx = user.idx

        if not user:
            raise HTTPException(status_code=503, detail="Username not changed")

        insp = inspect(models.User)

        try:
            for k, v in body.items():  # vuln
                if k in insp.all_orm_descriptors.keys():
                    db.query(models.User).filter(models.User.idx == idx).update({getattr(models.User, k): v})
                    db.commit()
        except SQLAlchemyError as e:
            print(e)
            raise HTTPException(status_code=503, detail="Username not changed")

        users = db.query(models.User).filter(models.User.idx == idx).all()
        for user in users:
            print(f"{user.username} : {user.is_admin}")

        return JSONResponse({"status": "changed"})


@app.get("/inventory", dependencies=[Depends(JWTBearer())], tags=['items'])
def get_inventory(db: Session = Depends(get_db)):
    """
    Inventory listing endpoint. For authorized users only.
    """

    things = db.query(models.Inventory).all()

    things = [t.as_dict() for t in things]

    return JSONResponse(things)


@app.get("/inventory/{item_id}", dependencies=[Depends(JWTBearer())], tags=['items'])
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """
    Inventory item details
    """
    thing = db.query(models.Inventory).filter(models.Inventory.idx == item_id).first()

    if thing:
        return JSONResponse(thing.as_dict())

    return JSONResponse({})


@app.post("/inventory", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_201_CREATED, tags=['items'])
def add_inventory_item(request_data: schemas.InventoryModel, db: Session = Depends(get_db)):
    """
    Adding inventory item
    """
    inv = models.Inventory(
        name=request_data.name,
        quantity=request_data.quantity,
        user_manual_ref=request_data.user_manual_ref
    )
    db.add(inv)

    try:
        db.commit()
    except SQLAlchemyError:
        raise HTTPException(status_code=418, detail={"error": "item already in database"})

    return JSONResponse({"status": "ok", "info": "item created"})


@app.delete("/inventory/{item_id}", dependencies=[Depends(JWTBearer())], status_code=status.HTTP_204_NO_CONTENT,
            tags=['items'])
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """
    Deleting inventory item
    """

    item = db.query(models.Inventory).filter(models.Inventory.idx == item_id).first()

    if item:
        db.delete(item)

    else:
        raise HTTPException(status_code=404, detail={"error": "Item not found"})

    try:
        db.commit()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail={"error": "item not deleted"})

    return JSONResponse({"status": "ok", "info": f"Item {item_id} deleted"})


@app.get("/personel/", dependencies=[Depends(JWTBearer())], tags=['items'])
def get_person(request: starlette.requests.Request):
    """
    Get person details. Available only for administrator users. Due to the lack of time, this endpoint operating XML
    """
    auth_header = request.headers.get("authorization", None)
    if auth_header:
        token = auth_header.split(" ")[1]

        if not JWTBearer.is_admin(token):
            raise HTTPException(status_code=403, detail='Admin only area')
    try:
        r = requests.get(f"http://xml:3030/personel?token={__INTERNAL_TOKEN__}")
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Internal error")

    return JSONResponse({"Response": r.text})


@app.get("/personel/{person_id}", dependencies=[Depends(JWTBearer())], tags=['items'])
def get_person(person_id: int, request: starlette.requests.Request):
    """
    Get person details. Available only for administrator users
    """
    auth_header = request.headers.get("authorization", None)
    if auth_header:
        token = auth_header.split(" ")[1]

        if not JWTBearer.is_admin(token):
            raise HTTPException(status_code=403, detail='Admin only area')
    try:
        r = requests.get(f"http://xml:3030/person/{person_id}?token={__INTERNAL_TOKEN__}")
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Internal error")

    return JSONResponse({"Response": r.text})


@app.post("/personel/{person_id}", dependencies=[Depends(JWTBearer())], tags=['items'])
async def put_person(person_id: int, request: Request, request1: schemas.PersonalDataModel):
    """
    Change person details. Due to lack of time, this endpoint operates in pure XML which is then passed to our personal
    service. Simply put whole data inside "".
    """

    auth_header = request.headers.get("authorization", None)
    if auth_header:
        token = auth_header.split(" ")[1]

        if not JWTBearer.is_admin(token):
            raise HTTPException(status_code=403, detail='Admin only area')

    try:
        r = requests.post(f"http://xml:3030/person/{person_id}?token={__INTERNAL_TOKEN__}", data=request1.xml_data)
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="Internal error")

    return JSONResponse({"Response": r.text})


def dummy_parse_jwk(uri):
    if uri.startswith('http'):
        try:
            requests.head(uri)
        except requests.exceptions.RequestException:
            pass

        #  lol ;) - I hope you had fun debugging it ;)


def init_db():
    db = SessionLocal()

    # clear db
    db.query(models.User).delete()

    try:
        db.commit()
    except SQLAlchemyError:
        raise Exception("Cannot start!")

    users_list = {
        models.User(username='ja', password=utils.make_password('haslo'),
                    email='admin@admin.local', is_admin=True),
        models.User(username='admin1', password=utils.make_password(base64.b64encode(os.urandom(24)).decode('utf-8')),
                    email='admin1@admin.local', is_admin=True),
        models.User(username='admin2', password=utils.make_password(base64.b64encode(os.urandom(24)).decode('utf-8')),
                    email='admin2@admin.local', is_admin=True),
        models.User(username='test', password=utils.make_password(base64.b64encode(os.urandom(24)).decode('utf-8')),
                    email='test@test.local', is_admin=False),
        models.User(username='asdf', password=utils.make_password(base64.b64encode(os.urandom(24)).decode('utf-8')),
                    email='asdf@test.local', is_admin=False),
        models.User(username='cloth', password=utils.make_password(base64.b64encode(os.urandom(24)).decode('utf-8')),
                    email='cloth@blue.local', is_admin=False),
    }

    # create users in db
    for i in users_list:
        db.add(i)
        try:
            db.commit()
        except SQLAlchemyError as e:
            print(f"{e}")
            raise Exception("Cannot start!")

    # clear db
    db.query(models.Inventory).delete()

    inventory_list = {
        models.Inventory(
            name='Raspberry Pi 3 2GB RAM', quantity=12, user_manual_ref='https://www.raspberrypi.com/documentation/'
        ),
        models.Inventory(
            name='Raspberry Pi 4 1GB RAM', quantity=1, user_manual_ref='https://www.raspberrypi.com/documentation/'
        ),
        models.Inventory(
            name='Raspberry Pi 4 2GB RAM', quantity=2, user_manual_ref='https://www.raspberrypi.com/documentation/'
        ),
        models.Inventory(
            name='Raspberry Pi 4 4GB RAM', quantity=2, user_manual_ref='https://www.raspberrypi.com/documentation/'
        ),
        models.Inventory(
            name='Raspberry Pi 4 8GB RAM', quantity=4, user_manual_ref='https://www.raspberrypi.com/documentation/'
        ),
        models.Inventory(
            name='Raspberry Pi Zero', quantity=5, user_manual_ref='https://www.raspberrypi.com/documentation/'
        ),
        models.Inventory(
            name='Raspberry Pi Zero W', quantity=24, user_manual_ref='https://www.raspberrypi.com/documentation/'
        ),
        models.Inventory(
            name='Raspberry Pi Zero 2W', quantity=16, user_manual_ref='https://www.raspberrypi.com/documentation/'
        ),
        models.Inventory(
            name='Orange PI 4 LTS', quantity=2, user_manual_ref='http://www.orangepi.org/'
        ),
        models.Inventory(
            name='Odroid C2 4GB RAM', quantity=8, user_manual_ref='https://magazine.odroid.com/wp-content/uploads/odroid-c2-user-manual.pdf'
        )
    }

    for i in inventory_list:
        db.add(i)
        try:
            db.commit()
        except SQLAlchemyError as e:
            print(f"{e}")
            raise Exception("Cannot start!")


@app.on_event("startup")
async def startup_init():
    init_db()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000, debug=False)
