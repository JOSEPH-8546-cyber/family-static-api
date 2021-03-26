"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_members():
    members = jackson_family.get_all_members()
    # response_body = {
    #     "hello": "Mr White",
    #     "family": members
    # }
    return jsonify(members), 200

@app.route('/members/<int:position>', methods=['GET'])
def get_member(position):
    member = jackson_family.get_member(position)
    response_body = {
        "family": member
    }
    return jsonify(response_body), 200


@app.route('/members', methods=['POST'])
def add_new_members():
     request_body = request.data
     decoded_object = json.loads(request_body)
     response=jackson_family.add_new_members(decoded_object)
     if response == True:
         print('the member is add', request_body)
         return jsonify(jackson_family.get_all_members()), 200
     else:
        return "Error", 500



@app.route('/members/<int:position>', methods=['DELETE'])
def delete_member(position):
    if type(position) != int:
        return jsonify(jackson_family.get_all_members()), 400
    else:
        result = jackson_family.delete_member(position)
        if result == True:
            print('this member is delete', position)
            return jsonify('member delete successfully'), 200
        else:
            'Error', 500





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
