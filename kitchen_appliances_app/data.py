"""Static application data for KitchenXCalc."""

APPLIANCES = {
    "Fryer":                   {"icon": "", "input_type": "wl",      "typical_w": 360, "typical_d": 380, "max_area": 0.137, "max_side": 380, "abs_max_area": 0.55, "nozzle": "2–30",  "flow": 2},
    "Fryer with drip board":   {"icon": "", "input_type": "wl_drip", "typical_w": 360, "typical_d": 540, "typical_drip": 160, "max_area": None, "max_side": None, "max_area_body": 0.137, "max_side_body": 380, "max_area_drip": 0.194, "max_side_drip": 540, "abs_max_area": 0.55, "nozzle": "2–30",  "flow": 2},
    "Griddle":                 {"icon": "", "input_type": "wl",      "typical_w": 760, "typical_d": 760, "max_area": 0.578, "max_side": 760, "nozzle": "1–60",  "flow": 1},
    "Gas or electric broiler": {"icon": "", "input_type": "wl",      "typical_w": 901, "typical_d": 601, "max_area": 0.561, "max_side": 920, "nozzle": "1–60",  "flow": 1},
    "Range top":               {"icon": "", "input_type": "wl",      "typical_w": 640, "typical_d": 640, "max_area": None,  "distance": 270,   "nozzle": "2–60",  "flow": 2},
    "Wok":                     {"icon": "", "input_type": "d",       "typical_dia": 410,                 "max_area": 0.30,  "abs_max_dia": 410, "nozzle": "2–30",  "flow": 2},
    "Tilt skillet":            {"icon": "", "input_type": "wl",      "typical_w": 700, "typical_d": 550, "max_area": 0.194,                 "nozzle": "2–30",  "flow": 2},
    "Circular duct":           {"icon": "", "input_type": "d",       "typical_dia": 404,                 "max_area": None, "max_dia": 404, "max_perim": 1270,  "nozzle": "1–110", "flow": 1},
    "Rectangular duct":        {"icon": "",  "input_type": "wl",      "typical_w": 211, "typical_d": 423, "max_area": None, "max_perim": 1270,                  "nozzle": "1–110", "flow": 1},
    "Plenum":                  {"icon": "", "input_type": "wl",      "typical_w": 600, "typical_d": 3000, "max_area": None, "max_width": 600, "max_length": 3000, "abs_max_width": 600, "nozzle": "1–60",  "flow": 1},
    "Plenum V-style":          {"icon": "", "input_type": "wl",      "typical_w": 1200, "typical_d": 3000, "max_area": None, "max_width": 600, "max_length": 3000, "min_cols": 2, "abs_max_width": 1200, "nozzle": "1–60",  "flow": 1},
}

MAX_APPLIANCES = 15

NOZZLE_PLACEMENT = {'Fryer': 'Nozzle placed 690 to 1200 mm above the top of its section, aiming at the section center.', 'Fryer with drip board': 'Nozzle placed 690 to 1200 mm above the top of its section, aiming at the section center.', 'Wok': 'Nozzle placed 690 to 1200 mm above the wok, aiming at the center.', 'Tilt skillet': 'Nozzle placed 690 to 1200 mm above its section, aiming at the section center. Position should be at the front so that there is a clear line from the nozzle to the entire hazard area with the lid in open position.', 'Griddle': 'Nozzle placed 760 to 1020 mm above its section, 0 to 50 mm from the edge, aiming at the section center.', 'Gas or electric broiler': 'Nozzle placed 500 to 1020 mm above its section, aiming at the section center.', 'Range top': 'Nozzle placed centrally 690 to 1020 mm above its section, aiming straight down. If there is a shelf, ensure there is a clear line from the nozzle to the entire surface area.', 'Plenum': 'Nozzle placed maximum 150 mm from the start of the plenum, 50 to 100 mm from the filters, aiming horizontally. For multiple nozzles, they must aim in the same direction with linear separation of maximum 3 m.', 'Plenum V-style': 'Nozzle placed maximum 150 mm from the start of the plenum, 50 to 100 mm from the filters, aiming horizontally. For multiple nozzles, they must aim in the same direction with linear separation of maximum 3 m', 'Circular duct': 'Nozzle placed centrally in its section, 50 to 200 mm into the duct, aiming straight up.', 'Rectangular duct': 'Nozzle placed centrally in its section, 50 to 200 mm into the duct, aiming straight up.'}


