from flask import Flask, render_template, request

from model import get_results

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/results", methods=['GET', 'POST'])
def results():
    rgb_val = request.form.get('rgb')
    color_result = get_results(rgb_val)
    return render_template("results.html", rgb_val=rgb_val, color_result=color_result)

if __name__ == "__main__":
    app.run(debug=True, port=8080)