import math
from flask import Flask, render_template, request
from calculator import (
    sheet_weight, circle_weight,
    nest_rectangular, nest_circular,
    nesting_efficiency, material_cost, net_rm_cost
)

app = Flask(__name__)

SHEET_SIZES = {
    "2500x1250": (2500, 1250),
    "2440x1220": (2440, 1220),
    "3000x1500": (3000, 1500),
    "2000x1000": (2000, 1000),
    "1500x1250": (1500, 1250),
}

DENSITY = {
    "CR": 7.85,
    "HR": 7.85,
    "AL": 2.70,
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculator():

    context = {
        "material": "", "sheet_size": "", "thickness": "",
        "blank_shape": "rect", "part_length": "", "part_width": "", "part_radius": "",
        "rm_rate": "", "scrap_rate": "",
        "weight": 0, "blank_weight": 0, "blanks_per_sheet": 0,
        "orientation": "", "nesting_eff": 0,
        "input_weight": 0, "scrap_weight": 0,
        "rm_cost": 0, "scrap_cost": 0, "rmc": 0,
        "error": None,
    }

    if request.method == "POST":
        try:
            material = request.form["material"]
            sheet_size = request.form["sheet_size"]
            thickness = float(request.form["thickness"])
            blank_shape = request.form["blank_shape"]
            rm_rate = float(request.form["rm_rate"])
            scrap_rate = float(request.form["scrap_rate"])

            context.update({
                "material": material, "sheet_size": sheet_size, "thickness": thickness,
                "blank_shape": blank_shape, "rm_rate": rm_rate, "scrap_rate": scrap_rate,
            })

            if sheet_size not in SHEET_SIZES:
                raise ValueError("Please select a valid standard sheet size.")

            length, width = SHEET_SIZES[sheet_size]
            sheet_area = length * width
            density = DENSITY.get(material, 7.85)

            # Full sheet weight
            weight = round(sheet_weight(thickness, length, width, density), 3)

            if blank_shape == "rect":
                part_length = float(request.form["part_length"])
                part_width = float(request.form["part_width"])
                context["part_length"] = part_length
                context["part_width"] = part_width

                if part_length <= 0 or part_width <= 0:
                    raise ValueError("Part length and width must be greater than 0.")

                blank_area = part_length * part_width
                blank_weight = round(sheet_weight(thickness, part_length, part_width, density), 5)
                blanks_per_sheet, orientation = nest_rectangular(length, width, part_length, part_width)

            elif blank_shape == "circle":
                part_radius = float(request.form["part_radius"])
                context["part_radius"] = part_radius

                if part_radius <= 0:
                    raise ValueError("Radius must be greater than 0.")

                diameter = part_radius * 2
                blank_area = math.pi * (part_radius ** 2)
                blank_weight = round(circle_weight(thickness, part_radius, density), 5)
                blanks_per_sheet = nest_circular(length, width, diameter)
                orientation = "N/A"

            else:
                raise ValueError("Invalid blank shape selected.")

            if blanks_per_sheet <= 0:
                raise ValueError(
                    "The part is too large to fit on the selected sheet even once. "
                    "Try a bigger standard sheet size or double-check your dimensions."
                )

            nesting_eff = nesting_efficiency(blanks_per_sheet, blank_area, sheet_area)

            input_weight = round(weight / blanks_per_sheet, 5)
            scrap_weight = round(input_weight - blank_weight, 5)

            rm_cost = round(material_cost(input_weight, rm_rate), 2)
            rmc = round(net_rm_cost(input_weight, rm_rate, scrap_rate, blank_weight), 2)
            scrap_cost = round(rm_cost - rmc, 2)

            context.update({
                "weight": weight,
                "blank_weight": blank_weight,
                "blanks_per_sheet": blanks_per_sheet,
                "orientation": orientation,
                "nesting_eff": nesting_eff,
                "input_weight": input_weight,
                "scrap_weight": scrap_weight,
                "rm_cost": rm_cost,
                "scrap_cost": scrap_cost,
                "rmc": rmc,
            })

        except KeyError:
            context["error"] = "Please fill in all required fields."
        except ValueError as e:
            context["error"] = str(e)

    return render_template("calculator.html", **context)


if __name__ == "__main__":
    app.run(debug=True)