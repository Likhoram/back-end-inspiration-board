from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from ..db import db

class Board(db.Model):
    __tablename__ = "board"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    cards: Mapped[Optional[list["Card"]]] = relationship(back_populates="board")

    def to_dict(self, include_cards=True) -> dict:
        model_dict = {
            "id": self.id,
            "title": self.title,
            "name": self.name,
            "cards": [card.to_dict() for card in self.cards] if include_cards else []
        }

        return model_dict

    @classmethod
    def from_dict(cls, data: dict) -> "Board":
        return cls(
            id=data.get("id"),
            title=data.get("title", ""),
            name=data.get("name", ""),
            cards=[Card.from_dict(card_data) for card_data in data.get("cards", [])] if "cards" in data else []
        )
