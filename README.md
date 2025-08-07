# 🎮 Hangman Game (PTUA17 Final Project)

This is a web-based Hangman game built using **FastAPI**, **Jinja2 templates**, and **MongoDB**. It supports user registration, login, session management, round/game statistics, and visual hangman display.

---

## 🚀 Features

- 🔐 Email & password login with hashed passwords (bcrypt)
- 🧠 Dynamic Hangman word loaded from MongoDB
- 📊 Tracks game and round statistics per user
- 💾 GameStats persisted to MongoDB (on logout)
- 🧩 Visual hangman drawing
- 🎨 Clean Bootstrap UI with dark theme
- 🧼 Session-based user handling (no query parameters)

---

## 📁 Project Structure

```
.
├── app.py                 # Main FastAPI app with routes
├── hangman.py             # Game logic (HangmanGame, GameStats, RoundStats)
├── words.py               # Word list (loaded into DB on startup)
├── visuals.py             # Hangman visual ASCII art
├── templates/             # Jinja2 templates
│   ├── signin.html
│   ├── register.html
│   ├── success.html
│   └── game.html
├── requirements.txt       # Dependencies
├── unit_tests.py      	   # Unit Tests
```

---

## 🧪 Running the App

### 1. Clone the repo

```bash
git clone https://github.com/yourname/hangman-app.git
cd hangman-app
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Start MongoDB

Make sure MongoDB is running and accessible at:

```
mongodb://127.0.0.1:27017
```

> You can change this address in `app.py` if needed.

### 4. Run the app

```bash
python app.py
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)


## 👤 Author

Created by **Lukas** | CodeAcademy | 2025