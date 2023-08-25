from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
import argparse

db = PostgresqlDatabase('people', user='postgres', password='', host='localhost', port=5432)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

class BaseModel(Model):
  class Meta:
    database = db

class Contact(BaseModel):
  name = CharField()
  age = IntegerField()

db.connect()
db.drop_tables([Contact])
db.create_tables([Contact])

Contact(name='Self', email_address='self@gmail.com', phone_number='800-555-5555', street_address_one='123 Fake Street', street_address_two='Apt 1A', city='New York', state='NY', zipcode=10001).save()

app = Flask(__name__)

@app.route('/contact/', methods=['GET', 'POST'])
@app.route('/contact/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Contact.get(Contact.id == id)))
    else:
        contact_list = []
        for contact in Contact.select():
            contact_list.append(model_to_dict(contact))
        return jsonify(contact_list)

  if request.method =='PUT':
    body = request.get_json()
    Contact.update(body).where(Contact.id == id).execute()
    return f'Contact {id} has been updated.'

  if request.method == 'POST':
    new_contact = dict_to_model(Contact, request.get_json())
    new_contact.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Contact.delete().where(Contact.id == id).execute()
    return f'Contact {id} has been deleted.'

app.run(debug=True, port=9000)