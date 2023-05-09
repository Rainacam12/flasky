from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.crystal import Crystal
from app.models.healer import Healer

# 4/28 comment out crystal class and hardcoded data
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
healer_bp = Blueprint("healers", __name__, url_prefix="/healers")
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

# responsible for validating and returning crystal instance
# cls is a reference to any class we are passing in
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} is not a valid type ({type(model_id)})."}, 400))
    # replace Crystal with 'cls'
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} does not exist"}, 404))

    return model

# define route for creating a crystal
@crystal_bp.route("", methods=['POST'])
def create_crystal():
    request_body = request.get_json()
    
    # pass in request_body
    new_crystal = Crystal.from_dict(request_body)

    db.session.add(new_crystal)
    db.session.commit()

    return jsonify(f"Crystal {new_crystal.name} successfully created"), 201

# define a route for getting all crystals 
@crystal_bp.route("", methods=['GET'])
def read_all_crystals():
    # filter the crystal query results
    # to those whose color mathes the 
    # query param
    color_query = request.args.get("color")
    # filter for powers
    powers_query = request.args.get("powers")
    # if query of color is present
    if color_query:
        crystals = Crystal.query.filter_by(color=color_query)
    elif powers_query:
        powers = Crystal.query.filter_by(powers=powers_query)
    else:
        crystals = Crystal.query.all()
    
    crystals_response = []
    # query.all gets crystals from db
    # crystals = Crystal.query.all()

    # add each crystal to the response body
    for crystal in crystals:
        crystals_response.append(crystal.to_dict())
    return jsonify(crystals_response)

# define a route for getting a sunngle crystal
# GET/crystals/<crystal_id>

@crystal_bp.route("/<crystal_id>", methods=["GET"])
def read_one_crystal(crystal_id):
    # query our db to grab the crystal that has the id we want
    crystal = validate_model(crystal_id)

    # show single crystal
    return crystal.to_dict(), 200

# define a route for updating crystal
# PUT /CRYSTALS/<crystal_id>
@crystal_bp.route("/<crystal_id>", methods=['PUT'])
def update_crystal(crystal_id):
    # query our db to grab the crystal that has the id we want
    crystal = validate_model(Crystal, crystal_id)
    # shape request body
    request_body = request.get_json()

    crystal.name = request_body["name"]
    crystal.color = request_body["color"]
    crystal.powers = request_body["powers"]

    # commit changes 
    db.session.commit()

    # send back updated crystal
    return crystal.to_dict(), 200

# Define a route for deleting one crystal
# DELETE/crystals/<crystal_id>
@crystal_bp.route("/<crystal_id>", methods=['DELETE'])
def delete_crystal(crystal_id):
    crystal = validate_model(crystal_id)

    db.session.delete(crystal)
    db.session.commit()

    return make_response(f"Crystal #{crystal.id} successfully deleted")


# Healers Routes
@healer_bp.route("", methods=['POST'])
# define a route for creating a crystal resource
def create_healer():
    request_body = request.get_json()
    
    new_healer = Healer(
        name=request_body["name"]
    )
    
    db.session.add(new_healer)
    db.session.commit()
    
    return jsonify(f"Yayyyy Healer {new_healer.name} successfully created!"), 201


@healer_bp.route("", methods=["GET"])
def read_all_healers():
    
    healers = Healer.query.all()
        
    healers_response = []
    
    for healer in healers:
        healers_response.append({ "name": healer.name, "id": healer.id})
    
    return jsonify(healers_response)

# create a route to create crystal by id
@healer_bp.route("/<healer_id>/crystals", methods=["POST"])
def create_crystal_by_id(healer_id):
    # pass in class and model_id
    healer = validate_model(Healer, healer_id)

    request_body = request.get_json()

    new_crystal = Crystal(
        name=request_body["name"],
        color=request_body["color"],
        powers=request_body["powers"],
        healer=healer 
    )
    # save to db
    db.session.add(new_crystal)
    db.session.commit()

    return jsonify(f"Crystal {new_crystal.name} owned by {new_crystal.healer.name} was successfully created. "), 201

@healer_bp.route("/<healer_id>/crystals", methods=["GET"])
def get_all_crystals_by_id(healer_id):
   
    healer = validate_model(Healer, healer_id)

    crystal_response = []
    for crystal in healer.crystals:
        # we can use to_dict
        crystal_response.append(crystal.to_dict())

    return jsonify(crystal_response), 200

