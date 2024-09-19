from dataclasses import asdict
from flask import Blueprint, request, jsonify
from models.responseDto import ResponseDto
from services.players_service import search_players
from validations.players_validations import check_search_players_validation

player_blueprint = Blueprint("players", __name__)


@player_blueprint.route("/", methods=["GET"])
def get_players():
    position = request.args.get("position")
    season = request.args.get("season")
    is_valid = check_search_players_validation(position, season)
    if is_valid:
        data = search_players(position, season)
        return jsonify(asdict(ResponseDto(body=data))), 200
    else:
        return jsonify(asdict(ResponseDto(error="invalid input"))), 400
