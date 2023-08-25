from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from app import Contact

def contacts():
    contact_list = []
    for contact in Contact.select():
        contact_list.append(model_to_dict(contact))

    def create():
        name = input('Input contact name here: ')
        email_address = input('Input contact email address here: ')
        phone_number = input('Input contact phone number here: ')
        street_address_one = input('Input contact street address (number and street name) here: ')
        street_address_two = input('Input contact apartment or suite number here (if applicable): ')
        city = input('Input contact city here: ')
        state = input('Input contact state here: ')
        zipcode = input('Input contact zipcode here: ')

        new_contact = Contact(name = name, email_address = email_address, phone_number = phone_number, street_address_one = street_address_one, street_address_two = street_address_two, city = city, state = state, zipcode = zipcode)
        new_contact.save()
        print(f'{new_contact.name} has been added to your contacts')

    def read():
        for i in contact_list:
            print(f"Name: {i['name']}\nEmail Address: {i['email_address']}\nPhone Number: {i['phone_number']}\nStreet Address: {i['street_address_one']}\n")
            if i['street_address_two']:
                print(f"Street Address Line Two: {i['street_address_two']}\n")
            print(f"City: {i['city']}\nState: {i['state']}\nZipcode: {i['zipcode']}")

    def create_or_read():
        choice = input(f'Enter 1 to add a new contact or 2 to view your contacts: ')

        if choice == '1':
            create()
        elif choice == '2':
            read()
        else:
            create_or_read()
        
    create_or_read()

contacts()