import math

def sheet_weight(thickness, length, width, density=7.85):
    """Weight of a rectangular piece (sheet OR blank) in kg."""
    return thickness * length * width * density / 1_000_000


def circle_weight(thickness, radius, density=7.85):
    """Weight of a circular blank in kg."""
    return thickness * math.pi * (radius ** 2) * density / 1_000_000


def nest_rectangular(sheet_length, sheet_width, blank_length, blank_width):
    """Grid nesting for rectangular blanks. Tries both orientations, returns the better one."""
    cols_normal = int(sheet_length // blank_length)
    rows_normal = int(sheet_width // blank_width)
    count_normal = cols_normal * rows_normal

    cols_rot = int(sheet_length // blank_width)
    rows_rot = int(sheet_width // blank_length)
    count_rot = cols_rot * rows_rot

    if count_rot > count_normal:
        return count_rot, "Rotated 90°"
    return count_normal, "Normal"


def nest_circular(sheet_length, sheet_width, diameter):
    """Simple square-grid nesting for circular blanks."""
    cols = int(sheet_length // diameter)
    rows = int(sheet_width // diameter)
    return cols * rows


def nesting_efficiency(blanks_per_sheet, blank_area, sheet_area):
    """% of sheet area actually used by blanks."""
    if sheet_area <= 0 or blanks_per_sheet <= 0:
        return 0.0
    return round((blanks_per_sheet * blank_area) / sheet_area * 100, 2)


def material_cost(weight, rm_rate):
    return weight * rm_rate


def net_rm_cost(weight, rm_rate, scrap_rate, part_weight):
    material = weight * rm_rate
    scrap_weight = weight - part_weight
    scrap_value = scrap_weight * scrap_rate
    return material - scrap_value