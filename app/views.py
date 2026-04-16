from functools import wraps
import bcrypt

from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from . import db
from .models import User, Speler, Club, Contract
from .forms import RegisterForm, LoginForm, UserForm, SpelerForm, ClubForm, ContractForm

bp = Blueprint("main", __name__)

POSITIES = [
    "Doelman",
    "Centrale verdediger",
    "Linker verdediger",
    "Rechter verdediger",
    "Wingback links",
    "Wingback rechts",
    "Verdedigende middenvelder",
    "Centrale middenvelder",
    "Aanvallende middenvelder",
    "Linksbuiten",
    "Rechtsbuiten",
    "Spits",
    "Schaduwspits",
]


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


def is_ingelogd():
    return get_current_user() is not None


def is_admin():
    user = get_current_user()
    return user is not None and user.is_admin


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not is_ingelogd():
            flash("Log eerst in.", "warning")
            return redirect(url_for("main.login"))
        return view_func(*args, **kwargs)
    return wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not is_ingelogd():
            flash("Log eerst in als admin.", "warning")
            return redirect(url_for("main.admin_login"))
        if not is_admin():
            flash("Geen toegang.", "danger")
            return redirect(url_for("main.home"))
        return view_func(*args, **kwargs)
    return wrapped_view


@bp.app_context_processor
def inject_user():
    return {
        "current_user": get_current_user(),
        "is_admin_user": is_admin(),
        "ingelogd": is_ingelogd(),
    }


@bp.route("/")
def landing():
    if is_ingelogd():
        if is_admin():
            return redirect(url_for("main.admin_dashboard"))
        return redirect(url_for("main.home"))
    return render_template("landing.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if is_ingelogd():
        if is_admin():
            return redirect(url_for("main.admin_dashboard"))
        return redirect(url_for("main.home"))

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        bestaand = User.query.filter_by(email=email).first()

        if bestaand:
            flash("Dit e-mailadres bestaat al.", "warning")
            return redirect(url_for("main.register"))

        hashed = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt())

        user = User(
            email=email,
            password_hash=hashed,
            is_admin=False
        )

        db.session.add(user)
        db.session.commit()

        flash("Registratie gelukt. Je kunt nu inloggen.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if is_ingelogd():
        if is_admin():
            return redirect(url_for("main.admin_dashboard"))
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.checkpw(form.password.data.encode("utf-8"), user.password_hash):
            flash("Ongeldige inloggegevens.", "danger")
            return redirect(url_for("main.login"))

        if user.is_admin:
            flash("Gebruik de admin login voor dit account.", "warning")
            return redirect(url_for("main.admin_login"))

        session.clear()
        session["user_id"] = user.id

        flash("Je bent ingelogd.", "success")
        return redirect(url_for("main.home"))

    return render_template("login.html", form=form)


@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if is_admin():
        return redirect(url_for("main.admin_dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.checkpw(form.password.data.encode("utf-8"), user.password_hash):
            flash("Ongeldige inloggegevens.", "danger")
            return redirect(url_for("main.admin_login"))

        if not user.is_admin:
            flash("Dit account heeft geen adminrechten.", "danger")
            return redirect(url_for("main.admin_login"))

        session.clear()
        session["user_id"] = user.id

        flash("Admin login geslaagd.", "success")
        return redirect(url_for("main.admin_dashboard"))

    return render_template("admin_login.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    flash("Je bent uitgelogd.", "info")
    return redirect(url_for("main.landing"))


@bp.route("/home")
@login_required
def home():
    zoekterm = request.args.get("q", "").strip()
    nationaliteit = request.args.get("nationaliteit", "").strip()

    query = Speler.query

    if zoekterm:
        query = query.filter(Speler.naam.ilike(f"%{zoekterm}%"))

    if nationaliteit:
        query = query.filter(Speler.nationaliteit.ilike(f"%{nationaliteit}%"))

    spelers = query.order_by(Speler.naam.asc()).all()
    return render_template(
        "home.html",
        spelers=spelers,
        zoekterm=zoekterm,
        nationaliteit=nationaliteit
    )


@bp.route("/spelers")
@login_required
def spelers():
    zoekterm = request.args.get("q", "").strip()
    nationaliteit = request.args.get("nationaliteit", "").strip()

    query = Speler.query

    if zoekterm:
        query = query.filter(Speler.naam.ilike(f"%{zoekterm}%"))

    if nationaliteit:
        query = query.filter(Speler.nationaliteit.ilike(f"%{nationaliteit}%"))

    spelers = query.order_by(Speler.naam.asc()).all()
    return render_template(
        "spelers.html",
        spelers=spelers,
        zoekterm=zoekterm,
        nationaliteit=nationaliteit
    )


@bp.route("/spelers/<int:speler_id>")
@login_required
def speler_detail(speler_id):
    speler = Speler.query.get_or_404(speler_id)
    return render_template("speler_detail.html", speler=speler)


@bp.route("/clubs")
@login_required
def clubs():
    clubs = Club.query.order_by(Club.naam.asc()).all()
    return render_template("clubs.html", clubs=clubs)


@bp.route("/contracten")
@login_required
def contracten():
    contracten = Contract.query.order_by(Contract.id.desc()).all()
    return render_template("contracten.html", contracten=contracten)


@bp.route("/admin")
@admin_required
def admin_dashboard():
    aantal_users = User.query.count()
    aantal_spelers = Speler.query.count()
    aantal_clubs = Club.query.count()
    aantal_contracten = Contract.query.count()

    return render_template(
        "admin_dashboard.html",
        aantal_users=aantal_users,
        aantal_spelers=aantal_spelers,
        aantal_clubs=aantal_clubs,
        aantal_contracten=aantal_contracten
    )


@bp.route("/admin/users")
@admin_required
def admin_users():
    users = User.query.order_by(User.email.asc()).all()
    return render_template("admin_users.html", users=users)


@bp.route("/admin/users/nieuw", methods=["GET", "POST"])
@admin_required
def admin_user_nieuw():
    form = UserForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        bestaand = User.query.filter_by(email=email).first()

        if bestaand:
            flash("Dit e-mailadres bestaat al.", "warning")
            return redirect(url_for("main.admin_user_nieuw"))

        if not form.password.data:
            flash("Wachtwoord is verplicht bij een nieuwe gebruiker.", "danger")
            return redirect(url_for("main.admin_user_nieuw"))

        hashed = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt())

        user = User(
            email=email,
            password_hash=hashed,
            is_admin=form.is_admin.data
        )

        db.session.add(user)
        db.session.commit()

        flash("Gebruiker aangemaakt.", "success")
        return redirect(url_for("main.admin_users"))

    return render_template("admin_user_form.html", form=form, titel="Nieuwe gebruiker")


@bp.route("/admin/users/bewerken/<int:user_id>", methods=["GET", "POST"])
@admin_required
def admin_user_bewerken(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm()

    if request.method == "GET":
        form.email.data = user.email
        form.is_admin.data = user.is_admin

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        bestaand = User.query.filter_by(email=email).first()

        if bestaand and bestaand.id != user.id:
            flash("Dit e-mailadres bestaat al.", "warning")
            return redirect(url_for("main.admin_user_bewerken", user_id=user.id))

        user.email = email
        user.is_admin = form.is_admin.data

        if form.password.data:
            user.password_hash = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt())

        db.session.commit()
        flash("Gebruiker bijgewerkt.", "success")
        return redirect(url_for("main.admin_users"))

    return render_template("admin_user_form.html", form=form, titel="Gebruiker bewerken", user=user)


@bp.route("/admin/users/verwijderen/<int:user_id>", methods=["POST"])
@admin_required
def admin_user_verwijderen(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == session.get("user_id"):
        flash("Je kunt jezelf niet verwijderen.", "danger")
        return redirect(url_for("main.admin_users"))

    db.session.delete(user)
    db.session.commit()

    flash("Gebruiker verwijderd.", "success")
    return redirect(url_for("main.admin_users"))


@bp.route("/admin/spelers")
@admin_required
def admin_spelers():
    zoekterm = request.args.get("q", "").strip()
    nationaliteit = request.args.get("nationaliteit", "").strip()

    query = Speler.query

    if zoekterm:
        query = query.filter(Speler.naam.ilike(f"%{zoekterm}%"))

    if nationaliteit:
        query = query.filter(Speler.nationaliteit.ilike(f"%{nationaliteit}%"))

    spelers = query.order_by(Speler.naam.asc()).all()

    return render_template(
        "admin_spelers.html",
        spelers=spelers,
        zoekterm=zoekterm,
        nationaliteit=nationaliteit
    )


@bp.route("/admin/spelers/nieuw", methods=["GET", "POST"])
@admin_required
def admin_speler_nieuw():
    form = SpelerForm()

    if form.validate_on_submit():
        speler = Speler(
            naam=form.naam.data.strip(),
            leeftijd=form.leeftijd.data,
            nationaliteit=form.nationaliteit.data.strip()
        )

        db.session.add(speler)
        db.session.commit()

        flash("Speler toegevoegd.", "success")
        return redirect(url_for("main.admin_spelers"))

    return render_template("admin_speler_form.html", form=form, titel="Nieuwe speler")


@bp.route("/admin/spelers/bewerken/<int:speler_id>", methods=["GET", "POST"])
@admin_required
def admin_speler_bewerken(speler_id):
    speler = Speler.query.get_or_404(speler_id)
    form = SpelerForm()

    if request.method == "GET":
        form.naam.data = speler.naam
        form.leeftijd.data = speler.leeftijd
        form.nationaliteit.data = speler.nationaliteit

    if form.validate_on_submit():
        speler.naam = form.naam.data.strip()
        speler.leeftijd = form.leeftijd.data
        speler.nationaliteit = form.nationaliteit.data.strip()

        db.session.commit()

        flash("Speler bijgewerkt.", "success")
        return redirect(url_for("main.admin_spelers"))

    return render_template("admin_speler_form.html", form=form, titel="Speler bewerken", speler=speler)


@bp.route("/admin/spelers/verwijderen/<int:speler_id>", methods=["POST"])
@admin_required
def admin_speler_verwijderen(speler_id):
    speler = Speler.query.get_or_404(speler_id)
    db.session.delete(speler)
    db.session.commit()

    flash("Speler verwijderd.", "success")
    return redirect(url_for("main.admin_spelers"))


@bp.route("/admin/clubs")
@admin_required
def admin_clubs():
    clubs = Club.query.order_by(Club.naam.asc()).all()
    return render_template("admin_clubs.html", clubs=clubs)


@bp.route("/admin/clubs/nieuw", methods=["GET", "POST"])
@admin_required
def admin_club_nieuw():
    form = ClubForm()

    if form.validate_on_submit():
        naam = form.naam.data.strip()
        bestaand = Club.query.filter_by(naam=naam).first()

        if bestaand:
            flash("Deze club bestaat al.", "warning")
            return redirect(url_for("main.admin_club_nieuw"))

        club = Club(
            naam=naam,
            land=form.land.data.strip()
        )

        db.session.add(club)
        db.session.commit()

        flash("Club toegevoegd.", "success")
        return redirect(url_for("main.admin_clubs"))

    return render_template("admin_club_form.html", form=form, titel="Nieuwe club")


@bp.route("/admin/clubs/bewerken/<int:club_id>", methods=["GET", "POST"])
@admin_required
def admin_club_bewerken(club_id):
    club = Club.query.get_or_404(club_id)
    form = ClubForm()

    if request.method == "GET":
        form.naam.data = club.naam
        form.land.data = club.land

    if form.validate_on_submit():
        naam = form.naam.data.strip()
        bestaand = Club.query.filter_by(naam=naam).first()

        if bestaand and bestaand.id != club.id:
            flash("Deze club bestaat al.", "warning")
            return redirect(url_for("main.admin_club_bewerken", club_id=club.id))

        club.naam = naam
        club.land = form.land.data.strip()

        db.session.commit()

        flash("Club bijgewerkt.", "success")
        return redirect(url_for("main.admin_clubs"))

    return render_template("admin_club_form.html", form=form, titel="Club bewerken", club=club)


@bp.route("/admin/clubs/verwijderen/<int:club_id>", methods=["POST"])
@admin_required
def admin_club_verwijderen(club_id):
    club = Club.query.get_or_404(club_id)
    db.session.delete(club)
    db.session.commit()

    flash("Club verwijderd.", "success")
    return redirect(url_for("main.admin_clubs"))


def vul_contract_choices(form):
    form.speler_id.choices = [(speler.id, speler.naam) for speler in Speler.query.order_by(Speler.naam.asc()).all()]
    form.club_id.choices = [(club.id, club.naam) for club in Club.query.order_by(Club.naam.asc()).all()]


@bp.route("/admin/contracten")
@admin_required
def admin_contracten():
    contracten = Contract.query.order_by(Contract.id.desc()).all()
    return render_template("admin_contracten.html", contracten=contracten)


@bp.route("/admin/contracten/nieuw", methods=["GET", "POST"])
@admin_required
def admin_contract_nieuw():
    form = ContractForm()
    vul_contract_choices(form)

    if form.validate_on_submit():
        contract = Contract(
            speler_id=form.speler_id.data,
            club_id=form.club_id.data,
            positie=form.positie.data.strip(),
            rugnummer=form.rugnummer.data
        )

        db.session.add(contract)
        db.session.commit()

        flash("Contract toegevoegd.", "success")
        return redirect(url_for("main.admin_contracten"))

    return render_template("admin_contract_form.html", form=form, titel="Nieuw contract")


@bp.route("/admin/contracten/bewerken/<int:contract_id>", methods=["GET", "POST"])
@admin_required
def admin_contract_bewerken(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    form = ContractForm()
    vul_contract_choices(form)

    if request.method == "GET":
        form.speler_id.data = contract.speler_id
        form.club_id.data = contract.club_id
        form.positie.data = contract.positie
        form.rugnummer.data = contract.rugnummer

    if form.validate_on_submit():
        contract.speler_id = form.speler_id.data
        contract.club_id = form.club_id.data
        contract.positie = form.positie.data.strip()
        contract.rugnummer = form.rugnummer.data

        db.session.commit()

        flash("Contract bijgewerkt.", "success")
        return redirect(url_for("main.admin_contracten"))

    return render_template("admin_contract_form.html", form=form, titel="Contract bewerken", contract=contract)
    

@bp.route("/admin/contracten/verwijderen/<int:contract_id>", methods=["POST"])
@admin_required
def admin_contract_verwijderen(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    db.session.delete(contract)
    db.session.commit()

    flash("Contract verwijderd.", "success")
    return redirect(url_for("main.admin_contracten"))