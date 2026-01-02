from flask import Blueprint, abort, make_response, request, Response
from app.db import db
from app.models.board import Board
from app.models.card import Card

def validate_model(cls, id, refresh=False):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{cls.__name__} {id} invalid"}, 400))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {id} not found"}, 404))

    if refresh:
        db.session.refresh(model)
    return model

def create_model(cls,data_dict):
    try:
        new_model = cls.from_dict(data_dict)
    except KeyError as e:
        abort(make_response({"message": f"Missing required field: {e.args[0]}"}, 400))

    db.session.add(new_model)
    db.session.commit()
    return new_model.to_dict(), 201

def delete_model(cls, id):
    model = validate_model(cls, id)

    db.session.delete(model)
    db.session.commit()
    return make_response({"message": f"{cls.__name__} {id} successfully deleted"}, 200)

def update_model(cls, id, data_dict):
    model = validate_model(cls, id)

    for key, value in data_dict.items():
        if hasattr(cls, key):
            setattr(model, key, value)

    db.session.commit()
    return model.to_dict(), 200

def get_models_or_abort(Model, id_list):

    instances = db.session.query(Model).filter(Model.id.in_(id_list)).all()

    if len(instances) != len(id_list):
        found_ids = {instance.id for instance in instances}
        missing_ids = [str(id) for id in id_list if id not in found_ids]

        if missing_ids:
            abort(make_response({"message": f"{Model.__name__}s with IDs {', '.join(missing_ids)} not found"}, 404))

    return instances