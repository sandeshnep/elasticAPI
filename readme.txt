REQUIRED:
1) Flask
2) Elasticsearch
3) elasticsearch.py


FILES:
  - api.py : all required functions triggered by HTTP requests.
  - contact.py : Contact class. Contains insert method into elasticsearch for simplicity.
  - es_functions.py : initializes elasticsearch and defines the contact data model in terms of how it is stored.
  - load.dummy : dummy contacts that are automatically loaded for testing.


NOTES:
  - the unique id used with elasticsearch is name: firstname and lastname saperated by a space.
  - relevant data is in the body of corresponding response.



RUN INSTRUCTIONS:
export FLASK_APP=api.py
flask run


TESTS [using postman]:

  1) POST /contact
        form-data:
          "name" : "John Doe",
          "phone1" : "3479999999",
          "phone2" : "7189999999",
          "zipcode" : "11111"

     RESPONSE
     John Doe created


  2) GET /contact/John Doe

    RESPONSE
    1 results
    {'name': 'John Doe', 'phone1': '3475576241', 'phone2': '3474715960', 'zipcode': '11111'}


  3) DELETE /contact/John Doe

     RESPONSE
     deleted


  4) PUT /contact/AAAAA AAAAA
       form-data:
         "name" : "AAAAA AAAAA",
         "phone1" : "3479999999",
         "phone2" : "7189999999",
         "zipcode" : "99999"

      RESPONSE
      updated
