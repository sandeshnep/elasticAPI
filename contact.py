from elasticsearch import RequestError;

#contact blueprint
class Contact:
    def __init__(self, name, phone1, phone2, zipcode):
        self.name = name;
        self.phone1 = phone1;
        self.phone2 = phone2;
        self.zipcode = zipcode;

    def insert(self, es):
        try:
            res = es.index(index="contacts", doc_type="contact", id=self.name , body={"name": self.name, "phone1" : self.phone1, "phone2" : self.phone2, "zipcode" : self.zipcode});
            return str(res['_id']) + " " + str(res['result']);
        except RequestError as err:
            msg = "Error: One or more of the fields do not conform to contact_definition in es_functions.py/initialize(). More details:\n" + str(err);
            return msg;
