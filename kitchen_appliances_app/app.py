import math
import base64
from pathlib import Path
from shiny import App, ui, render, reactive


_logo_path = Path(__file__).parent / "www" / "logo.png"
_LOGO_SRC = "data:image/png;base64," + base64.b64encode(_logo_path.read_bytes()).decode()

# input_type: "wl" = width+length, "d" = diameter only, "wl_drip" = width+length+drip board depth
# typical_w / typical_d / typical_dia in mm; max_area in m²; max_side in mm (optional)
# nozzle: nozzle spacing range string; flow: flow rate per nozzle
APPLIANCES = {
    "Fryer":                   {"icon": "", "input_type": "wl",      "typical_w": 360, "typical_d": 380, "max_area": 0.137, "max_side": 380, "abs_max_area": 0.55, "nozzle": "2–30",  "flow": 2},
    "Fryer with drip board":   {"icon": "", "input_type": "wl_drip", "typical_w": 360, "typical_d": 540, "typical_drip": 160, "max_area": None, "max_side": None, "max_area_body": 0.137, "max_side_body": 380, "max_area_drip": 0.1945, "max_side_drip": 540, "abs_max_area": 0.55, "nozzle": "2–30",  "flow": 2},
    "Griddle":                 {"icon": "", "input_type": "wl",      "typical_w": 760, "typical_d": 760, "max_area": 0.578, "max_side": 760, "nozzle": "1–60",  "flow": 1},
    "Gas or electric broiler": {"icon": "", "input_type": "wl",      "typical_w": 901, "typical_d": 601, "max_area": 0.561, "max_side": 920, "nozzle": "1–60",  "flow": 1},
    "Range top":               {"icon": "", "input_type": "wl",      "typical_w": 640, "typical_d": 640, "max_area": None,  "distance": 270,   "nozzle": "2–60",  "flow": 2},
    "Wok":                     {"icon": "", "input_type": "d",       "typical_dia": 410,                 "max_area": 0.30,  "abs_max_dia": 410, "nozzle": "2–30",  "flow": 2},
    "Tilt skillet":            {"icon": "", "input_type": "wl",      "typical_w": 700, "typical_d": 550, "max_area": 0.1945,                 "nozzle": "2–30",  "flow": 2},
    "Circular duct":           {"icon": "", "input_type": "d",       "typical_dia": 404,                 "max_area": None, "max_dia": 404, "max_perim": 1270,  "nozzle": "1–110", "flow": 1},
    "Rectangular duct":        {"icon": "",  "input_type": "wl",      "typical_w": 211, "typical_d": 423, "max_area": None, "max_perim": 1270,                  "nozzle": "1–110", "flow": 1},
    "Plenum":                  {"icon": "", "input_type": "wl",      "typical_w": 600, "typical_d": 3000, "max_area": None, "max_width": 600, "max_length": 3000, "abs_max_width": 600, "nozzle": "1–60",  "flow": 1},
    "Plenum V-style":          {"icon": "", "input_type": "wl",      "typical_w": 1200, "typical_d": 3000, "max_area": None, "max_width": 600, "max_length": 3000, "min_cols": 2, "abs_max_width": 1200, "nozzle": "1–60",  "flow": 1},
}

CSS = """
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@500;600;700&display=swap');

    :root {
        --red:        #E3000F;
        --red-dark:   #b50000;
        --navy:       #2b2a29;
        --navy-mid:   #3d3c3b;
        --steel:      #3D4F6B;
        --silver:     #8A96A8;
        --light:      #F0F2F5;
        --white:      #FFFFFF;
        --border:     #D6DBE4;
        --shadow:     rgba(26,34,51,0.10);
        --shadow-lg:  rgba(26,34,51,0.18);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
        background: var(--light);
        font-family: 'Barlow', sans-serif;
        color: var(--navy);
        min-height: 100vh;
    }

    .app-wrapper {
        max-width: 860px;
        margin: 0 auto;
        padding: 40px 24px 80px;
    }

    /* Header */
    .header { margin-bottom: 36px; }
    .header-eyebrow {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 11px;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: var(--red);
        font-weight: 600;
        margin-bottom: 8px;
    }
    .header h1 {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 700;
        line-height: 1.05;
        color: var(--navy);
        margin-bottom: 10px;
        letter-spacing: -0.01em;
    }
    .header h1 em { font-style: normal; color: var(--red); }
    .header p {
        font-size: 14px;
        color: var(--steel);
        font-weight: 400;
        max-width: 480px;
        line-height: 1.6;
    }
    .divider { width: 40px; height: 3px; background: var(--red); margin: 14px 0 16px; }

    /* Card */
    .card {
        background: var(--white);
        border-radius: 4px;
        padding: 16px 18px;
        box-shadow: 0 1px 4px var(--shadow), 0 0 0 1px var(--border);
        margin-bottom: 10px;
        min-width: 0;
        overflow: hidden;
    }
    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .card-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--navy);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .card-title::before {
        content: '';
        display: inline-block;
        width: 3px; height: 14px;
        border-radius: 2px;
        background: var(--red);
    }

    /* Remove button */
    .btn-remove {
        background: none;
        border: 1px solid var(--border);
        border-radius: 3px;
        color: var(--steel);
        font-family: 'Barlow', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.06em;
        padding: 5px 12px;
        cursor: pointer;
        transition: border-color 0.15s, color 0.15s;
    }
    .btn-remove:hover { border-color: var(--red); color: var(--red); }

    /* Form controls */
    .form-group { margin-bottom: 10px; }
    label {
        display: block;
        font-size: 10px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 600;
        color: var(--steel);
        margin-bottom: 4px;
    }
    select, input[type="number"] {
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
        padding: 7px 10px;
        border: 1px solid var(--border);
        border-radius: 3px;
        background: var(--white);
        font-family: 'Barlow', sans-serif;
        font-size: 13px;
        color: var(--navy);
        transition: border-color 0.15s, box-shadow 0.15s;
        appearance: none;
        -webkit-appearance: none;
    }
    select {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%23E3000F' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 12px center;
        padding-right: 36px;
    }
    select:focus, input[type="number"]:focus {
        outline: none;
        border-color: var(--red);
        box-shadow: 0 0 0 3px rgba(227,0,15,0.10);
    }
    .input-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; min-width: 0; }
    .input-row > * { min-width: 0; }
    .unit-hint {
        font-size: 10px;
        color: var(--silver);
        margin-top: 3px;
        font-weight: 400;
        letter-spacing: 0;
        text-transform: none;
    }

    /* Add button */
    .btn-add-wrapper { margin: 4px 0 18px; }
    .btn-add {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--red);
        color: var(--white);
        border: none;
        border-radius: 3px;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 11px 22px;
        cursor: pointer;
        transition: background 0.15s, transform 0.1s;
        box-shadow: 0 2px 8px rgba(227,0,15,0.22);
    }
    .btn-add:hover { background: var(--red-dark); transform: translateY(-1px); }
    .btn-add:active { transform: translateY(0); }

    /* Result card (inline) */
    .result-card-inline {
        background: var(--navy);
        border-radius: 4px;
        padding: 16px 18px;
        color: var(--white);
        box-shadow: 0 2px 12px var(--shadow-lg);
        position: relative;
        overflow: visible;
        box-sizing: border-box;
        border-left: 3px solid var(--red);
    }
    .result-card-inline::after { display: none; }
    .result-inline-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .result-inline-icon { font-size: 24px; }
    .result-inline-name {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        line-height: 1.2;
        text-transform: uppercase;
    }
    .result-inline-subtitle {
        font-size: 10px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        opacity: 0.45;
    }
    .result-inline-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
        gap: 6px;
        margin-bottom: 10px;
    }
    .result-inline-stat {
        background: rgba(255,255,255,0.07);
        border-radius: 3px;
        padding: 7px 9px;
        border-top: 2px solid var(--red);
    }
    .result-inline-stat-label {
        font-size: 9px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        opacity: 0.5;
        margin-bottom: 4px;
        font-weight: 500;
    }
    .result-inline-stat-value {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        line-height: 1;
    }
    .result-inline-stat-unit { font-size: 9px; opacity: 0.5; margin-top: 2px; }
    .result-inline-dims { font-size: 10px; opacity: 0.45; line-height: 1.5; }
    .result-inline-empty {
        background: var(--navy);
        border-radius: 4px;
        padding: 16px 18px;
        color: rgba(255,255,255,0.3);
        font-size: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        min-height: 80px;
        font-style: italic;
        border-left: 3px solid rgba(255,255,255,0.1);
    }

    /* Side-by-side row */
    .appliance-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 12px;
        align-items: start;
    }
    .appliance-row > * { min-width: 0; }
    .appliance-row .card { margin-bottom: 0; }

    /* Section display */
    .sections-neutral {
        margin-top: 10px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 3px;
        padding: 8px 10px;
    }
    .sections-neutral-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 10px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.55);
        font-weight: 600;
        margin-bottom: 6px;
    }
    .sections-list { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 4px; }
    .section-chip {
        background: rgba(255,255,255,0.10);
        border-radius: 2px;
        padding: 3px 8px;
        font-size: 10px;
        color: rgba(255,255,255,0.8);
        white-space: nowrap;
    }
    .sections-note { font-size: 10px; opacity: 0.5; margin-top: 5px; }

    /* Summary table */
    .summary-card {
        background: var(--white);
        border-radius: 4px;
        padding: 16px 18px;
        box-shadow: 0 1px 4px var(--shadow), 0 0 0 1px var(--border);
        margin-bottom: 10px;
    }
    .summary-title {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--navy);
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .summary-title::before {
        content: '';
        display: inline-block;
        width: 3px; height: 14px;
        border-radius: 2px;
        background: var(--red);
    }
    .summary-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .summary-table th {
        text-align: left;
        font-size: 9px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--steel);
        font-weight: 600;
        padding: 0 12px 10px 0;
        border-bottom: 2px solid var(--red);
    }
    .summary-table td { padding: 9px 12px 9px 0; border-bottom: 1px solid var(--border); color: var(--navy); }
    .summary-table tr:last-child td { border-bottom: none; }
    .summary-table .total-row td {
        font-weight: 700;
        color: var(--navy);
        padding-top: 12px;
        border-top: 2px solid var(--navy);
        border-bottom: none;
    }

    /* Empty state */
    .empty-state { text-align: center; padding: 32px 0; color: var(--silver); }
    .empty-state .big-icon { font-size: 44px; margin-bottom: 10px; }
    .empty-state p { font-size: 14px; line-height: 1.6; }

    /* Result card (unused legacy) */
    .result-card {
        background: var(--navy);
        border-radius: 4px;
        padding: 24px 28px;
        color: var(--white);
        margin-bottom: 12px;
        border-left: 3px solid var(--red);
    }

    .btn-pdf {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--white);
        color: var(--navy);
        border: 1.5px solid var(--border);
        border-radius: 3px;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 11px 22px;
        cursor: pointer;
        margin-left: 10px;
        transition: border-color 0.15s;
    }
    .btn-pdf:hover { border-color: var(--navy); }

    @media print {
        html { font-size: 10px; }
        * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        .btn-add-wrapper, .btn-remove, .card-header .btn-remove,
        .btn-pdf { display: none !important; }
        body { background: white !important; }
        .app-wrapper { padding: 8px !important; max-width: 100% !important; }
        .appliance-row {
            grid-template-columns: 1fr 1fr !important;
            gap: 8px !important;
            margin-bottom: 8px !important;
            page-break-inside: avoid;
        }
        .card { padding: 8px 10px !important; box-shadow: none !important;
                border: 1px solid #D6DBE4 !important; margin-bottom: 0 !important; }
        .result-card-inline { padding: 8px 10px !important; border-left: 2px solid #E3000F !important;
                               box-shadow: none !important; }
        .summary-card { padding: 8px 10px !important; box-shadow: none !important;
                        border: 1px solid #D6DBE4 !important; margin-bottom: 6px !important; }
        .result-inline-grid { gap: 4px !important; margin-bottom: 6px !important; }
        .result-inline-stat { padding: 4px 6px !important; }
        .sections-neutral { padding: 5px 8px !important; margin-top: 5px !important; }
        .form-group { margin-bottom: 5px !important; }
        select, input[type="number"] { padding: 3px 6px !important;
                                       border: 1px solid #ccc !important; font-size: 11px !important; }
        .header { margin-bottom: 12px !important; }
        .header h1 { font-size: 1.6rem !important; }
        svg { max-width: 160px !important; }
    }

    @media (max-width: 600px) { .appliance-row { grid-template-columns: 1fr; } }
    @media (max-width: 520px) {
        .card, .summary-card { padding: 14px 14px; }
        .app-wrapper { padding: 24px 12px 60px; }
    }
"""

MAX_APPLIANCES = 15


NOZZLE_PLACEMENT = {'Fryer': 'Nozzle placed 690 to 1200 mm above the top of its section, aiming at the section center.', 'Fryer with drip board': 'Nozzle placed 690 to 1200 mm above the top of its section, aiming at the section center.', 'Wok': 'Nozzle placed 690 to 1200 mm above the wok, aiming at the center.', 'Tilt skillet': 'Nozzle placed 690 to 1200 mm above its section, aiming at the section center. Position should be at the front so that there is a clear line from the nozzle to the entire hazard area with the lid in open position.', 'Griddle': 'Nozzle placed 760 to 1020 mm above its section, 0 to 50 mm from the edge, aiming at the section center.', 'Gas or electric broiler': 'Nozzle placed 500 to 1020 mm above its section, aiming at the section center.', 'Range top': 'Nozzle placed centrally 690 to 1020 mm above its section, aiming straight down. If there is a shelf, ensure there is a clear line from the nozzle to the entire surface area.', 'Plenum': 'Nozzle placed maximum 150 mm from the start of the plenum, 50 to 100 mm from the filters, aiming horizontally. For multiple nozzles, they must aim in the same direction with linear separation of maximum 3 m.', 'Plenum V-style': 'Nozzle placed maximum 150 mm from the start of the plenum, 50 to 100 mm from the filters, aiming horizontally. For multiple nozzles, they must aim in the same direction with linear separation of maximum 3 m', 'Circular duct': 'Nozzle placed centrally in its section, 50 to 200 mm into the duct, aiming straight up.', 'Rectangular duct': 'Nozzle placed centrally in its section, 50 to 200 mm into the duct, aiming straight up.'}


def appliance_card_ui(idx):
    """Return UI for one hazard entry card. Input fields depend on selected hazard type."""
    suffix = f"_{idx}"
    remove_btn = (
        ui.input_action_button(f"remove{suffix}", "✕ Remove", class_="btn-remove")
        if idx > 1
        else ui.div()
    )
    return ui.div(
        {"class": "card", "id": f"appliance-card-{idx}"},
        ui.div(
            {"class": "card-header"},
            ui.div({"class": "card-title"}, f"Hazard {idx}"),
            remove_btn,
        ),
        ui.div(
            {"class": "form-group"},
            ui.input_select(
                f"appliance{suffix}",
                "Select Hazard",
                choices=["— choose one —"] + list(APPLIANCES.keys()),
                selected="— choose one —",
            ),
        ),
        # Dynamic input fields (incl. quantity) rendered after hazard selection
        ui.output_ui(f"inputs_{idx}"),
    )


app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@300;400;500;600;700&display=swap",
        ),
        ui.tags.style(CSS),
    ),
    ui.div(
        {"class": "app-wrapper"},
        ui.div(
            {"class": "header"},
            ui.div({"style": "display:flex;align-items:center;gap:16px;margin-bottom:20px;"},ui.tags.img(src=_LOGO_SRC, alt="KitchenX", style="height:60px;display:block;"),ui.tags.span("Calculation Tool", style="font-family:'Barlow Condensed',sans-serif;font-size:60px;font-weight:600;color:var(--fg);letter-spacing:-0.01em;line-height:1;")),
            
            ui.tags.p(
                "Simplified system design for KitchenX"
            ),
        ),
        ui.div({"id": "row_container_1", "style": "display:block;"},
            ui.div({"class": "appliance-row"},
                ui.output_ui("card_1"),
                ui.output_ui("result_1"),
            )
        ),
        ui.div({"id": "row_container_2", "style": "display:none;"},
            ui.div({"class": "appliance-row"},
                ui.output_ui("card_2"),
                ui.output_ui("result_2"),
            )
        ),
        ui.div({"id": "row_container_3", "style": "display:none;"},
            ui.div({"class": "appliance-row"},
                ui.output_ui("card_3"),
                ui.output_ui("result_3"),
            )
        ),
        ui.div({"id": "row_container_4", "style": "display:none;"},
            ui.div({"class": "appliance-row"},
                ui.output_ui("card_4"),
                ui.output_ui("result_4"),
            )
        ),
        ui.div({"id": "row_container_5", "style": "display:none;"},
            ui.div({"class": "appliance-row"},
                ui.output_ui("card_5"),
                ui.output_ui("result_5"),
            )
        ),
        ui.div({"id": "row_container_6", "style": "display:none;"},
            ui.div({"class": "appliance-row"},
                ui.output_ui("card_6"),
                ui.output_ui("result_6"),
            )
        ),
        ui.div({"id": "row_container_7", "style": "display:none;"},
            ui.div({"class": "appliance-row"},
                ui.output_ui("card_7"),
                ui.output_ui("result_7"),
            )
        ),
        ui.div({"id": "row_container_8", "style": "display:none;"},
            ui.div({"class": "appliance-row"},
                ui.output_ui("card_8"),
                ui.output_ui("result_8"),
            )
        ),
        ui.div(
            {"class": "btn-add-wrapper"},
            ui.input_action_button(
                "add_appliance",
                ui.HTML("+ &nbsp; Add Another Hazard"),
                class_="btn-add",
            ),
        ),
        ui.output_ui("summary_panel"),
    ),

    ui.tags.script("""
(function(){
  const LS_KEY = 'kxappliances_autosave';
  const MAX_SLOTS = 8;
  const SLOT_FIELDS = ['appliance','width','depth','dia','drip','qty'];

  // ── Save state to localStorage ──────────────────────────────────
  function saveState(){
    try {
      const data = { slots: [], timestamp: Date.now() };
      // Find active slots by checking which selects exist and have a value
      for(let i = 1; i <= MAX_SLOTS; i++){
        const sel = document.getElementById('appliance' + i);
        if(!sel) continue;
        const slot = { id: i };
        SLOT_FIELDS.forEach(function(f){
          const el = document.getElementById(f + i);
          if(el) slot[f] = el.value;
        });
        data.slots.push(slot);
      }
      localStorage.setItem(LS_KEY, JSON.stringify(data));
    } catch(e){}
  }

  // ── Restore state from localStorage ────────────────────────────
  function restoreState(){
    try {
      const raw = localStorage.getItem(LS_KEY);
      if(!raw) return;
      const data = JSON.parse(raw);
      if(!data.slots || !data.slots.length) return;

      // Click "Add Another Hazard" to create enough slots
      const firstSlot = data.slots[0];
      const addBtn = document.querySelector('.btn-add');

      function setField(id, value){
        const el = document.getElementById(id);
        if(!el || value === undefined || value === null || value === '') return;
        const nativeInputSetter = Object.getOwnPropertyDescriptor(
          window.HTMLInputElement.prototype, 'value') ||
          Object.getOwnPropertyDescriptor(window.HTMLSelectElement.prototype, 'value');
        if(nativeInputSetter && nativeInputSetter.set){
          nativeInputSetter.set.call(el, value);
        } else {
          el.value = value;
        }
        el.dispatchEvent(new Event('change', {bubbles: true}));
        el.dispatchEvent(new Event('input', {bubbles: true}));
      }

      function restoreSlot(slot, attempt){
        attempt = attempt || 0;
        if(attempt > 30) return;
        const appSel = document.getElementById('appliance' + slot.id);
        if(!appSel){
          // Slot not rendered yet — click Add button and retry
          if(addBtn && slot.id > 1) addBtn.click();
          setTimeout(function(){ restoreSlot(slot, attempt + 1); }, 150);
          return;
        }
        // Set appliance selector
        setField('appliance' + slot.id, slot.appliance);
        // Wait for dynamic inputs to render, then set dimensions
        setTimeout(function(){
          SLOT_FIELDS.forEach(function(f){
            if(f !== 'appliance') setField(f + slot.id, slot[f]);
          });
        }, 300);
      }

      // Restore slots sequentially with delays to allow Shiny to render
      data.slots.forEach(function(slot, idx){
        setTimeout(function(){ restoreSlot(slot, 0); }, idx * 500);
      });

    } catch(e){}
  }

  // Auto-save on any input change (debounced)
  let saveTimer = null;
  document.addEventListener('change', function(){ 
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveState, 800);
  });
  document.addEventListener('input', function(){
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveState, 800);
  });

  // Restore on page load after Shiny is ready
  if(window.Shiny){
    Shiny.addCustomMessageHandler('__kx_ready__', function(){ restoreState(); });
  }
  // Fallback: restore after a delay
  setTimeout(restoreState, 1500);
})();
"""),
)



def optimal_circle_grid(n):
    """
    For n sections covering a circle with rows×cols grid,
    find the rows×cols combination with fewest total cells
    whose total area >= circle area (i.e. rows*cols >= n),
    preferring grids that are as square as possible.
    Returns (rows, cols).
    """
    best = None
    for rows in range(1, n + 1):
        cols = math.ceil(n / rows)
        total = rows * cols
        if best is None or total < best[0] or (total == best[0] and abs(rows - cols) < abs(best[1] - best[2])):
            best = (total, rows, cols)
    return best[1], best[2]


def compute_sections(w_mm, d_mm, max_area, max_side=None):
    """
    Find minimum rows×cols grid satisfying:
      - each cell area  <= max_area
      - each cell side  <= max_side  (if given)
    Returns (rows, cols, cell_w_mm, cell_d_mm, n_total).
    """
    best = None
    # Try all row counts up to a reasonable ceiling
    max_rows = math.ceil(d_mm / (max_side or d_mm)) if max_side else 1
    max_cols = math.ceil(w_mm / (max_side or w_mm)) if max_side else 1
    max_rows = max(max_rows, math.ceil((w_mm * d_mm / 1e6) / max_area))
    max_cols = max(max_cols, math.ceil((w_mm * d_mm / 1e6) / max_area))

    for rows in range(1, max_rows * max_cols + 2):
        for cols in range(1, max_rows * max_cols + 2):
            cw = w_mm / cols
            cd = d_mm / rows
            cell_area = (cw / 1000) * (cd / 1000)
            side_ok = (max_side is None) or (cw <= max_side and cd <= max_side)
            if cell_area <= max_area and side_ok:
                total = rows * cols
                # Prefer fewer sections; on tie prefer more rows (horizontal split)
                if best is None or total < best[4] or (total == best[4] and rows < best[0]):
                    best = (rows, cols, cw, cd, total)
                break   # found valid cols for this rows
        # Stop only when current rows exceeds best total (can't improve further)
        if best and rows > best[4]:
            break

    if best is None:
        # Fallback: just divide each dimension by max_side
        cols = math.ceil(w_mm / (max_side or w_mm))
        rows = math.ceil(d_mm / (max_side or d_mm))
        cw = w_mm / cols
        cd = d_mm / rows
        best = (rows, cols, cw, cd, rows * cols)
    return best



def compute_c(w_mm, d_mm):
    """c = sqrt((w/2 - 130)^2 + (d/2 - 130)^2)  (260/2 = 130)"""
    return math.sqrt((w_mm / 2 - 130) ** 2 + (d_mm / 2 - 130) ** 2)


def compute_sections_distance(w_mm, d_mm, distance):
    """
    Find minimum rows×cols grid where every section satisfies c < distance.
    c is computed on each cell (cell_w, cell_d).
    Returns (rows, cols, cell_w, cell_d, n_total).
    """
    for total in range(1, 200):
        for rows in range(1, total + 1):
            cols = math.ceil(total / rows)
            if rows * cols != total:
                continue
            cw = w_mm / cols
            cd = d_mm / rows
            if compute_c(cw, cd) < distance:
                return rows, cols, cw, cd, rows * cols
    # fallback
    cols = math.ceil(w_mm / (distance * 2))
    rows = math.ceil(d_mm / (distance * 2))
    cw, cd = w_mm / cols, d_mm / rows
    return rows, cols, cw, cd, rows * cols


def compute_sections_plenum(w_mm, d_mm, max_width, max_length, min_cols=1):
    """
    Plenum: sections must satisfy cell_width <= max_width AND cell_length <= max_length.
    Width sections split along the width axis (cols), length sections along length axis (rows).
    min_cols enforces a minimum number of width-axis sections (e.g. V-style always >= 2).
    Returns (rows, cols, cell_w, cell_d, n_total).
    """
    cols = max(math.ceil(w_mm / max_width) if w_mm > max_width else 1, min_cols)
    rows = math.ceil(d_mm / max_length) if d_mm > max_length else 1
    cell_w = w_mm / cols
    cell_d = d_mm / rows
    return rows, cols, cell_w, cell_d, rows * cols


def cell_perimeter(w_mm, d_mm):
    """2*(w+d) in mm"""
    return 2 * (w_mm + d_mm)


def compute_sections_perimeter(w_mm, d_mm, max_perim):
    """
    Find minimum rows×cols grid where every cell satisfies 2*(cell_w+cell_d) < max_perim.
    Among grids with the same total, prefer the most square (minimise |rows-cols|).
    Returns (rows, cols, cell_w, cell_d, n_total).
    """
    best = None
    for total in range(1, 300):
        valid_for_total = []
        for rows in range(1, total + 1):
            cols = math.ceil(total / rows)
            if rows * cols != total:
                continue
            cw = w_mm / cols
            cd = d_mm / rows
            if cell_perimeter(cw, cd) < max_perim:
                valid_for_total.append((rows, cols, cw, cd, total))
        if valid_for_total:
            # Among valid grids for this total, pick the most square
            best = min(valid_for_total, key=lambda t: abs(t[0] - t[1]))
            return best
    # fallback
    cols = max(1, math.ceil(w_mm / (max_perim / 4)))
    rows = max(1, math.ceil(d_mm / (max_perim / 4)))
    return rows, cols, w_mm / cols, d_mm / rows, rows * cols


def nozzle_symbols_svg(cx, cy, cell_w_px, cell_h_px, appliance,
                        cell_x=None, cell_y=None, scale=1.0):
    """
    Returns SVG string for nozzle symbols per hazard type.
    cx, cy       = cell centre in SVG coords.
    cell_x/y     = cell top-left corner.
    scale        = mm-to-px scale factor (used for fixed-mm insets like griddle 50 mm).

    Fryer / Fryer with drip board:
      - Full-cell dashed red overlay + cross at centre, no circle.

    Wok:
      - Full-cell dashed red overlay + cross at centre, no circle.

    Griddle:
      - Dashed red overlay inset 50 mm from each edge + cross at centre, no circle.

    All others:
      - Small filled red circle + cross at centre.
    """
    r   = max(min(cell_w_px, cell_h_px) * 0.06, 2.5)
    arm = max(min(cell_w_px, cell_h_px) * 0.10, 3)

    ox = cell_x if cell_x is not None else cx - cell_w_px / 2
    oy = cell_y if cell_y is not None else cy - cell_h_px / 2

    def dashed_overlay(rx, ry, rw, rh):
        return (
            f'<rect x="{rx:.1f}" y="{ry:.1f}" '
            f'width="{rw:.1f}" height="{rh:.1f}" '
            f'fill="rgba(227,0,15,0.12)" stroke="#E3000F" stroke-width="1.2" '
            f'stroke-dasharray="4 3"/>'
        )

    def cross_svg():
        return (
            f'<line x1="{cx-arm:.1f}" y1="{cy:.1f}" x2="{cx+arm:.1f}" y2="{cy:.1f}" '
            f'stroke="#E3000F" stroke-width="1.5"/>'
            f'<line x1="{cx:.1f}" y1="{cy-arm:.1f}" x2="{cx:.1f}" y2="{cy+arm:.1f}" '
            f'stroke="#E3000F" stroke-width="1.5"/>'
        )

    if appliance in ("Fryer", "Fryer with drip board", "Gas or electric broiler", "Tilt skillet"):
        # Inset overlay slightly (2px) so dashed border is visible inside the cell outline
        inset = 2.0
        return dashed_overlay(ox + inset, oy + inset,
                              cell_w_px - 2 * inset, cell_h_px - 2 * inset) + cross_svg()

    elif appliance == "Wok":
        # For wok the shape is circular — draw a circular dashed overlay inset 2px
        # cx/cy is the centre; the "radius" in px is half the smaller dimension minus inset
        wr = min(cell_w_px, cell_h_px) / 2 - 2.0
        circ_overlay = (
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{max(wr,3):.1f}" '
            f'fill="rgba(227,0,15,0.12)" stroke="#E3000F" stroke-width="1.2" '
            f'stroke-dasharray="4 3"/>'
        )
        return circ_overlay + cross_svg()

    elif appliance == "Griddle":
        # Overlay is the border band: area within 50mm of each edge.
        # Draw 4 fill-only strips (no stroke), then one dashed border around the inner hole.
        inset_px = min(50 * scale, cell_w_px / 2 - 1, cell_h_px / 2 - 1)
        fill_only = 'fill="rgba(227,0,15,0.12)" stroke="none"'
        # Top, bottom, left, right strips — fill only, no border
        t  = f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{cell_w_px:.1f}" height="{inset_px:.1f}" {fill_only}/>'
        bo = f'<rect x="{ox:.1f}" y="{oy+cell_h_px-inset_px:.1f}" width="{cell_w_px:.1f}" height="{inset_px:.1f}" {fill_only}/>'
        le = f'<rect x="{ox:.1f}" y="{oy+inset_px:.1f}" width="{inset_px:.1f}" height="{cell_h_px-2*inset_px:.1f}" {fill_only}/>'
        ri = f'<rect x="{ox+cell_w_px-inset_px:.1f}" y="{oy+inset_px:.1f}" width="{inset_px:.1f}" height="{cell_h_px-2*inset_px:.1f}" {fill_only}/>'
        # Single dashed border around the inner clear zone only
        inner_border = (
            f'<rect x="{ox+inset_px:.1f}" y="{oy+inset_px:.1f}" '
            f'width="{cell_w_px-2*inset_px:.1f}" height="{cell_h_px-2*inset_px:.1f}" '
            f'fill="none" stroke="#E3000F" stroke-width="1.2" stroke-dasharray="4 3"/>'
        )
        return t + bo + le + ri + inner_border + cross_svg()

    elif appliance in ("Plenum", "Plenum V-style"):
        # Circle at bottom centre of cell on the cell outline
        # Dashed vertical line going up 3/4 of cell height from circle centre
        bottom_cx = cx
        bottom_cy = oy + cell_h_px
        line_len  = cell_h_px * 0.75
        line_top  = bottom_cy - line_len
        plenum_line = (
            f'<line x1="{bottom_cx:.1f}" y1="{bottom_cy:.1f}" '
            f'x2="{bottom_cx:.1f}" y2="{line_top:.1f}" '
            f'stroke="#E3000F" stroke-width="1.5" stroke-dasharray="4 3"/>'
        )
        plenum_circle = (
            f'<circle cx="{bottom_cx:.1f}" cy="{bottom_cy:.1f}" r="{r:.1f}" '
            f'fill="#E3000F" stroke="#E3000F" stroke-width="1"/>'
        )
        return plenum_line + plenum_circle

    else:
        circle = (
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
            f'fill="#E3000F" stroke="#E3000F" stroke-width="1"/>'
        )
        return cross_svg() + circle


def compute_sections_drip(w_mm, d_mm, drip_mm,
                           max_area_body, max_side_body,
                           max_area_drip, max_side_drip):
    """
    Find minimum total sections for a fryer-with-drip-board.
    Total shape is width × depth. The drip board occupies the bottom drip_mm of depth.

    Layout: cols columns, upper_rows uniform upper rows + 1 bottom row.
    Cells do NOT have to be equal height:
      - Bottom row height (cd_bot) can differ from upper row height (cd_top).
      - cd_bot + upper_rows * cd_top = d_mm  (rows must fill full depth)
      - Upper cells: cell_w × cd_top  ≤ max_area_body, max(cell_w, cd_top) ≤ max_side_body
      - Bottom cells: cell_w × cd_bot ≤ max_area_drip,  max(cell_w, cd_bot) ≤ max_side_drip

    We try all (cols, upper_rows) combos and for each, compute the optimal cd_bot / cd_top split.
    Returns (total_rows, cols, cell_w_mm, cd_top_mm, n_sections, cd_bot_mm).
    The extra return value cd_bot_mm lets callers draw the bottom row differently.
    """
    best = None  # (n_sections, total_rows, cols, cw, cd_top, cd_bot)

    for cols in range(1, 50):
        cw = w_mm / cols
        # Max cd_bot allowed by drip constraints
        max_cd_bot = min(
            max_area_drip / (cw / 1000) * 1000,   # area → mm
            max_side_drip,
            d_mm                                    # can't exceed full depth
        )
        if max_cd_bot <= 0:
            continue

        for upper_rows in range(0, 50):
            # cd_bot must be ≥ drip_mm (drip board must fit in bottom row)
            # cd_bot ≤ max_cd_bot
            # If upper_rows > 0: remaining depth for upper = d_mm - cd_bot
            #   cd_top = (d_mm - cd_bot) / upper_rows
            #   must satisfy body constraints

            if upper_rows == 0:
                # Only one row (bottom), which contains the drip board.
                # Must still satisfy drip constraints AND body constraints
                # (body zone = cell_d - drip_mm must satisfy body limits).
                cd_bot = d_mm
                if cd_bot > max_cd_bot:
                    continue
                body_d_single = cd_bot - drip_mm
                body_ok_single = (
                    body_d_single <= 0 or (   # no body zone at all
                        (cw / 1000) * (body_d_single / 1000) <= max_area_body and
                        max(cw, body_d_single) <= max_side_body
                    )
                )
                if not body_ok_single:
                    continue   # single cell violates body constraint, try more rows
                n = cols
                if best is None or n < best[0]:
                    best = (n, 1, cols, cw, cd_bot, cd_bot, 0)
            else:
                # Find cd_bot in [drip_mm, max_cd_bot] that makes cells as equal as possible,
                # i.e. minimise |cd_bot - cd_top| while satisfying all constraints.
                # cd_top = (d_mm - cd_bot) / upper_rows
                # Equal when cd_bot == cd_top → cd_bot = d_mm / (upper_rows + 1)
                ideal_cd_bot = d_mm / (upper_rows + 1)
                # Clamp to valid range
                cd_bot = max(drip_mm, min(max_cd_bot, ideal_cd_bot))
                remaining = d_mm - cd_bot
                if remaining <= 0:
                    continue
                cd_top = remaining / upper_rows
                body_ok = (
                    (cw / 1000) * (cd_top / 1000) <= max_area_body and
                    max(cw, cd_top) <= max_side_body
                )
                if not body_ok:
                    # cd_top too big; shrink cd_bot toward drip_mm to give more room to upper rows
                    # Max cd_top allowed by body constraints
                    max_cd_top = min(max_area_body / (cw / 1000) * 1000, max_side_body)
                    cd_top = max_cd_top
                    cd_bot = d_mm - cd_top * upper_rows
                    cd_bot = max(drip_mm, min(max_cd_bot, cd_bot))
                    remaining = d_mm - cd_bot
                    if remaining <= 0:
                        continue
                    cd_top = remaining / upper_rows
                    body_ok = (
                        (cw / 1000) * (cd_top / 1000) <= max_area_body and
                        max(cw, cd_top) <= max_side_body
                    )
                if body_ok:
                    n = cols * (upper_rows + 1)
                    diff = abs(cd_bot - cd_top)
                    if best is None or n < best[0] or (n == best[0] and diff < best[5]):
                        best = (n, upper_rows + 1, cols, cw, cd_top, cd_bot, diff)
                    break

    if best is None:
        # Hard fallback
        cols = max(1, math.ceil(w_mm / max_side_body))
        cw   = w_mm / cols
        cd   = d_mm / 2
        return 2, cols, cw, cd, 2 * cols, cd

    n, total_rows, cols, cw, cd_top, cd_bot = best[0], best[1], best[2], best[3], best[4], best[5]
    return total_rows, cols, cw, cd_top, n, cd_bot


def drip_needs_split(w_mm, d_mm, drip_mm, max_area_body, max_side_body,
                     max_area_drip, max_side_drip):
    """
    Split is needed if ANY of these is true:
      1. depth × width > max_area_drip  (0.1945 m²)
      2. width × (depth - drip_depth) > max_area_body  (0.137 m²)
      3. depth > max_side_drip or width > max_side_drip  (540 mm)
      4. (depth - drip_depth) > max_side_body or width > max_side_body  (380 mm)
    """
    body_d = d_mm - drip_mm   # depth of body zone (above drip board)
    return (
        (w_mm / 1000) * (d_mm / 1000)      > max_area_drip  or
        (w_mm / 1000) * (body_d / 1000)    > max_area_body  or
        d_mm > max_side_drip or w_mm > max_side_drip         or
        body_d > max_side_body or w_mm > max_side_body
    )





def build_sections_svg(itype, vals, area_m2, max_area, rows=1, cols=1, needs_split=None, appliance=""):
    """
    Build an SVG showing the footprint outline with section dividers inside.
    Always shown — single section when no split needed, grid when split needed.
    For circular: finds optimal rows×cols grid whose total >= circle area / sec_area.
    """
    SVG_W  = 220
    PAD    = 18
    draw_w = SVG_W - 2 * PAD

    if needs_split is None:
        needs_split = (max_area is not None and area_m2 > max_area)
    n_sections   = rows * cols if needs_split else 1
    section_area = area_m2 / n_sections if n_sections else area_m2

    def cell_color(i):
        return "rgba(255,255,255,0.10)", "rgba(255,255,255,0.55)"

    # ── CIRCULAR ─────────────────────────────────────────────────────
    if itype == "d":
        dia   = vals.get("dia") or 1
        r_px  = draw_w / 2
        cx    = SVG_W / 2
        cy    = PAD + r_px
        svg_h = int(cy + r_px + PAD + 14)

        if not needs_split:
            # Single circle filled — outline IS the circle, no rectangles
            fill, _ = cell_color(0)
            symbols = nozzle_symbols_svg(cx, cy, draw_w, draw_w, appliance, PAD, cy - r_px)
            return (
                f'<svg viewBox="0 0 {SVG_W} {svg_h}" width="{SVG_W}" height="{svg_h}" '
                f'xmlns="http://www.w3.org/2000/svg" style="display:block;margin:10px 0 4px;">\n'
                f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_px:.1f}" '
                f'fill="{fill}" stroke="rgba(245,240,232,0.9)" stroke-width="2"/>\n'
                f'  {symbols}\n'
                f'</svg>'
            )

        # Split case: rectangular grid cells (may overflow circle — dashed border)
        # Scale cells to preserve actual mm aspect ratio (dia/cols × dia/rows).
        # For a circle dia==dia so cell aspect = cols/rows.
        # Fit the whole grid into the bounding square of the circle (draw_w × draw_w).
        cell_w = draw_w / cols
        cell_h = draw_w / rows   # square bounding box → each cell is draw_w/cols × draw_w/rows

        elements = []
        k = 0
        for r in range(rows):
            for c in range(cols):
                x = PAD + c * cell_w
                y = cy - r_px + r * cell_h
                fill, stroke = cell_color(k)
                elements.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_w:.1f}" height="{cell_h:.1f}" '
                    f'fill="{fill}" stroke="{stroke}" stroke-width="1.3" stroke-dasharray="4 2"/>'
                )
                cell_cx = x + cell_w / 2
                cell_cy = y + cell_h / 2
                elements.append(nozzle_symbols_svg(cell_cx, cell_cy, cell_w, cell_h, appliance, x, y))
                k += 1

        # Grid dividers clipped to circle height
        for c in range(1, cols):
            x = PAD + c * cell_w
            elements.append(
                f'<line x1="{x:.1f}" y1="{cy-r_px:.1f}" x2="{x:.1f}" y2="{cy+r_px:.1f}" '
                f'stroke="rgba(245,240,232,0.3)" stroke-width="0.8"/>'
            )
        for r in range(1, rows):
            y = cy - r_px + r * cell_h
            elements.append(
                f'<line x1="{PAD}" y1="{y:.1f}" x2="{PAD+draw_w:.1f}" y2="{y:.1f}" '
                f'stroke="rgba(245,240,232,0.3)" stroke-width="0.8"/>'
            )

        elems_svg = "\n  ".join(elements)
        grid_note = f"{rows}×{cols} grid"
        return (
            f'<svg viewBox="0 0 {SVG_W} {svg_h}" width="{SVG_W}" height="{svg_h}" '
            f'xmlns="http://www.w3.org/2000/svg" style="display:block;margin:10px 0 4px;">\n'
            f'  {elems_svg}\n'
            f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r_px:.1f}" '
            f'fill="none" stroke="rgba(245,240,232,0.9)" stroke-width="2"/>\n'
            f'font-size="9" fill="rgba(245,240,232,0.45)">⌀ {dia} mm  ·  {grid_note}</text>\n'
            f'</svg>'
        )

    # ── RECTANGULAR ──────────────────────────────────────────────────
    else:
        w_mm  = vals.get("width") or 1
        d_mm  = vals.get("depth") or 1

        # Fit into available canvas preserving true aspect ratio
        max_draw_w = draw_w          # 184 px
        max_draw_h = 160             # cap tall shapes

        scale     = min(max_draw_w / w_mm, max_draw_h / d_mm)
        rect_w    = w_mm * scale
        rect_h    = d_mm * scale

        # Each cell pixel size is proportional to its mm dimensions
        cell_w_mm = w_mm / cols
        cell_d_mm = d_mm / rows
        cell_w_px = cell_w_mm * scale

        # Fryer with drip board may have variable row heights
        # vals["_cell_d_bot"] stores bottom row depth in mm; upper rows share remaining depth
        cell_d_bot_mm = vals.get("_cell_d_bot", cell_d_mm) if appliance == "Fryer with drip board" else cell_d_mm
        upper_rows    = rows - 1
        if appliance == "Fryer with drip board" and upper_rows > 0:
            cell_d_top_mm = (d_mm - cell_d_bot_mm) / upper_rows
        else:
            cell_d_top_mm = cell_d_mm
        cell_h_top_px = cell_d_top_mm * scale
        cell_h_bot_px = cell_d_bot_mm * scale

        svg_h  = int(PAD + rect_h + PAD + 14)

        elements = []
        nozzle_elements = []   # drawn after outer border so they appear on top
        k = 0
        # Build cumulative y positions for each row
        row_y = []
        y_cur = PAD
        for r in range(rows):
            row_y.append(y_cur)
            if r < rows - 1:
                y_cur += cell_h_top_px
            else:
                y_cur += cell_h_bot_px

        for r in range(rows):
            cell_h_px = cell_h_bot_px if r == rows - 1 else cell_h_top_px
            for c in range(cols):
                x = PAD + c * cell_w_px
                y = row_y[r]
                fill, stroke = cell_color(k)
                elements.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell_w_px:.1f}" height="{cell_h_px:.1f}" '
                    f'fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'
                )
                cell_cx = x + cell_w_px / 2
                cell_cy = y + cell_h_px / 2
                nozzle_elements.append(nozzle_symbols_svg(cell_cx, cell_cy, cell_w_px, cell_h_px, appliance, x, y, scale))
                k += 1

        # outer border on top of cells but under nozzle symbols
        elements.append(
            f'<rect x="{PAD}" y="{PAD}" width="{rect_w:.1f}" height="{rect_h:.1f}" '
            f'fill="none" stroke="rgba(245,240,232,0.9)" stroke-width="2"/>'
        )
        elements.append(
            f'font-size="9" fill="rgba(245,240,232,0.45)">{w_mm} × {d_mm} mm</text>'
        )
        # nozzle symbols on top of everything
        elements.extend(nozzle_elements)

        # Drip board line: horizontal white dashed line inset drip_depth mm from bottom
        if appliance == "Fryer with drip board":
            drip_mm = vals.get("drip") or 0
            if drip_mm > 0:
                drip_px  = drip_mm * scale
                drip_y   = PAD + rect_h - drip_px
                elements.append(
                    f'<line x1="{PAD:.1f}" y1="{drip_y:.1f}" '
                    f'x2="{PAD + rect_w:.1f}" y2="{drip_y:.1f}" '
                    f'stroke="rgba(255,255,255,0.9)" stroke-width="1.5" stroke-dasharray="5 3"/>'
                )

        elems_svg = "\n  ".join(elements)
        return (
            f'<svg viewBox="0 0 {SVG_W} {svg_h}" width="{SVG_W}" height="{svg_h}" '
            f'xmlns="http://www.w3.org/2000/svg" style="display:block;margin:10px 0 4px;">\n'
            f'  {elems_svg}\n</svg>'
        )

def server(input, output, session):
    slots = reactive.value([1])   # list of active slot IDs
    next_id = reactive.value(2)   # ever-increasing ID counter

    # ── Add a new slot ──────────────────────────────────────────
    @reactive.effect
    @reactive.event(input.add_appliance)
    def _add():
        current = slots.get()
        if len(current) < MAX_APPLIANCES:
            nid = next_id.get()
            slots.set(current + [nid])
            next_id.set(nid + 1)

    # ── Register a remove observer for a given slot ID ───────────
    def _register_remove(idx):
        @reactive.effect
        @reactive.event(getattr(input, f"remove_{idx}"))
        def _remove():
            slots.set([s for s in slots.get() if s != idx])

    # ── Read inputs for a slot, returns dict or None ────────────────
    def read_inputs(idx):
        suffix = f"_{idx}"
        try:
            appliance = getattr(input, f"appliance{suffix}")()
        except Exception:
            return None, None
        if not appliance or appliance == "— choose one —":
            return appliance, None
        info = APPLIANCES[appliance]
        itype = info["input_type"]
        try:
            qty = getattr(input, f"qty{suffix}")() or 1
            if itype == "d":
                dia = getattr(input, f"dia{suffix}")()
                return appliance, {"dia": dia, "qty": qty}
            elif itype == "wl_drip":
                w = getattr(input, f"width{suffix}")()
                d = getattr(input, f"depth{suffix}")()
                drip = getattr(input, f"drip{suffix}")()
                return appliance, {"width": w, "depth": d, "drip": drip, "qty": qty}
            else:
                w = getattr(input, f"width{suffix}")()
                d = getattr(input, f"depth{suffix}")()
                return appliance, {"width": w, "depth": d, "qty": qty}
        except Exception:
            return appliance, None

    # ── Compute area in m² from inputs dict ──────────────────────
    def compute_area(appliance, vals):
        if vals is None:
            return None
        info = APPLIANCES[appliance]
        itype = info["input_type"]
        if itype == "d":
            dia = vals.get("dia")
            if not dia:
                return None
            return math.pi * (dia / 2000) ** 2   # dia in mm → radius in m
        else:
            w = vals.get("width")
            d = vals.get("depth")
            if not w or not d:
                return None
            return (w / 1000) * (d / 1000)       # mm → m

    # ── Build inline result panel for one slot ──────────────────
    def build_inline_result(idx):
        appliance, vals = read_inputs(idx)

        if not appliance or appliance == "— choose one —":
            return ui.div({"class": "result-inline-empty"}, "← select a hazard")

        info = APPLIANCES[appliance]
        icon = info["icon"]
        itype = info["input_type"]
        area_m2 = compute_area(appliance, vals)
        max_area = info["max_area"]

        if area_m2 is not None:
            max_px   = 100
            # ── Determine required grid ───────────────────────────
            if itype == "d":
                dia       = vals.get("dia") or 1
                max_dia   = info.get("max_dia")
                max_perim = info.get("max_perim")

                if max_dia is not None and dia > max_dia:
                    # Diameter exceeded: find grid of cell_w×cell_h covering the circle
                    # where each cell perimeter < max_perim
                    # Grid cells are draw_w/cols × draw_w/rows in px terms,
                    # but in mm the circle bounding square is dia×dia, so cell is dia/cols × dia/rows
                    needs_split = True
                    # Find minimum grid where cell perimeter < max_perim
                    rows, cols, cell_w, cell_d, n_sections = compute_sections_perimeter(
                        dia, dia, max_perim
                    )
                    section_area   = area_m2 / n_sections
                    violation_msgs = [f"diameter {dia} mm > max {max_dia} mm"]
                    if max_perim:
                        cp = cell_perimeter(cell_w, cell_d)
                        violation_msgs.append(f"cell perimeter: {cp:.0f} mm < {max_perim} mm ✓")
                elif max_area is not None and area_m2 > max_area:
                    n_sections_area = math.ceil(area_m2 / max_area)
                    rows, cols      = optimal_circle_grid(n_sections_area)
                    n_sections      = rows * cols
                    needs_split     = True
                    section_area    = area_m2 / n_sections
                    violation_msgs  = [f"area {area_m2:.4f} m² > max {max_area} m²"]
                else:
                    rows, cols, n_sections = 1, 1, 1
                    section_area   = area_m2
                    needs_split    = False
                    violation_msgs = []
            else:
                w_mm     = vals.get("width") or 1
                d_mm     = vals.get("depth") or 1
                max_side = info.get("max_side")
                distance = info.get("distance")  # range top special constraint

                if distance is not None:
                    # Range top: constraint is c < distance per section
                    c_val        = compute_c(w_mm, d_mm)
                    dist_exceeded = c_val >= distance
                    needs_split   = dist_exceeded
                    if needs_split:
                        rows, cols, cell_w, cell_d, n_sections = compute_sections_distance(
                            w_mm, d_mm, distance
                        )
                    else:
                        rows, cols, n_sections = 1, 1, 1
                        cell_w, cell_d = w_mm, d_mm
                    section_area   = (w_mm * d_mm / 1e6) / n_sections
                    violation_msgs = []
                    if dist_exceeded:
                        violation_msgs.append(
                            f"c = {c_val:.1f} mm ≥ distance {distance} mm"
                        )
                elif info.get("max_width") is not None:
                    # Plenum: separate max_width (cols) and max_length (rows) constraints
                    max_width      = info["max_width"]
                    max_length     = info["max_length"]
                    min_cols       = info.get("min_cols", 1)
                    abs_max_width  = info.get("abs_max_width")
                    w_exceeded     = w_mm > max_width
                    d_exceeded     = d_mm > max_length
                    abs_exceeded   = abs_max_width is not None and w_mm > abs_max_width
                    needs_split    = w_exceeded or d_exceeded or (min_cols > 1)
                    rows, cols, cell_w, cell_d, n_sections = compute_sections_plenum(
                        w_mm, d_mm, max_width, max_length, min_cols
                    )
                    section_area   = (w_mm * d_mm / 1e6) / n_sections
                    violation_msgs = []
                    if w_exceeded:
                        violation_msgs.append(f"width {w_mm} mm > max {max_width} mm")
                    if d_exceeded:
                        violation_msgs.append(f"length {d_mm} mm > max {max_length} mm")
                    if min_cols > 1 and not w_exceeded:
                        violation_msgs.append(f"minimum {min_cols} width sections required")
                elif itype == "wl_drip" and info.get("max_area_body") is not None:
                    # Fryer with drip board: dual constraints, variable row heights
                    drip_mm        = vals.get("drip") or 0
                    max_area_body  = info["max_area_body"]
                    max_side_body  = info["max_side_body"]
                    max_area_drip  = info["max_area_drip"]
                    max_side_drip  = info["max_side_drip"]

                    needs_split = drip_needs_split(
                        w_mm, d_mm, drip_mm,
                        max_area_body, max_side_body,
                        max_area_drip, max_side_drip
                    )

                    if needs_split:
                        rows, cols, cell_w, cell_d, n_sections, cell_d_bot = compute_sections_drip(
                            w_mm, d_mm, drip_mm,
                            max_area_body, max_side_body,
                            max_area_drip, max_side_drip
                        )
                    else:
                        rows, cols, n_sections = 1, 1, 1
                        cell_w, cell_d = w_mm, d_mm
                        cell_d_bot = d_mm

                    # Store cell_d_bot for SVG rendering
                    vals["_cell_d_bot"] = cell_d_bot
                    vals["_rows"]       = rows
                    vals["_cols"]       = cols

                    section_area   = (w_mm * d_mm / 1e6) / n_sections
                    violation_msgs = []
                    if needs_split:
                        violation_msgs.append(
                            f"body: {(w_mm/1000)*(d_mm/1000):.4f} m², drip row: {cell_w:.0f}×{cell_d_bot:.0f} mm"
                        )

                else:
                    max_perim_rect = info.get("max_perim")
                    area_exceeded  = max_area is not None and area_m2 > max_area
                    side_exceeded  = max_side is not None and (w_mm > max_side or d_mm > max_side)
                    perim_exceeded = max_perim_rect is not None and cell_perimeter(w_mm, d_mm) >= max_perim_rect
                    needs_split    = area_exceeded or side_exceeded or perim_exceeded

                    if perim_exceeded and not area_exceeded and not side_exceeded:
                        # Split by perimeter only
                        rows, cols, cell_w, cell_d, n_sections = compute_sections_perimeter(
                            w_mm, d_mm, max_perim_rect
                        )
                    elif needs_split:
                        rows, cols, cell_w, cell_d, n_sections = compute_sections(
                            w_mm, d_mm, max_area or 1e9, max_side
                        )
                    else:
                        rows, cols, n_sections = 1, 1, 1
                        cell_w, cell_d = w_mm, d_mm

                    section_area   = (w_mm * d_mm / 1e6) / n_sections if needs_split else area_m2
                    violation_msgs = []
                    if area_exceeded:
                        violation_msgs.append(f"area {area_m2:.4f} m² > max {max_area} m²")
                    if side_exceeded:
                        exc_sides = []
                        if w_mm > max_side: exc_sides.append(f"width {w_mm} mm")
                        if d_mm > max_side: exc_sides.append(f"length {d_mm} mm")
                        violation_msgs.append(f"{' & '.join(exc_sides)} > max side {max_side} mm")
                    if perim_exceeded:
                        violation_msgs.append(f"perimeter {cell_perimeter(w_mm,d_mm):.0f} mm ≥ max {max_perim_rect} mm")

            # ── Absolute max dimension check (plenum / wok / fryer) ─
            abs_exceeded = False
            abs_warning   = ui.div()
            if itype == "d":
                abs_max_dia = info.get("abs_max_dia")
                if abs_max_dia is not None and (vals.get("dia") or 0) > abs_max_dia:
                    abs_exceeded = True
            else:
                abs_max_width = info.get("abs_max_width")
                if abs_max_width is not None and (vals.get("width") or 0) > abs_max_width:
                    abs_exceeded = True
                abs_max_area = info.get("abs_max_area")
                if abs_max_area is not None and area_m2 is not None and area_m2 > abs_max_area:
                    abs_exceeded = True

            # ── Build SVG (skip if abs_max_width exceeded) ────────
            svg_html = "" if abs_exceeded else build_sections_svg(itype, vals, area_m2, max_area, rows, cols, needs_split, appliance)

            # ── Build sections block ──────────────────────────────
            if needs_split:
                if itype == "d":
                    grid_info = f"{rows}×{cols} grid · "
                else:
                    grid_info = f"{rows}×{cols} grid · " if (rows > 1 and cols > 1) else ""
                if itype == "d" and info.get("max_perim") is not None:
                    # Circular duct: show cell perimeter instead of area
                    cell_w_mm_circ = vals.get("dia", 1) / cols
                    cell_d_mm_circ = vals.get("dia", 1) / rows
                    cp_circ = cell_perimeter(cell_w_mm_circ, cell_d_mm_circ)
                    note_parts = [f"{grid_info}Cell perimeter: {cp_circ:.0f} mm  ·  Max: {info['max_perim']} mm"]
                elif itype != "d":
                    note_parts = [f"{grid_info}Each section: {section_area:.4f} m²,  {cell_w:.0f}×{cell_d:.0f} mm"]
                else:
                    note_parts = [f"{grid_info}Each section: {section_area:.4f} m²"]
                _distance  = info.get("distance")
                _max_side  = info.get("max_side")
                _max_perim = info.get("max_perim")
                if _distance is not None:
                    c_cell = compute_c(cell_w, cell_d)
                    note_parts.append(f"c per section: {c_cell:.1f} mm  ·  Limit: {_distance} mm")
                elif info.get("max_width") is not None:
                    note_parts.append(f"Max width: {info['max_width']} mm  ·  Max length: {info['max_length']/1000:.0f} m")
                elif _max_perim is not None and itype != "d":
                    cp = cell_perimeter(cell_w, cell_d)
                    note_parts.append(f"Cell perimeter: {cp:.0f} mm  ·  Max: {_max_perim} mm")
                # (circular duct perimeter already added above when itype=="d")
                elif max_area is not None:
                    note_parts.append(f"Max area: {max_area} m²")
                    if _max_side:
                        note_parts.append(f"Max side: {_max_side} mm")

                note_text = "  ·  ".join(note_parts)

                # For fryer with drip board with unequal rows, replace note with per-row details
                if appliance == "Fryer with drip board" and needs_split:
                    cell_d_bot_note = vals.get("_cell_d_bot", cell_d)
                    cell_d_top_note = cell_d  # upper rows
                    if rows > 1 and abs(cell_d_top_note - cell_d_bot_note) > 0.5:
                        area_top = (cell_w / 1000) * (cell_d_top_note / 1000)
                        area_bot = (cell_w / 1000) * (cell_d_bot_note / 1000)
                        row_label = 'row' if rows == 2 else f'{rows-1} rows'
                        dim_note = ui.div(
                            {"class": "sections-note", "style": "margin-top:2px;"},
                            f"Upper {row_label}: {cell_w:.0f}×{cell_d_top_note:.0f} mm ({area_top:.4f} m²)  ·  "
                            f"Bottom row (drip): {cell_w:.0f}×{cell_d_bot_note:.0f} mm ({area_bot:.4f} m²)"
                        )
                        note_text = ""  # suppress the generic note above
                    else:
                        dim_note = ui.div()
                else:
                    dim_note = ui.div()

                placement_text = NOZZLE_PLACEMENT.get(appliance, "")
                sections_block = ui.div(
                    {"class": "sections-neutral"},
                    ui.div(
                        {"class": "sections-neutral-title"},
                        f"{n_sections} section{'s' if n_sections > 1 else ''}",
                    ),
                    ui.div() if abs_exceeded else ui.HTML(svg_html),
                    ui.div({"class": "sections-note"}, note_text) if note_text else ui.div(),
                    dim_note,
                    ui.div({"class": "sections-note", "style": "margin-top:6px; font-style:italic;"},
                        placement_text) if placement_text else ui.div(),
                )
            else:
                _distance  = info.get("distance")
                _max_perim = info.get("max_perim")
                if _distance is not None:
                    c_val    = compute_c(w_mm, d_mm) if itype != "d" else 0
                    ok_parts = [f"c = {c_val:.1f} mm  ·  Distance limit: {_distance} mm"]
                elif info.get("max_width") is not None:
                    ok_parts = [f"Width: {w_mm} mm  ·  Length: {d_mm} mm  ·  Max: {info['max_width']} mm / {info['max_length']/1000:.0f} m"]
                elif _max_perim is not None and itype == "d":
                    ok_parts = [f"Diameter {vals.get('dia')} mm ≤ max {info.get('max_dia')} mm"]
                elif _max_perim is not None:
                    ok_parts = [f"Perimeter: {cell_perimeter(w_mm, d_mm):.0f} mm  ·  Max: {_max_perim} mm"]
                elif max_area is not None:
                    ok_parts = [f"Area: {area_m2:.4f} m²  ·  Max: {max_area} m²"]
                    _max_side = info.get("max_side")
                    if _max_side:
                        ok_parts.append(f"Max side: {_max_side} mm")
                else:
                    ok_parts = [f"Area: {area_m2:.4f} m²"]
                placement_text = NOZZLE_PLACEMENT.get(appliance, "")
                sections_block = ui.div(
                    {"class": "sections-neutral"},
                    ui.div(
                        {"class": "sections-neutral-title"},
                        "1 section",
                    ),
                    ui.div() if abs_exceeded else ui.HTML(svg_html),
                    ui.div({"class": "sections-note"}, "  ·  ".join(ok_parts)),
                    ui.div({"class": "sections-note", "style": "margin-top:6px; font-style:italic;"},
                        placement_text) if placement_text else ui.div(),
                )

            area_style = ""

            # Absolute max width warning (V-style plenum)
            if abs_exceeded:
                if itype == "d":
                    abs_lim  = info.get("abs_max_dia")
                    abs_val  = vals.get("dia")
                    abs_desc = f"Diameter {abs_val} mm exceeds maximum {abs_lim} mm"
                elif info.get("abs_max_area") is not None and area_m2 is not None and area_m2 > info["abs_max_area"]:
                    abs_lim  = info["abs_max_area"]
                    abs_desc = f"Area {area_m2:.4f} m² exceeds maximum {abs_lim} m²"
                else:
                    abs_lim  = info.get("abs_max_width")
                    abs_val  = vals.get("width")
                    abs_desc = f"Width {abs_val} mm exceeds maximum {abs_lim} mm"
                abs_warning = ui.div(
                    {"style": "margin-top:8px; padding:10px 12px; background:rgba(227,0,15,0.18); "
                               "border:1.5px solid rgba(227,0,15,0.5); border-radius:4px;"},
                    ui.div(
                        {"style": "font-family:'Barlow Condensed',sans-serif; font-size:10px; "
                                  "letter-spacing:0.12em; text-transform:uppercase; "
                                  "color:#ff6b6b; font-weight:700; margin-bottom:4px;"},
                        f"⛔  {abs_desc}"
                    ),
                    ui.div(
                        {"style": "font-size:12px; color:rgba(245,240,232,0.85); font-weight:500;"},
                        f"The {appliance.lower()} cannot be protected."
                    ),
                )
            else:
                abs_warning = ui.div()

            # Build stat tiles depending on input type
            if itype == "d":
                dia = vals["dia"]
                viz_size = min(int(dia / 10), max_px)
                stat_tiles = []
                footprint = ui.div()
            elif itype == "wl_drip":
                w, d, drip = vals["width"], vals["depth"], vals["drip"]
                viz_w = min(int((w or 0) / 10), max_px)
                viz_h = min(int((d or 0) / 10), max_px)
                stat_tiles = []
                footprint = ui.div()
            else:
                w, d = vals["width"], vals["depth"]
                viz_w = min(int((w or 0) / 10), max_px)
                viz_h = min(int((d or 0) / 10), max_px)
                stat_tiles = []
                footprint = ui.div()


            # Nozzle / flow tiles
            qty    = vals.get("qty") or 1
            nozzle = info.get("nozzle")
            flow   = info.get("flow")
            if nozzle is not None:
                nozzle_label = f"{n_sections}x {nozzle}"
                stat_tiles.append(
                    ui.div({"class": "result-inline-stat"},
                           ui.div({"class": "result-inline-stat-label"}, "Nozzle"),
                           ui.div({"class": "result-inline-stat-value", "style": "font-size:1rem;"}, nozzle_label),
                           ui.div({"class": "result-inline-stat-unit"}, ""))
                )
            if flow is not None:
                qty        = vals.get("qty") or 1
                total_flow = n_sections * flow * qty
                stat_tiles.append(
                    ui.div({"class": "result-inline-stat"},
                           ui.div({"class": "result-inline-stat-label"}, "Flow"),
                           ui.div({"class": "result-inline-stat-value"}, str(total_flow)),
                           ui.div({"class": "result-inline-stat-unit"}, ""))
                )
            stats = ui.div({"class": "result-inline-grid"}, *stat_tiles)

        else:
            sections_block = ui.div()
            abs_warning    = ui.div()
            # Placeholder stat tiles
            labels = []
            if info.get("nozzle") is not None:
                labels.append("Nozzle")  # placeholder shown before values entered
            if info.get("flow") is not None:
                labels.append("Flow")
            stats = ui.div(
                {"class": "result-inline-grid"},
                *[ui.div({"class": "result-inline-stat"},
                         ui.div({"class": "result-inline-stat-label"}, lbl),
                         ui.div({"class": "result-inline-stat-value"}, "—"))
                  for lbl in labels]
            )
            if itype == "d":
                hint = "Enter diameter to calculate"
            elif itype == "wl_drip":
                hint = "Enter width, length & drip depth"
            else:
                hint = "Enter width & length to calculate"
            footprint = ui.div(
                {"class": "result-inline-dims", "style": "opacity:0.4; margin-top:6px;"},
                hint
            )

        return ui.div(
            {"class": "result-card-inline"},
            ui.div(
                {"class": "result-inline-header"},
                ui.div({"class": "result-inline-icon"}, icon),
                ui.div(
                    ui.div({"class": "result-inline-name"}, appliance),
                    ui.div({"class": "result-inline-subtitle"}, "dimensions"),
                ),
            ),
            stats,
            footprint,
            sections_block,
            abs_warning,
        )

    # ── Register a static card renderer per slot ────────────────
    def _register_card(idx):
        @output(id=f"card_{idx}")
        @render.ui
        def _card():
            return appliance_card_ui(idx)

    # ── Show/hide row containers based on active slots ────────────
    @reactive.effect
    def _update_visibility():
        current = slots.get()
        for i in range(1, MAX_APPLIANCES + 1):
            display = "block" if i in current else "none"
            ui.insert_ui(
                ui.tags.script(
                    f"document.getElementById('row_container_{i}').style.display='{display}';"
                ),
                selector="body",
                where="beforeEnd",
            )

    # Register card renderers for all possible slots upfront
    for _i in range(1, MAX_APPLIANCES + 1):
        _register_card(_i)

    # ── Register a result renderer for a slot ────────────────────
    def _register_result(idx):
        @output(id=f"result_{idx}")
        @render.ui
        def _result():
            return build_inline_result(idx)

    # ── Register dynamic input fields renderer for a slot ───────────
    def _register_inputs(idx):
        @output(id=f"inputs_{idx}")
        @render.ui
        def _inputs():
            suffix = f"_{idx}"
            try:
                appliance = getattr(input, f"appliance{suffix}")()
            except Exception:
                appliance = None
            if not appliance or appliance == "— choose one —":
                return ui.div()
            info = APPLIANCES[appliance]
            itype = info["input_type"]
            if itype == "d":
                return ui.div(
                    ui.div(
                        {"class": "input-row"},
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"dia{suffix}", "Diameter", value=None, min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"qty{suffix}", "Quantity", value=1, min=1, max=999),
                        ),
                    ),
                )
            elif itype == "wl_drip":
                return ui.div(
                    ui.div(
                        {"class": "input-row"},
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"width{suffix}", "Width", value=None, min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"depth{suffix}", "Depth", value=None, min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                    ),
                    ui.div(
                        {"class": "input-row", "style": "margin-top:4px;"},
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"drip{suffix}", "Drip Board Depth", value=None, min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"qty{suffix}", "Quantity", value=1, min=1, max=999),
                        ),
                    ),
                )
            else:
                depth_label = "Length" if appliance in ("Plenum", "Plenum V-style") else "Depth"
                return ui.div(
                    ui.div(
                        {"class": "input-row"},
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"width{suffix}", "Width", value=None, min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"depth{suffix}", depth_label, value=None, min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                    ),
                    ui.div(
                        {"class": "form-group", "style": "margin-top:4px; max-width:50%;"},
                        ui.input_numeric(f"qty{suffix}", "Quantity", value=1, min=1, max=999),
                    ),
                )

    # Register result and input renderers for all possible slots upfront
    for _i in range(1, MAX_APPLIANCES + 1):
        _register_result(_i)
        _register_inputs(_i)

    # ── Build result data for summary table ───────────────────────
    def build_result(idx):
        appliance, vals = read_inputs(idx)
        if not appliance or appliance == "— choose one —":
            return None, None
        info = APPLIANCES[appliance]
        itype = info["input_type"]
        area_m2 = compute_area(appliance, vals)
        if area_m2 is None:
            return None, None

        # Compute n_sections (same logic as build_inline_result)
        max_area = info["max_area"]
        max_side = info.get("max_side")
        distance = info.get("distance")
        if itype == "d":
            dia       = vals.get("dia") or 1
            max_dia   = info.get("max_dia")
            max_perim = info.get("max_perim")
            if max_dia is not None and dia > max_dia and max_perim is not None:
                _, _, _, _, n_sections = compute_sections_perimeter(dia, dia, max_perim)
            elif max_area is not None and area_m2 > max_area:
                n_sec = math.ceil(area_m2 / max_area)
                rows_g, cols_g = optimal_circle_grid(n_sec)
                n_sections = rows_g * cols_g
            else:
                n_sections = 1
        else:
            w_mm = vals.get("width") or 1
            d_mm = vals.get("depth") or 1
            if distance is not None:
                if compute_c(w_mm, d_mm) >= distance:
                    _, _, _, _, n_sections = compute_sections_distance(w_mm, d_mm, distance)
                else:
                    n_sections = 1
            elif info.get("max_width") is not None:
                _, _, _, _, n_sections = compute_sections_plenum(
                    w_mm, d_mm, info["max_width"], info["max_length"], info.get("min_cols", 1)
                )
            elif itype == "wl_drip" and info.get("max_area_body") is not None:
                drip_mm = vals.get("drip") or 0
                if drip_needs_split(w_mm, d_mm, drip_mm,
                                    info["max_area_body"], info["max_side_body"],
                                    info["max_area_drip"], info["max_side_drip"]):
                    _, _, _, _, n_sections, _ = compute_sections_drip(
                        w_mm, d_mm, drip_mm,
                        info["max_area_body"], info["max_side_body"],
                        info["max_area_drip"], info["max_side_drip"]
                    )
                else:
                    n_sections = 1
            else:
                max_perim_r = info.get("max_perim")
                perim_ex    = max_perim_r is not None and cell_perimeter(w_mm, d_mm) >= max_perim_r
                area_ex     = max_area is not None and area_m2 > max_area
                side_ex     = max_side is not None and (w_mm > max_side or d_mm > max_side)
                if perim_ex and not area_ex and not side_ex:
                    _, _, _, _, n_sections = compute_sections_perimeter(w_mm, d_mm, max_perim_r)
                elif area_ex or side_ex:
                    _, _, _, _, n_sections = compute_sections(w_mm, d_mm, max_area or 1e9, max_side)
                else:
                    n_sections = 1

        nozzle     = info.get("nozzle")
        flow       = info.get("flow")
        qty        = vals.get("qty") or 1
        total_flow = (n_sections * flow * qty) if flow is not None else None
        nozzle_str   = f"{n_sections}x {nozzle}" if nozzle is not None else None
        nozzle_count = n_sections * qty if nozzle is not None else 0
        nozzle_type  = nozzle  # the range string e.g. "2-30"

        row_data = (appliance, info["icon"], qty, nozzle_str, total_flow, nozzle_count, nozzle_type)
        return None, row_data

    # ── Render summary table only ─────────────────────────────────
    @output
    @render.ui
    def summary_panel():
        current = slots.get()
        table_rows = []
        total_flow = 0

        nozzle_totals = {}  # nozzle_type -> total count
        for idx in current:
            _, row_data = build_result(idx)
            if row_data:
                name, icon, qty, nozzle_str, flow_val, nozzle_count, nozzle_type = row_data
                if flow_val is not None:
                    total_flow += flow_val
                if nozzle_type is not None and nozzle_count > 0:
                    nozzle_totals[nozzle_type] = nozzle_totals.get(nozzle_type, 0) + nozzle_count
                table_rows.append(
                    ui.tags.tr(
                        ui.tags.td(icon),
                        ui.tags.td(name),
                        ui.tags.td(str(qty)),
                        ui.tags.td(nozzle_str if nozzle_str is not None else "—"),
                        ui.tags.td(str(flow_val) if flow_val is not None else "—"),
                    )
                )

        if len(table_rows) < 1:
            return ui.div()

        if 1 <= total_flow <= 11:
            rec_text = "KX1R – KitchenX Single System"
        elif 12 <= total_flow <= 22:
            rec_text = "KX2R/KX2RM – KitchenX Double System"
        elif 23 <= total_flow <= 33:
            rec_text = "KX3R – KitchenX Triple System"
        else:
            rec_text = None

        # Nozzle totals line
        if nozzle_totals:
            nozzle_parts = [f"{count}× {ntype}" for ntype, count in sorted(nozzle_totals.items())]
            nozzle_summary = ui.div(
                {"style": "margin-top:6px; font-size:12px; color:var(--steel);"},
                "Nozzles: " + ",  ".join(nozzle_parts),
            )
        else:
            nozzle_summary = ui.div()

        if rec_text:
            system_rec = ui.div(
                {"style": "margin-top:14px; padding:12px 14px; "
                           "background:rgba(227,0,15,0.08); border-left:3px solid var(--red); "
                           "border-radius:3px;"},
                ui.div(
                    {"style": "font-family:'Barlow Condensed',sans-serif; font-size:0.95rem; "
                               "font-weight:700; letter-spacing:0.04em; color:var(--navy);"},
                    rec_text,
                ),
                nozzle_summary,
            )
        else:
            system_rec = ui.div()

        return ui.div(
            {"class": "summary-card"},
            ui.div({"class": "summary-title"}, "System Summary"),
            ui.tags.table(
                {"class": "summary-table"},
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th(""),
                        ui.tags.th("Hazard"),
                        ui.tags.th("Qty"),
                        ui.tags.th("Nozzle"),
                        ui.tags.th("Flow"),
                    )
                ),
                ui.tags.tbody(
                    *table_rows,
                    ui.tags.tr(
                        {"class": "total-row"},
                        ui.tags.td(""),
                        ui.tags.td("Total"),
                        ui.tags.td(""),
                        ui.tags.td(""),
                        ui.tags.td(str(total_flow)),
                    ),
                ),
            ),
            system_rec,
            ui.div(
                {"style": "display:flex;gap:10px;align-items:center;margin-top:14px;"},
                ui.tags.button(
                    "⬇ Save as PDF",
                    onclick="window.print()",
                    class_="btn-pdf",
                ),
                ui.tags.button(
                    "⬇ Save System Summary",
                    onclick="""
                        var el = document.querySelector('.summary-card');
                        if (!el) return;
                        var w = window.open('', '_blank');
                        w.document.write('<html><head><title>System Summary</title>');
                        w.document.write('<style>');
                        w.document.write(document.querySelector('style') ? document.querySelector('style').innerHTML : '');
                        w.document.write('body{background:white;padding:24px;font-family:Barlow,sans-serif;}');
                        w.document.write('</style></head><body>');
                        w.document.write(el.outerHTML);
                        w.document.write('</body></html>');
                        w.document.close();
                        w.focus();
                        setTimeout(function(){ w.print(); }, 400);
                    """,
                    class_="btn-pdf",
                ),
            ),
        )


app = App(app_ui, server)
