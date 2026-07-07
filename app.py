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
    sheet_size = ""

    thickness = ""
    blanks_per_sheet = ""
    part_weight = ""
    rm_rate = ""
    scrap_rate = ""

    length = 0
    width = 0

    if request.method == "POST":

        material = request.form["material"]
        sheet_size = request.form["sheet_size"]

        thickness = float(request.form["thickness"])

        # Standard Sheet Sizes
        sheet_sizes = {
            "2500x1250": (2500, 1250),
            "2440x1220": (2440, 1220),
            "3000x1500": (3000, 1500),
            "2000x1000": (2000, 1000),
            "1500x1250": (1500, 1250)
        }

        length, width = sheet_sizes[sheet_size]

        blanks_per_sheet = float(request.form["blanks_per_sheet"])
        part_weight = float(request.form["part_weight"])

        rm_rate = float(request.form["rm_rate"])
        scrap_rate = float(request.form["scrap_rate"])

        # Material Density
        if material == "CR":
            density = 7.85
        elif material == "HR":
            density = 7.85
        elif material == "AL":
            density = 2.70
        else:
            density = 7.85

        # Sheet Weight
        weight = round(sheet_weight(thickness, length, width, density), 3)

        # Input Weight
        input_weight = round(weight / blanks_per_sheet, 3)

        # Scrap Weight
        scrap_weight = round(input_weight - part_weight, 3)

        # Cost Calculations
        rm_cost = round(input_weight * rm_rate, 2)
        scrap_cost = round(scrap_weight * scrap_rate, 2)

        # Final RMC
        rmc = round(rm_cost - scrap_cost, 2)

    return render_template(
        "calculator.html",
        material=material,
        sheet_size=sheet_size,
        weight=weight,
        input_weight=input_weight,
        scrap_weight=scrap_weight,
        rm_cost=rm_cost,
        scrap_cost=scrap_cost,
        rmc=rmc,
        thickness=thickness,
        blanks_per_sheet=blanks_per_sheet,
        part_weight=part_weight,
        rm_rate=rm_rate,
        scrap_rate=scrap_rate
    )


if __name__ == "__main__":
    app.run(debug=True)