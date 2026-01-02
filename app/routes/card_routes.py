from flask import Blueprint, abort, make_response, request, Response
from app.db import db
from app.models.board import Board
from app.models.card import Card
from .route_utilities import validate_model, create_model, delete_model, update_model

bp = Blueprint("card_bp", __name__, url_prefix="/boards/<board_id>/cards")

@bp.route("", methods=["POST"])
def create_card(board_id):
    validate_model(Board, board_id)

    data = request.get_json()
    data["board_id"] = board_id

    return create_model(Card, data)

@bp.route("", methods=["GET"])
def get_cards(board_id):
    validate_model(Board, board_id)

    cards = db.session.query(Card).filter(Card.board_id == board_id).order_by(Card.id).all()
    return make_response({"cards": [card.to_dict() for card in cards]}, 200)

@bp.route("/<id>/like", methods=["PATCH"])
def like_card(board_id, id):
    validate_model(Board, board_id)
    card = validate_model(Card, id)

    if card.board_id != int(board_id):
        abort(make_response(
            {"message": f"Card {id} does not belong to Board {board_id}"},
            400
        ))

    return update_model(Card, id, {"likes": card.likes + 1})

@bp.route("/<id>", methods=["DELETE"])
def delete_card(board_id, id):
    validate_model(Board, board_id)
    card = validate_model(Card, id)

    if card.board_id != int(board_id):
        abort(make_response({"message": f"Card {id} does not belong to Board {board_id}"}, 400))

    return delete_model(Card, id)


