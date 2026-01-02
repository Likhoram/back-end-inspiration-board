from flask import Blueprint, abort, make_response, request, Response
from app.db import db
from app.models.board import Board
from app.models.card import Card
from .route_utilities import validate_model, create_model, delete_model, update_model, get_models_or_abort

bp = Blueprint("board_bp", __name__, url_prefix="/boards")

@bp.route("", methods=["POST"])
def create_board():
    data = request.get_json()
    return create_model(Board, data)

@bp.route("/<id>", methods=["DELETE"])
def delete_board(id: str):
    return delete_model(Board, id)

@bp.route("", methods=["GET"])
def get_boards():
    boards = db.session.query(Board).all()
    boards_list = [board.to_dict() for board in boards]
    return make_response({"boards": boards_list}, 200)

@bp.route("/<id>", methods=["GET"])
def get_board(id: str):
    board = validate_model(Board, id)
    return make_response(board.to_dict(), 200)

@bp.route("/<id>", methods=["PATCH"])
def update_board(id: str):
    data = request.get_json()
    board = validate_model(Board, id)
    return update_model(board, data)

@bp.route("/<id>/cards", methods=["POST"])
def link_cards_with_board_id(id: str):
    data = request.get_json()
    board = validate_model(Board, id)

    for card_data in data.get("cards", []):
        new_card = Card.from_dict(card_data)
        new_card.board = board
        db.session.add(new_card)

    db.session.commit()

    return make_response(board.to_dict(), 200)

