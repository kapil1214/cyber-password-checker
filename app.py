from flask import Flask, render_template, request
import hashlib
import requests

app = Flask(__name__)

def check_password_strength(password):
    length = len(password)

    if length < 6:
        return "Weak"
    elif length < 10:
        return "Medium"
    else:
        return "Strong"

def check_breach(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    hashes = (line.split(":") for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return True
    return False

@app.route("/", methods=["GET","POST"])
def index():
    strength = None
    breached = None

    if request.method == "POST":
        password = request.form["password"]
        strength = check_password_strength(password)
        breached = check_breach(password)

    return render_template("index.html", strength=strength, breached=breached)

if __name__ == "__main__":
    app.run(debug=True)