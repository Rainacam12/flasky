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

@crystal_bp.route("", methods=['POST'])

# define route for creating a crystal
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