import os

from flask import Flask
from flask_login import LoginManager

from limit import limiter
from models import Client, Document, User, db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    db.init_app(app)
    limiter.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app


def initialize_database(app):
    with app.app_context():
        db.create_all()

        if not User.query.get(1):
            test_user = User(id=1, username="t.testovich", password="test-passwd-894")
            db.session.add(test_user)

        if not Document.query.get(1):
            documents = [
                Document(
                    id=1, name="Образец рапорта на выдачу довольствия", path="doc1.docx"
                ),
                Document(
                    id=2,
                    name="Образец заявки на изготовление талонов",
                    path="doc2.docx",
                ),
                Document(
                    id=3, name="Образец списка норм довольствия", path="doc3.docx"
                ),
            ]
            db.session.bulk_save_objects(documents)

        if not Client.query.get(1):
            clients = [
                Client(id=1, name="Дикобраз", coupon="талон-XXXXXXXXXX"),
                Client(id=2, name="Выдра", coupon="талон-XXXXXXXXXX"),
            ]
            db.session.bulk_save_objects(clients)

        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    initialize_database(app)
    app.run(host="0.0.0.0", debug=True)
