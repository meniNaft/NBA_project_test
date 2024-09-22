from dataclasses import asdict
from flask import Blueprint, request, jsonify
from models.responseDto import ResponseDto
import services.teams_service as teams_service
import validations.teams_validation as validation
from typing import List

team_blueprint = Blueprint("teams", __name__)


@team_blueprint.route("/", methods=["POST"])
def create_team():
    data = request.json
    team_name = data.get("team_name")
    player_ids: List[int] = data.get("player_ids")
    if not team_name or not isinstance(player_ids, list) or len(player_ids) != 5:
        return jsonify(asdict(ResponseDto(error="invalid input"))), 400
    elif not validation.is_valid_player_positions(player_ids):
        return jsonify(asdict(ResponseDto(error="should be all 5 type of positions"))), 400
    elif validation.is_team_exist_by_name(team_name):
        return jsonify(asdict(ResponseDto(error="this team is already exist"))), 400
    elif validation.is_players_in_other_team_by_team_name(player_ids, team_name):
        return jsonify(asdict(ResponseDto(error="team not found"))), 400
    else:
        team_id = teams_service.create_new_team(player_ids, team_name)
        return jsonify(asdict(ResponseDto(body={"team_id": team_id}, message="team created successfully"))), 201


@team_blueprint.route("/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    data = request.json
    player_ids: List[int] = data.get("player_ids")
    if not isinstance(player_ids, list) or len(player_ids) != 5:
        return jsonify(asdict(ResponseDto(error="invalid input"))), 400
    elif not validation.is_valid_player_positions(player_ids):
        return jsonify(asdict(ResponseDto(error="should be all 5 type of positions"))), 400
    elif not validation.is_team_exist(team_id):
        return jsonify(asdict(ResponseDto(error="team not found"))), 400
    elif validation.is_players_in_other_team(player_ids, team_id):
        return jsonify(asdict(ResponseDto(error="team not found"))), 400
    elif not teams_service.update_team_players(player_ids, team_id):
        return jsonify(asdict(ResponseDto(error="some error occurred"))), 400
    else:
        return jsonify(asdict(ResponseDto(message="team updated successfully"))), 204


@team_blueprint.route("/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    if not validation.is_team_exist(team_id):
        return jsonify(asdict(ResponseDto(error="team not exist"))), 404
    is_success_deleting = teams_service.delete(team_id)
    if is_success_deleting:
        return jsonify(asdict(ResponseDto(error="team deleted successfully"))), 204
    else:
        return jsonify(asdict(ResponseDto(error="some error occurred"))), 400


@team_blueprint.route("/<int:team_id>", methods=["GET"])
def get_team_players_details(team_id):
    res = teams_service.get_team_by_id(team_id)
    if res is None:
        return jsonify(asdict(ResponseDto(error="team not found"))), 404
    return jsonify(asdict(ResponseDto(body=res))), 200
