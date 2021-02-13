import os
from flask import url_for
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///xmeme.db")


@app.route("/", methods = ['GET', 'POST'])
def index():
    return redirect("/meme")


@app.route("/memes", methods=['GET', 'POST'])
def rest():
    if request.method == "GET":
        ide = request.args.get("id", None)
        if not ide:
            rows = db.execute("SELECT * FROM xmeme ORDER BY user_id LIMIT 100 ")
            if not rows:
                print("yo")
                return jsonify(reversed(rows))
            else:
                print("No")
                return jsonify(reversed(rows))
        elif str(ide).isdigit():
            print(f"got name {ide}")
            rows = db.execute("SELECT * FROM xmeme WHERE user_id = :values", values=int(ide))
            if not rows:
                return "NO MEME Found"
            else:
                print("fo")
                return jsonify(reversed(rows))
    else:
        username = request.args.get("username")
        caption = request.args.get("caption")
        url = request.args.get("url")
        if not username or not caption or not url:
            return "Please provide all args"
        else:
            db.execute("INSERT INTO xmeme (username, caption, url) VALUES (:username, :caption, :url)", username = username, caption = caption, url = url)
            rows = db.execute("SELECT user_id FROM xmeme WHERE url = :values", values=url)
            return jsonify(rows)


@app.route("/meme", methods = ['GET' , 'POST'])
def frontend():
    if request.method == "GET":

        rows = reversed(db.execute("SELECT * FROM xmeme LIMIT 100"))
        if not rows:
            string = "No one has posted ):, Dont worry Be the first one to post"
            return render_template("index.html", string = string)
        else:
            return render_template("index.html", row = rows)
    else:
        if not request.form.get("username") or not request.form.get("caption") or not request.form.get("url"):
            return "Please provide your name"
        else:
            db.execute("INSERT INTO xmeme (username, caption, url) VALUES (:username, :caption, :url)", username = str(request.form.get("username")), caption = str(request.form.get("caption")), url = request.form.get("url"))
            rows = reversed(db.execute("SELECT * FROM xmeme LIMIT 100"))
            return render_template("/index.html", row = rows)


@app.route("/editurl", methods=["POST"])
def edit():
    if request.method == "POST":
        ide = request.form.get("id")
        url = request.form.get("url")
        if not url :
            return "Please update any atleast one"
        else:
            db.execute("UPDATE xmeme SET url = :values WHERE user_id = :ide", ide = ide, values = url)
        rows = reversed(db.execute("SELECT * FROM xmeme LIMIT 100"))
        return render_template("/index.html", row = rows)

@app.route("/editcaption", methods=["POST"])
def editu():
    if request.method == "POST":
        ide = request.form.get("id")
        caption = request.form.get("caption")
        if not caption:
            return "Please update any atleast one"
        else:
            db.execute("UPDATE xmeme SET caption = :values WHERE user_id = :ide", ide = ide, values = caption)
        rows = reversed(db.execute("SELECT * FROM xmeme LIMIT 100"))
        return render_template("/index.html", row = rows)


if __name__ == "__main__":
    app.run(debug = True)