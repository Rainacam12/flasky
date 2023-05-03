from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.crystal import Crystal

# 4/28 comment out crystal class and hardcoded data on line 11
# class Crystal:
#     def __init__(self, id, name, color, powers):
#         self.id = id
#         self.name = name
#         self.color = color
#         self.powers = powers

# create a list of instances
# crystals = [
#     Crystal(1, "Amethyst", "Purple", "Infinite knowledge and wisdom"),
#     Crystal(2, "Tiger's Eye", "Gold", "Confidence, strength"),
#     Crystal(3, "Rose Quartz", "Pink", "Love")
# ]

crystal_bp = Blueprint("crystals", __name__, url_prefix="/crystals")

# create endpoint to get resources
# @crystal_bp.route("", methods=["GET"])

# def handle_crystals():
#     crystal_response = []
#     for crystal in crystals:
#         crystal_response.append({
#             "id": crystal.id,
#             "name": crystal.name,
#             "color": crystal.color,
#             "powers": crystal.powers
#         })

#     return jsonify(crystal_response)


def validate_crystal(crystal_id):
    try:
        crystal_id = int(crystal_id)
    except:
        abort(make_response({"message": f"{crystal_id} is not a valid type ({type(crystal_id)})."}, 400))

    crystal = Crystal.query.get(crystal_id)

    if not crystal:
        abort(make_response({"message":f"Crystal {crystal_id} does not exist"}, 404))

    return crystal

# define route for creating a crystal
@crystal_bp.route("", methods=['POST'])
def handle_crystals():
    request_body = request.get_json()

    new_crystal = Crystal(
        name = request_body["name"],
        color = request_body["color"],
        powers = request_body["powers"]
    )

    db.session.add(new_crystal)
    db.session.commit()

    return make_response(f"Crystal {new_crystal.name} successfully created", 201)

# define a route for getting all crystals 
@crystal_bp.route("", methods=['GET'])
def read_all_crystals():
    crystals_response = []
    # query.all gets crystals from db
    crystals = Crystal.query.all()

    # add each crystal to the response body
    for crystal in crystals:
        crystals_response.append({
            "id": crystal.id,
            "name": crystal.name,
            "color": crystal.color,
            "powers": crystal.powers
        })
    return jsonify(crystals_response)

# define a route for getting a sunngle crystal
# GET/crystals/<crystal_id>

@crystal_bp.route("/<crystal_id>", methods=["GET"])
def read_one_crystal(crystal_id):
    # query our db to grab the crystal that has the id we want
    crystal = validate_crystal(crystal_id)

    # show single crystal
    return {
       "id": crystal.id,
            "name": crystal.name,
            "color": crystal.color,
            "powers": crystal.powers 
    }, 200

# define a route for updating crystal
# PUT /CRYSTALS/<crystal_id>
@crystal_bp.route("/<crystal_id>", methods=['PUT'])
def update_crystal(crystal_id):
    # query our db to grab the crystal that has the id we want
    crystal = validate_crystal(crystal_id)
    # shape request body
    request_body = request.get_json()

    crystal.name = request_body["name"]
    crystal.color = request_body["color"]
    crystal.powers = request_body["powers"]

    # commit changes 
    db.session.commit()

    # send back updated crystal
    return {
        "id": crystal.id,
        "name": crystal.name,
        "color": crystal.color,
        "powers": crystal.powers 
    }, 200

# Define a route for deleting one crystal
# DELETE/crystals/<crystal_id>
@crystal_bp.route("/<crystal_id>", methods=['DELETE'])
def delete_crystal(crystal_id):
    crystal = validate_crystal(crystal_id)

    db.session.delete(crystal)
    db.session.commit()

    return make_response(f"Crystal #{crystal.id} successfully deleted")
