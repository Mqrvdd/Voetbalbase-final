# ⚽ VoetbalBase

Een voetbalbase voor beheer van spelers, clubs en contracten. Registreer met je email, log in, en beheer je voetbaldata!

---

## ✨ Functies

• Gebruikersaccounts: Registreer met email en wachtwoord

• Spelers Management: Toevoegen, bewerken en verwijderen van voetbalspelers

• Clubs Management: Beheer clubs met automatisch ingevulde standaard clubs

• Contracten System: Koppel spelers aan clubs met positie en rugnummer

• Geavanceerd Zoeken: Zoek spelers op naam en filter op nationaliteit

• Dashboard: Overzicht van alle spelers, clubs en contracten

• Admin Interface: Volledige beheerfunctionaliteit voor administrators

• Beveiliging: Wachtwoorden gehasht met bcrypt, login-required bescherming

• Responsief Design: Werkt op desktop, tablet en mobiel

---

## 📋 Vereisten

• Python 3.8 of hoger
• pip (Python package manager)

---

## 🚀 Installatie

### Stap 1: Clone of download het project

```
cd Voetbalbase
```

### Stap 2: Maak een virtuele omgeving (aanbevolen)

```
python -m venv venv
```

### Stap 3: Activeer de virtuele omgeving

Op Windows:
```
venv\Scripts\activate
```

Op macOS/Linux:
```
source venv/bin/activate
```

### Stap 4: Installeer de vereiste packages

```
pip install -r requirements.txt
```

### Stap 5: Voer de applicatie uit

```
python app.py
```

De applicatie start nu op `http://127.0.0.1:5000`

### Stap 6: Open in je browser

Open je webbrowser en ga naar: [http://127.0.0.1:5000](http://127.0.0.1:5000/)

---

## 🎮 Hoe Gebruik Je Het

### Registratie & Login

1. Nieuw account: Klik op "Registreer" en vul je email en wachtwoord in
2. Login: Log in met je email en wachtwoord
3. Dashboard: Je bent nu ingelogd en ziet het overzicht

### Spelers Beheren

1. Ga naar Spelers pagina
2. Voeg speler toe: Klik op "+ Nieuwe speler" en vul de gegevens in
3. Bewerk speler: Klik het potlood-icoon naast een speler
4. Verwijder speler: Klik het prullenbak-icoon
5. Zoek spelers: Gebruik de zoekbalk om spelers te filteren

### Clubs Beheren

1. Ga naar Clubs pagina
2. Voeg club toe: Klik op "+ Nieuwe club" en vul naam en land in
3. Bewerk club: Klik het potlood-icoon
4. Verwijder club: Klik het prullenbak-icoon
5. Standaard clubs: 50+ standaard clubs zijn al vooraf ingeladen

### Contracten Beheren

1. Ga naar Contracten pagina
2. Voeg contract toe: Selecteer een speler, club, positie en rugnummer
3. Bewerk contract: Klik het potlood-icoon
4. Verwijder contract: Klik het prullenbak-icoon

---

## ⚙️ Configuratie

Standaardwaarden:

• Database: SQLite (database.db)
• Server poort: 5000
• Debug modus: Aan (development)
• Standaard clubs: 50+ Nederlandse clubs

---

## 🛠️ Technologie Stack

• Backend: Python / Flask
• Database: SQLite + SQLAlchemy ORM
• Frontend: Bootstrap 5 + Jinja2 Templates
• Authenticatie: Flask-WTF + bcrypt
• Database Migration: Flask-Migrate

Dependencies:

• Flask
• Flask-SQLAlchemy
• Flask-WTF
• Flask-Migrate
• bcrypt
• WTForms
• email-validator

---

## 🔒 Veiligheid

• Wachtwoorden worden beveiligd opgeslagen (hashed met bcrypt)
• Sessies zijn beveiligd met geheime sleutels
• SQL injection bescherming via SQLAlchemy
• CSRF bescherming ingebouwd

---

## 📝 Licentie

Dit project is gelicentieerd onder de MIT Licentie.

---

## 📊 Database

• SQLite (`database.db`)
• Wordt automatisch aangemaakt
• Seed met clubs bij eerste start

---

## Inloggegevens voor testen

### Standaard Admin Account

E-mail: `admin@voetbalbase.nl`

Wachtwoord: `Admin123!`

(Je mag natuurlijk ook je eigen account aanmaken)

---

Veel plezier met het beheren van je voetbaldata! ⚽

Laatst geupdate: April 2026

---

## Structuur

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
│
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

---

## Licentie

MIT License
