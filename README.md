# 🎮 Hangman Game (PTUA17 Final Project)

This is a web-based Hangman game built using **FastAPI**, **Jinja2 templates**, and **MongoDB**. It supports user registration, login, session management, round/game statistics, and visual hangman display.
Project is dockerized with option to reload files and easily access log files

---

## 🚀 Features

- 🔐 Email & password login with hashed passwords (bcrypt)
- 🧠 Dynamic Hangman words loading from MongoDB
- 📊 Tracks game and round statistics per user
- 💾 GameStats persisted to MongoDB (on logout)
- 🧩 Visual hangman drawing
- 🎨 Clean Bootstrap UI with dark theme
- 🧼 Session-based user handling (no query parameters)
- 🧾 Extended logging with possibility to configure different loggers by module

---

## 📁 Project Structure

```
.
├── app/
│	├── hangman.py             # Game logic (HangmanGame, GameStats, RoundSta
│	├── app.py                 # Main FastAPI app with routes
│   ├── words.py               # Word list (loaded into DB on startup)
│	├── visuals.py             # Hangman visual ASCII art
│   ├── logger.py			   # Logging logic
│   ├── logger_conf.json       # Logging config
│	├── unit_tests.py      	   # Unit Tests
│   └── requirements.txt       # Dependencies
├── templates/             	   # Jinja2 templates
│   ├── signin.html
│   ├── register.html
│   ├── success.html
│   └── game.html
├── main/             	   	   # app/ snapshot for reloading files
├── Dockerfile				   # Docker build file for hangman:PTUA17
├── docker-compose.yml    	   # Docker-compose file for Hangman and MongoDB
```
---

##  Build and start with Docker Compose

### 1. Clone the repo

```
git clone git@github.com:LukasZal/Hangman-Game-PTUA17-final-project.git
```

### 2. Build and start with Docker Compose

```
cd Hangman-Game-PTUA17-final-project
docker compose up --build -d
```

### 3. Check running containers

Make sure hangman and mongo-db is running

```
docker ps -a
```

### 4. Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)