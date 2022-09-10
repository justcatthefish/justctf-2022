#! /usr/bin/env python3

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class RegisterResponseModel(BaseModel):
    status: str
    info: str


class TimestampModel(BaseModel):
    Timestamp: int
    Ping: str


class PingResponseModel(BaseModel):
    heartbeat: TimestampModel


class JWTResponseModel(BaseModel):
    token: str


class ChangePasswdModel(BaseModel):
    old_passwd: str
    new_passwd: str


class ChangeUsernameModel(BaseModel):
    username: str


class InventoryModel(BaseModel):
    name: str
    quantity: str
    user_manual_ref: str


class PersonalDataModel(BaseModel):
    xml_data: str