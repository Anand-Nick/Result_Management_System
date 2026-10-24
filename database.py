from flask import Flask
from models import db, Admin
from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__)

    # Secret key for session management
    app.config["SECRET_KEY"] = "resultmanagement123"

    # SQLite Database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///result.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy
    db.init_app(app)

    return app


def initialize_database():
    """
    Creates all tables and inserts a default admin account
    if one does not already exist.
    """

    app = create_app()

    with app.app_context():
        db.create_all()

        # Create default admin
        admin = Admin.query.filter_by(username="admin").first()

        if not admin:
            new_admin = Admin(
                username="admin",
                password=generate_password_hash("admin123")
            )

            db.session.add(new_admin)
            db.session.commit()

            print("===================================")
            print("Database Created Successfully")
            print("Default Admin Created")
            print("Username : admin")
            print("Password : admin123")
            print("===================================")
        else:
            print("Database already exists.")


if __name__ == "__main__":
    initialize_database()