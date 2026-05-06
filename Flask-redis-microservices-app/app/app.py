from flask import Flask, request, render_template_string
from redis import Redis

app = Flask(__name__)
r = Redis(host='redis', port=6379)

TEMPLATE = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Mini Forum</title>
</head>
<body>
    <h1>Mini Forum</h1>
    <form method="post">
        <input type="text" name="nick" placeholder="Twój nick" required>
        <input type="text" name="comment" placeholder="Wpisz komentarz" required>
        <button type="submit">Dodaj</button>
    </form>
    <h2>Komentarze:</h2>
    <ul>
        {% for c in comments %}
            <li>{{ c}}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nick = request.form.get("nick")
        comment = request.form.get("comment")
        if nick and comment:
            r.lpush("comments", f"{comment} ~{nick}")

    comments = [c.decode('utf-8') for c in r.lrange("comments", 0, -1)]
    return render_template_string(TEMPLATE, comments=comments)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)