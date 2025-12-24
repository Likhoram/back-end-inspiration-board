from ..db import db
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Card(db.Model):
    __tablename__ = "card"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]  
    likes: Mapped[int] = mapped_column(default=0)
    board_id: Mapped[Optional[int]] = mapped_column(ForeignKey("board.id")) 
    board: Mapped[Optional["Board"]] = relationship(back_populates="cards")

    def to_dict(self):
        result = {
            "id": self.id,
            "message": self.message,
            "likes": self.likes,
        }
        if self.board_id is not None:
            result["board_id"] = self.board_id
        return result
    
    @classmethod
    def from_dict(cls, card_data):
        return cls(message=card_data["message"],
                    likes=card_data.get("likes", 0),
                    board_id=card_data.get("board_id", None)
        )
        
