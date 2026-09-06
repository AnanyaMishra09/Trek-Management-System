from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)
    CORS(app)

    from models import booking, staff_profile, trek, user  # noqa: F401  registers tables

    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.staff import staff_bp
    from routes.user import user_bp
    from routes.history import history_bp
    from routes.export import export_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(export_bp)

    @app.route("/")
    def home():
        return {"message": "Trekking Management Application API"}

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
