from flask import Flask, jsonify, request;
from datetime import datetime;
from elasticsearch import Elasticsearch, NotFoundError;
from es_functions import initialize, filldummy;
from contact import Contact;

#by default, connects to localhost:9200
es = Elasticsearch();
initialize(es);
filldummy(es);
app = Flask(__name__);


#GET /contact?pageSize={}&page={}&query={}

#SEARCH : GET , with specified parameters
@app.route('/contact', methods=['GET'])
def search_pages():
    pageSize = request.args.get('pageSize','');
    page = request.args.get('page','');
    query = request.args.get('query','');

    res = es.search(index="contacts", doc_type="contact", body={"query": {"query_string": {"query" : query}}}, from_=int(page)*int(pageSize), size=pageSize);

    return formatRes(res);



#CREATE : POST
@app.route('/contact', methods=['POST'])
def create():
    #searching if the id already exists
    if(exists(request.form['name'])):
        return "ERROR: Contact already exists.";
    else:
        contact = Contact(request.form['name'], request.form['phone1'], request.form['phone2'], request.form['zipcode']);
        return(contact.insert(es));



#SEARCH : GET
@app.route('/contact/<string:name>', methods=['GET'])
def search_name(name):
    try:
        res = es.search(index="contacts", doc_type="contact", body={"query" : {"match" : { "name" : name}}});
        res = formatRes(res);
    except NotFoundError as n:
        res = "ERROR: Not Found";
    return str(res);



#UPDATE : PUT
#Limitation: Cannot update name (which is tied to the id).
@app.route('/contact/<string:name>', methods=['PUT'])
def update(name):
    if(exists(name)):

        contact_body = {
        "doc" : {
            "name" : request.form['name'],
            "phone1" : request.form['phone1'],
            "phone2" : request.form['phone2'],
            "zipcode" : request.form['zipcode']
            }
        };

        res = es.update(index="contacts", doc_type="contact", id=name, body=contact_body);

        return str(res['result']);
    else:
        return "ERROR: Not Found";



#DELETE : DELETE
@app.route('/contact/<string:name>', methods=['DELETE'])
def delete(name):
    #checking if exists
    if(exists(name)):
        res = es.delete(index="contacts", doc_type="contact", id=name);
    else:
        res="ERROR: Not Found";
    return str(res['result']);



#Bool
def exists(name):
    return es.exists(index="contacts", doc_type="contact", id=name);



#Formats results to be more presentable for the GET search queries.
def formatRes(res):
    res_pretty = str(res['hits']['total']) + " results \n";
    for doc in res['hits']['hits']:
        res_pretty = res_pretty + str(doc['_source']) + "\n";
    return res_pretty ;
