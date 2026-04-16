from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User {self.email}>"


class Speler(db.Model):
    __tablename__ = "spelers"

    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(100), nullable=False)
    leeftijd = db.Column(db.Integer, nullable=False)
    nationaliteit = db.Column(db.String(100), nullable=False)

    contracten = db.relationship(
        "Contract",
        back_populates="speler",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Speler {self.naam}>"


class Club(db.Model):
    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(100), nullable=False, unique=True)
    land = db.Column(db.String(100), nullable=False)

    contracten = db.relationship(
        "Contract",
        back_populates="club",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Club {self.naam}>"


class Contract(db.Model):
    __tablename__ = "contracten"

    id = db.Column(db.Integer, primary_key=True)
    speler_id = db.Column(db.Integer, db.ForeignKey("spelers.id"), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey("clubs.id"), nullable=False)
    positie = db.Column(db.String(100), nullable=False)
    rugnummer = db.Column(db.Integer, nullable=False)

    speler = db.relationship("Speler", back_populates="contracten")
    club = db.relationship("Club", back_populates="contracten")

    def __repr__(self):
        return f"<Contract {self.speler_id}-{self.club_id}>"