from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt

db = SQLAlchemy()
migrate = Migrate()


def seed_clubs():
    from .models import Club

    standaard_clubs = [
        ("Ajax", "Nederland"),
        ("PSV", "Nederland"),
        ("Feyenoord", "Nederland"),
        ("AZ", "Nederland"),
        ("FC Twente", "Nederland"),
        ("FC Utrecht", "Nederland"),
        ("SC Heerenveen", "Nederland"),
        ("FC Groningen", "Nederland"),
        ("PEC Zwolle", "Nederland"),
        ("Go Ahead Eagles", "Nederland"),
        ("Sparta Rotterdam", "Nederland"),
        ("Heracles Almelo", "Nederland"),
        ("NEC", "Nederland"),
        ("NAC Breda", "Nederland"),
        ("Willem II", "Nederland"),
        ("RKC Waalwijk", "Nederland"),
        ("Fortuna Sittard", "Nederland"),
        ("Almere City FC", "Nederland"),
        ("FC Emmen", "Nederland"),
        ("De Graafschap", "Nederland"),
        ("ADO Den Haag", "Nederland"),
        ("Excelsior", "Nederland"),
        ("FC Volendam", "Nederland"),
        ("Cambuur", "Nederland"),
        ("MVV Maastricht", "Nederland"),
        ("TOP Oss", "Nederland"),
        ("VVV-Venlo", "Nederland"),
        ("Telstar", "Nederland"),
        ("Roda JC", "Nederland"),
        ("Helmond Sport", "Nederland"),
        ("ACV", "Nederland"),
        ("Achilles 1894", "Nederland"),
        ("Asser Boys", "Nederland"),
        ("Drenthina", "Nederland"),
        ("VV Beilen", "Nederland"),
        ("DZOH", "Nederland"),
        ("HOVC", "Nederland"),
        ("WKE '16", "Nederland"),
        ("Germanicus", "Nederland"),
        ("SVBO", "Nederland"),
    ]

    for naam, land in standaard_clubs:
        bestaande_club = Club.query.filter_by(naam=naam).first()
        if not bestaande_club:
            db.session.add(Club(naam=naam, land=land))

    db.session.commit()


def seed_admin():
    from .models import User

    admin_email = "admin@voetbalbase.nl"
    admin_password = "Admin123!"

    bestaande_admin = User.query.filter_by(email=admin_email).first()
    if not bestaande_admin:
        hashed = bcrypt.hashpw(admin_password.encode("utf-8"), bcrypt.gensalt())
        admin = User(
            email=admin_email,
            password_hash=hashed,
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()
        seed_clubs()
        seed_admin()

    return app