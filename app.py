from flask import Flask, render_template, request
from calculator import sheet_weight

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculator():

    weight = 0
    input_weight = 0
    scrap_weight = 0
    rm_cost = 0
    scrap_cost = 0
    rmc = 0

    material = ""

    thickness = ""
    length = ""
    width = ""
    blanks_per_sheet = ""
    part_weight = ""
    rm_rate = ""
    scrap_rate = ""

    if request.method == "POST":

        material = request.form["material"]

        thickness = float(request.form["thickness"])
        length = float(request.form["length"])
        width = float(request.form["width"])

        blanks_per_sheet = float(request.form["blanks_per_sheet"])
        part_weight = float(request.form["part_weight"])

        rm_rate = float(request.form["rm_rate"])
        scrap_rate = float(request.form["scrap_rate"])

        # Select density
        if material == "CR":
            density = 7.85
        elif material == "HR":
            density = 7.85
        elif material == "AL":
            density = 2.70
        else:
            density = 7.85

        # Sheet weight
        weight = round(sheet_weight(thickness, length, width, density), 3)

        # Input weight per part
        input_weight = round(weight / blanks_per_sheet, 3)

        # Scrap weight
        scrap_weight = round(input_weight - part_weight, 3)

        # Cost calculations
        rm_cost = input_weight * rm_rate
        scrap_cost = scrap_weight * scrap_rate

        # Final RMC
        rmc = round(rm_cost - scrap_cost, 2)

    return render_template(
        "calculator.html",
        material=material,
        weight=weight,
        input_weight=input_weight,
        scrap_weight=scrap_weight,
        rm_cost=rm_cost,
        scrap_cost=scrap_cost,
        rmc=rmc,
        thickness=thickness,
        length=length,
        width=width,
        blanks_per_sheet=blanks_per_sheet,
        part_weight=part_weight,
        rm_rate=rm_rate,
        scrap_rate=scrap_rate
    )
if __name__ == "__main__":
    app.run(debug=True)