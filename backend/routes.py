from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return data,200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"]) 
def get_picture_by_id(id):
    for i in data:
        if i.get("id") == id:
            return i
    return jsonify({"message": "Picture not found"}), 404
# CREATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["POST"])
def create_picture(id):
    picture_data = request.get_json()

   
    for existing_picture in data:
        if existing_picture.get("id") == id:
            return jsonify({"Message": f"Picture with id {id} already present"}), 302

    new_picture = {
        "id":  picture_data.get("id"),
        "pic_url": picture_data.get("pic_url"),
        "event_country": picture_data.get("event_country"),
        "event_state": picture_data.get("event_state"),
        "event_city": picture_data.get("event_city"),
        "event_date": picture_data.get("event_date")
    }
    data.append(new_picture)

    return jsonify(new_picture), 201

    
    
 
    

 
    
  
 
 
    
 
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_data = request.get_json()

    for existing_picture in data:
        if existing_picture.get("id") == id:
            existing_picture == picture_data
            return jsonify(existing_picture),200
    return {"message": "picture not found"},404
 
   




######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i in data:
        if i.get("id") == id:
            data.remove(i)
            return {"message": "HTTP_204_NO_CONTENT."},204
    return {"message": "picture not found"} ,404
