from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/results", methods=['GET', 'POST'])
def results():
    rgb_val = request.form.get('rgb')
    return render_template("results.html", rgb_val=rgb_val)

if __name__ == "__main__":
    app.run(debug=True, port=8080)