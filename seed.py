from dotenv import load_dotenv
from app import create_app
from app.db import db
from app.models.board import Board
from app.models.card import Card

# ---------- Data ----------
boards_data = [
    {"title": "Daily Life", "name": "Alice"},
    {"title": "Career", "name": "Bob"},
    {"title": "Health & Fitness", "name": "Charlie"},
]

cards_data = [
    {"message": "Go for a walk 🏞", "likes": 0, "board_title": "Daily Life"},
    {"message": "Water the plants 🌱", "likes": 0, "board_title": "Daily Life"},
    {"message": "Update resume", "likes": 0, "board_title": "Career"},
    {"message": "Practice LeetCode", "likes": 0, "board_title": "Career"},
    {"message": "Do 20 push-ups 💪", "likes": 0, "board_title": "Health & Fitness"},
]

# ---------- Utility ----------
def get_by_field(cls, field_name, value):
    stmt = db.select(cls).where(getattr(cls, field_name) == value)
    return db.session.scalar(stmt)

# ---------- Main ----------
def main():
    load_dotenv()
    app = create_app()

    with app.app_context():
        # --- Seed Boards ---
        title_to_board = {}
        for b in boards_data:
            board = get_by_field(Board, "title", b["title"]) or Board(
                title=b["title"],
                name=b["name"]
            )
            if board.id is None:
                db.session.add(board)
                db.session.flush()  # ensures board.id is assigned
            title_to_board[board.title] = board

        # --- Seed Cards ---
        for c in cards_data:
            existing = get_by_field(Card, "message", c["message"])
            if existing:
                continue

            board = title_to_board.get(c["board_title"])
            if not board:
                continue

            card = Card(
                message=c["message"],
                likes=c.get("likes", 0),
                board_id=board.id
            )
            db.session.add(card)

        db.session.commit()

        # --- Print Summary ---
        print("Seed complete.\nBoards and their cards:")
        boards = db.session.scalars(db.select(Board)).all()
        for board in boards:
            db.session.refresh(board)  # ensures board.cards relationship is loaded
            print(f"- [{board.id}] {board.title} ({board.name})")
            for card in board.cards:
                print(f"   • [{card.id}] {card.message} (likes: {card.likes})")

if __name__ == "__main__":
    main()