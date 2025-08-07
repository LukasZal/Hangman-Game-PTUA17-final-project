from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import starlette.status as status
import uvicorn
from pymongo import MongoClient
from hangman import HangmanGame, GameStats
from visuals import display_hangman
from words import word_list
import random
import bcrypt


client = MongoClient("mongodb://10.48.7.100:27017")
database = client["HangmanDB"]
users = database["users"]
words = database["words"]


def load_words():
    current_list = list(words.find({}))
    if current_list:
        return [documents["word"] for documents in current_list]
    new_list = [w.upper() for w in word_list]
    words.insert_many([{"word": w} for w in new_list])
    return new_list

wordlist = load_words()

games = {}
stats = {}


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="GD/,##l$1SD14DsR")
templates = Jinja2Templates(directory="templates")


def get_word():
    return random.choice(wordlist)

def get_user_email(request: Request):
    return request.session.get("email")

def save_stats_to_db(email: str):
    current_stats = stats.get(email)
    if current_stats:
        users.update_one({"email": email}, {"$set": {"game_stats": current_stats.game_history()}})


@app.get("/", response_class=HTMLResponse)
def signin(request: Request):
    error = request.query_params.get("x-error")
    success = request.query_params.get("x-success")
    return templates.TemplateResponse("signin.html", {"request": request, "error": error, "success": success})

@app.post("/", response_class=RedirectResponse)
def validate(request: Request, email: str = Form(...), password: str = Form(...)):
    user = users.find_one({"email": email}) 
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        request.session["email"] = email
        request.session["name"] = user.get("name")
        request.session["surname"] = user.get("surname")
        stats[email] = GameStats.user_stat(user["game_stats"])
        return RedirectResponse("/success", status_code=302)
    return RedirectResponse("/?x-error=Wrong+email+or+password", status_code=302)

@app.get("/success", response_class=HTMLResponse)
def success_page(request: Request):
    email = get_user_email(request)
    if not email:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("success.html", {
        "request": request,
        "name": request.session.get("name"),
        "surname": request.session.get("surname")
    })

@app.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    error = request.query_params.get("x-error")
    return templates.TemplateResponse("register.html", {"request": request, "error": error})

@app.post("/register", response_class=RedirectResponse)
def register_post(request: Request, name: str = Form(...), surname: str = Form(...), email: str = Form(...), password: str = Form(...)):
    existing = users.find_one({"email": email})
    if existing:
        return RedirectResponse("/register?x-error=Email+already+registered", status_code=302)
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users.insert_one({
        "name": name,
        "surname": surname,
        "email": email,
        "password": hashed_pw,
        "game_stats": GameStats().game_history()
    })
    return RedirectResponse("/?x-success=Registration+successful,+please+login", status_code=302)

@app.get("/game", response_class=HTMLResponse)
def game_page(request: Request):
    email = get_user_email(request)
    if not email:
        return RedirectResponse("/", status_code=302)

    if email not in games:
        user_stats = stats.setdefault(email, GameStats())
        games[email] = HangmanGame(get_word(), stats=user_stats)

    game = games[email]
    play_again = game.is_over()
    game_over_message = (
        f"Congratulations! You guessed the word: {game.word}" if game.guessed
        else f"Game Over! The word was: {game.word}"
    )if play_again else None

    return templates.TemplateResponse("game.html", {
        "request": request,
        "name": request.session.get("name"),
        "surname": request.session.get("surname"),
        "email": email,
        "tries": game.tries,
        "word_completion": game.word_completion,
        "guessed": game.guessed,
        "guessed_letters": ', '.join(sorted(game.guessed_letters)) if game.guessed_letters else 'None',
        "game_over_message": game_over_message,
        "play_again": play_again,
        "visual": display_hangman(game.tries),
        "messages": game.messages,
        "round_stats": str(game.round_stats),
        "game_stats": str(game.stats)
    })

@app.post("/guess", response_class=RedirectResponse)
def make_guess(request: Request, guess: str = Form(...)):
    email = get_user_email(request)
    if not email or email not in games:
        return RedirectResponse("/", status_code=302)
    game = games[email]
    msg = game.guess_letter(guess)
    game.messages.append(msg)
    return RedirectResponse("/game", status_code=302)

@app.post("/play-again", response_class=RedirectResponse)
def play_again(request: Request):
    email = get_user_email(request)
    if not email:
        return RedirectResponse("/", status_code=302)
    user_stats = stats.setdefault(email, GameStats())
    games[email] = HangmanGame(get_word(), stats=user_stats)
    return RedirectResponse("/game", status_code=302)

@app.post("/exit", response_class=RedirectResponse)
def exit_game(request: Request):
    email = get_user_email(request)
    if email:
        save_stats_to_db(email)
        games.pop(email, None)
        stats.pop(email, None)
    request.session.clear()
    return RedirectResponse("/", status_code=302)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)