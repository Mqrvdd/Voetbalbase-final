# ⚽ VoetbalBase

Een voetbalbase voor beheer van spelers, clubs en contracten. Registreer met je e-mail, log in en beheer eenvoudig je voetbaldata.

---

## ✨ Functies

* Gebruikersaccounts: registreer met e-mail en wachtwoord
* Spelersmanagement: toevoegen, bewerken en verwijderen van spelers
* Clubsmanagement: beheer clubs met automatisch ingevulde standaardclubs
* Contractensysteem: koppel spelers aan clubs met positie en rugnummer
* Geavanceerd zoeken: zoek spelers op naam en filter op nationaliteit
* Dashboard: overzicht van spelers, clubs en contracten
* Admin interface: volledige beheerfunctionaliteit voor administrators
* Beveiliging: wachtwoorden gehasht met bcrypt en login-protectie
* Responsief design: werkt op desktop, tablet en mobiel

---

## 📋 Vereisten

* Python 3.8 of hoger
* pip (Python package manager)

---

## 🚀 Installatie

### 1. Clone of download het project

```bash
cd Voetbalbase
```

### 2. Maak een virtuele omgeving (aanbevolen)

```bash
python -m venv venv
```

### 3. Activeer de virtuele omgeving

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### 4. Installeer de vereiste packages

```bash
pip install -r requirements.txt
```

### 5. Start de applicatie

```bash
python app.py
```

De applicatie draait op: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🎮 Gebruik

### Registratie & Login

1. Klik op **Registreer** en maak een account
2. Log in met je gegevens
3. Je komt op het dashboard

### Spelers beheren

* Ga naar de spelerspagina
* Voeg spelers toe via **+ Nieuwe speler**
* Bewerken via het potlood-icoon
* Verwijderen via het prullenbak-icoon
* Gebruik de zoekbalk om te filteren

### Clubs beheren

* Ga naar de clubspagina
* Voeg clubs toe met naam en land
* Bewerk of verwijder bestaande clubs
* 50+ standaardclubs zijn vooraf geladen

### Contracten beheren

* Ga naar contracten
* Koppel speler aan club met positie en rugnummer
* Bewerken/verwijderen via iconen

---

## ⚙️ Configuratie

* Database: SQLite (`database.db`)
* Serverpoort: 5000
* Debugmodus: aan (development)
* Standaardclubs: 50+ Nederlandse clubs

---

## 🛠️ Technologie Stack

* Backend: Python / Flask
* Database: SQLite + SQLAlchemy
* Frontend: Bootstrap 5 + Jinja2
* Authenticatie: Flask-WTF + bcrypt
* Migraties: Flask-Migrate

### Dependencies

* Flask
* Flask-SQLAlchemy
* Flask-WTF
* Flask-Migrate
* bcrypt
* WTForms
* email-validator

---

## 🔒 Veiligheid

* Wachtwoorden worden gehasht met bcrypt
* Sessies beveiligd met geheime sleutels
* SQL-injection bescherming via SQLAlchemy
* CSRF-bescherming ingebouwd

---

## 📊 Database

* SQLite (`database.db`)
* Wordt automatisch aangemaakt
* Seed met clubs bij eerste start

---

## 🔑 Testgegevens

**Admin account**

* E-mail: `admin@voetbalbase.nl`
* Wachtwoord: `Admin123!`

Je kunt ook zelf een account aanmaken.

---

## 📁 Projectstructuur

```
VoetbalBase/
│
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── landing.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── admin_login.html
│   │   ├── home.html
│   │   ├── spelers.html
│   │   ├── speler_detail.html
│   │   ├── clubs.html
│   │   ├── contracten.html
│   │   ├── admin_dashboard.html
│   │   ├── admin_users.html
│   │   ├── admin_user_form.html
│   │   ├── admin_spelers.html
│   │   ├── admin_speler_form.html
│   │   ├── admin_clubs.html
│   │   ├── admin_club_form.html
│   │   ├── admin_contracten.html
│   │   └── admin_contract_form.html
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   └── views.py
│
├── app.py
├── config.py
├── database.db
├── requirements.txt
└── README.md
```

---

## 📝 Licentie

MIT License

---

*Laatst geüpdatet: april 2026*
