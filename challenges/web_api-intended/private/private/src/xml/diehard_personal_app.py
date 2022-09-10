#!/usr/bin/env python3

import faker
from flask import Flask, request, jsonify, Response
from lxml import etree


app = Flask(__name__)
fake = faker.Faker()
__TOKEN__ = 'c6ajUzKXJSdMBErkARNxBySPXVUFlaTfKAA6UCJjF3m97fP61IB36ZphsNWZ9t4'
__PERSONEL__ = {}
_PERSON_ = """
<?xml version="1.0" encoding="UTF-8"?>
<person>
<username>{username}</username>
<name>{name}</name>
<job_title>{job}</job_title>
<ssn>{ssn}</ssn>
<internet_provider>{IP}</internet_provider>
<date_of_employment>{date_of_employment}</date_of_employment>
</person>
""".replace('\n', '')


def check_if_authorized(token):
    if not token or token != __TOKEN__:
        return False
    return True


@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'API': {'version': '1a'}})


@app.route('/personel', methods=['GET'])
def personel():
    if not check_if_authorized(request.args.get('token', None)):
        return jsonify({'error': 'Not Authorized'}), 403

    return jsonify(__PERSONEL__), 200


@app.route('/person/<int:idx>', methods=['GET', 'POST'])
def person(idx):
    if not check_if_authorized(request.args.get('token', None)):
        print('here')
        return jsonify({'error': 'Not Authorized'}), 403

    if not idx in __PERSONEL__.keys():
        return jsonify({'error': 'Not found'}), 404

    if request.method == 'GET':
        return Response(__PERSONEL__[idx], mimetype='text/xml')

    elif request.method == 'POST':
        parser = etree.XMLParser(no_network=False)  # vuln
        p = request.data.strip().replace(b'\n', b'')
        p = p.replace(b'proc', b'')
        p = p.replace(b'http', b'')

        if p is not None:
            try:
                data = etree.fromstring(p, parser)
                parsed_xml = etree.tostring(data)
            except etree.XMLSyntaxError:
                return jsonify({'error': 'General error'}), 503

            # __PERSONEL__[idx] = parsed_xml.decode('utf-8')

            return jsonify({'status':  parsed_xml.decode('utf-8')}), 200

    return jsonify({'error': 'General error'}), 503


@app.before_first_request
def generate_people():
    for i in range(30):
        profile = fake.profile()
        person = _PERSON_.format(
            username=fake.simple_profile()['username'],
            name=profile['name'],
            job=profile['job'],
            ssn=profile['ssn'],
            IP=fake.company(),
            date_of_employment=fake.date()
        )
        __PERSONEL__[i] = person


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3030)
