from flask import Flask, render_template, request
from calculator import sheet_weight

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculator():

    weight = None

    if request.method == "POST":

        thickness = float(request.form["thickness"])
        length = float(request.form["length"])
        width = float(request.form["width"])

        weight = round(sheet_weight(thickness, length, width), 3)

    return render_template("calculator.html", weight=weight)


if __name__ == "__main__":
    app.run(debug=True)