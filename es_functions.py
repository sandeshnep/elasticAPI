#Purpose: defines types for the contact entity, creates a "contacts" index in es and loads data into it.
from contact import Contact;

def initialize(es):
    #safeguard: delete contacts index if it exists
    if(es.indices.exists(index="contacts")):
        es.indices.delete(index="contacts");

    #types of allowed fields in the contact entity.
    contact_definition={
        "settings" : {"number_of_shards" : 1},
        "mappings": {
                "contact": {
                    "properties": {
                        "name": {"type": "keyword"},
                        "phone1": {"type": "long"},
                        "phone2": {"type": "long"},
                        "zipcode": {"type": "integer"}}}}}

    #creates an emptyindex
    es.indices.create(index="contacts", body=contact_definition, ignore=400);


def filldummy(es):
    for line in open('load.dummy'):
        data = line.split(',');
        contact = Contact(data[0], data[1], data[2], data[3]);
        print(contact.insert(es));
