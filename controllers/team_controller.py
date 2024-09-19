from dataclasses import asdict
from flask import Blueprint, request, jsonify
from models.responseDto import ResponseDto
from services.players_service import search_players
from validations.players_validations import check_search_players_validation

team_blueprint = Blueprint("teams", __name__)


@team_blueprint.route("/", methods=["GET"])
def get_players():
     pass
     # # position = request.args["position"]
     # # season = request.args["season"]
     # user_input = check_search_players_validation(request.args)
     # data = search_players(position, season)
     # return jsonify(asdict(ResponseDto(body=data))), 200

