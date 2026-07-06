def sheet_weight(thickness, length, width, density=7.854):
    return thickness * length * width * density / 1000000


def material_cost(weight, rm_rate):
    return weight * rm_rate


def net_rm_cost(weight, rm_rate, scrap_rate, part_weight):
    material = weight * rm_rate
    scrap_weight = weight - part_weight
    scrap_value = scrap_weight * scrap_rate
    return material - scrap_value
def sheet_weight(thickness, length, width, density=7.854):
    return thickness * length * width * density / 1000000