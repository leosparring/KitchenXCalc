"""Reactive server wiring for KitchenXCalc."""

import math

from shiny import ui, render, reactive

from calculations import (
    calculate_slot,
    cell_perimeter,
    compute_area,
    compute_c,
    compute_sections,
    compute_sections_distance,
    compute_sections_drip,
    compute_sections_perimeter,
    compute_sections_plenum,
    compute_sections_range_top_shelf,
    drip_needs_split,
    optimal_circle_grid,
    summarize_slot,
)
from data import APPLIANCES, MAX_APPLIANCES
from svg import build_sections_svg
from translations import (
    get_appliance_label,
    get_nozzle_placement,
    get_translation,
    normalize_language,
)
from components import appliance_card_ui

def server(input, output, session):
    slots = reactive.value([1])   # list of active slot IDs
    next_id = reactive.value(2)   # ever-increasing ID counter

    def current_lang():
        try:
            return normalize_language(input.language())
        except Exception:
            return "en"

    @output
    @render.ui
    def header_title():
        return ui.tags.span(
            get_translation("app_title", current_lang()),
            style="font-family:'Barlow Condensed',sans-serif;font-size:clamp(28px,7vw,60px);font-weight:600;color:var(--navy);letter-spacing:-0.01em;line-height:1;",
        )

    @output
    @render.ui
    def header_description():
        return ui.tags.p(get_translation("app_description", current_lang()))

    @output
    @render.ui
    def language_label():
        return ui.tags.label(
            {"for": "language", "class": "sr-only"},
            get_translation("language_label", current_lang()),
        )

    @output
    @render.ui
    def language_indicator():
        return ui.tags.span(
            current_lang().upper(),
            {
                "class": "language-icon",
                "title": get_translation("language_label", current_lang()),
                "onclick": "document.getElementById('language_picker').classList.toggle('open');",
            },
        )

    @output
    @render.ui
    def add_button():
        return ui.input_action_button(
            "add_appliance",
            ui.HTML("+ &nbsp; " + get_translation("add_another_hazard", current_lang())),
            class_="btn-add",
        )

    # ── Update input labels and values when language changes ───────────────
    @reactive.effect
    @reactive.event(current_lang)
    def _update_input_labels():
        lang = current_lang()
        for idx in range(1, MAX_APPLIANCES + 1):
            suffix = f"_{idx}"
            try:
                appliance = getattr(input, f"appliance{suffix}")()
            except Exception:
                continue
            if not appliance:
                continue
            info = APPLIANCES[appliance]
            itype = info["input_type"]
            # Update labels and values
            if itype == "d":
                ui.update_numeric(f"dia{suffix}", label=get_translation("diameter", lang))
                ui.update_numeric(f"qty{suffix}", label=get_translation("quantity", lang))
                try:
                    dia_val = getattr(input, f"dia{suffix}")()
                    qty_val = getattr(input, f"qty{suffix}")()
                    ui.update_numeric(f"dia{suffix}", value=dia_val)
                    ui.update_numeric(f"qty{suffix}", value=qty_val or 1)
                except Exception:
                    pass
            elif itype == "wl_drip":
                ui.update_numeric(f"width{suffix}", label=get_translation("width", lang))
                ui.update_numeric(f"depth{suffix}", label=get_translation("depth", lang))
                ui.update_numeric(f"drip{suffix}", label=get_translation("drip_board_depth", lang))
                ui.update_numeric(f"qty{suffix}", label=get_translation("quantity", lang))
                try:
                    w_val = getattr(input, f"width{suffix}")()
                    d_val = getattr(input, f"depth{suffix}")()
                    drip_val = getattr(input, f"drip{suffix}")()
                    qty_val = getattr(input, f"qty{suffix}")()
                    ui.update_numeric(f"width{suffix}", value=w_val)
                    ui.update_numeric(f"depth{suffix}", value=d_val)
                    ui.update_numeric(f"drip{suffix}", value=drip_val)
                    ui.update_numeric(f"qty{suffix}", value=qty_val or 1)
                except Exception:
                    pass
            else:
                ui.update_numeric(f"width{suffix}", label=get_translation("width", lang))
                depth_label = get_translation("length", lang) if appliance in ("Plenum", "Plenum V-style") else get_translation("depth", lang)
                ui.update_numeric(f"depth{suffix}", label=depth_label)
                ui.update_numeric(f"qty{suffix}", label=get_translation("quantity", lang))
                try:
                    w_val = getattr(input, f"width{suffix}")()
                    d_val = getattr(input, f"depth{suffix}")()
                    qty_val = getattr(input, f"qty{suffix}")()
                    ui.update_numeric(f"width{suffix}", value=w_val)
                    ui.update_numeric(f"depth{suffix}", value=d_val)
                    ui.update_numeric(f"qty{suffix}", value=qty_val or 1)
                except Exception:
                    pass
                if appliance == "Range top":
                    ui.update_numeric(f"shelf_height{suffix}", label=get_translation("shelf_height", lang))
                    ui.update_numeric(f"shelf_overhang{suffix}", label=get_translation("shelf_overhang", lang))
                    try:
                        sh_val = getattr(input, f"shelf_height{suffix}")()
                        so_val = getattr(input, f"shelf_overhang{suffix}")()
                        ui.update_numeric(f"shelf_height{suffix}", value=sh_val)
                        ui.update_numeric(f"shelf_overhang{suffix}", value=so_val)
                    except Exception:
                        pass

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
        if not appliance:
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
                vals = {"width": w, "depth": d, "qty": qty}
                if appliance == "Range top":
                    try:
                        vals["shelf_height"]   = getattr(input, f"shelf_height{suffix}")()
                        vals["shelf_overhang"] = getattr(input, f"shelf_overhang{suffix}")()
                    except Exception:
                        pass
                return appliance, vals
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
    def build_inline_result(idx, lang):
        appliance, vals = read_inputs(idx)

        if not appliance:
            return ui.div({"class": "result-inline-empty"}, get_translation("select_hazard_hint", lang))

        info = APPLIANCES[appliance]
        appliance_label = get_appliance_label(appliance, lang)
        icon = info["icon"]
        itype = info["input_type"]
        area_m2 = compute_area(appliance, vals)
        max_area = info["max_area"]

        if area_m2 is not None:
            max_px   = 100
            calc = calculate_slot(appliance, vals, APPLIANCES)
            rows = calc["rows"]
            cols = calc["cols"]
            cell_w = calc["cell_w"]
            cell_d = calc["cell_d"]
            n_sections = calc["n_sections"]
            needs_split = calc["needs_split"]
            section_area = calc["section_area"]
            violation_msgs = calc["violation_msgs"]
            w_mm = vals.get("width") or 1
            d_mm = vals.get("depth") or 1

            # ── Shelf infeasible warning ───────────────────────────────────────
            shelf_infeasible = vals.get("_shelf_infeasible", False) if vals else False

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
            svg_html = "" if (abs_exceeded or (vals and vals.get("_shelf_infeasible"))) else build_sections_svg(itype, vals, area_m2, max_area, rows, cols, needs_split, appliance)

            # ── Build sections block ──────────────────────────────
            if needs_split:
                if itype == "d":
                    grid_info = f"{rows}×{cols} {get_translation('grid', lang)} · "
                else:
                    grid_info = f"{rows}×{cols} {get_translation('grid', lang)} · " if (rows > 1 and cols > 1) else ""
                if itype == "d" and info.get("max_perim") is not None:
                    # Circular duct: show cell perimeter instead of area
                    cell_w_mm_circ = vals.get("dia", 1) / cols
                    cell_d_mm_circ = vals.get("dia", 1) / rows
                    cp_circ = cell_perimeter(cell_w_mm_circ, cell_d_mm_circ)
                    note_parts = [f"{grid_info}{get_translation('cell_perimeter', lang)}: {cp_circ:.0f} mm  ·  {get_translation('max', lang)}: {info['max_perim']} mm"]
                elif itype != "d":
                    note_parts = [f"{grid_info}{get_translation('each_section', lang)}: {section_area:.4f} m²,  {cell_w:.0f}×{cell_d:.0f} mm"]
                else:
                    note_parts = [f"{grid_info}{get_translation('each_section', lang)}: {section_area:.4f} m²"]
                _distance  = info.get("distance")
                _max_side  = info.get("max_side")
                _max_perim = info.get("max_perim")
                if _distance is not None:
                    _shelf_off_here = vals.get("_shelf_offset", 0) or 0
                    c_cell = compute_c(cell_w, cell_d + 2 * _shelf_off_here) if _shelf_off_here else compute_c(cell_w, cell_d)
                    note_parts.append(f"c: {c_cell:.1f} mm  ·  {get_translation('limit', lang)}: {_distance} mm")
                    _shelf_nozzle_h = vals.get("_shelf_nozzle_h") if itype != "d" else None
                elif info.get("max_width") is not None:
                    note_parts.append(f"{get_translation('max_width', lang)}: {info['max_width']} mm  ·  {get_translation('max_length', lang)}: {info['max_length']/1000:.0f} m")
                elif _max_perim is not None and itype != "d":
                    cp = cell_perimeter(cell_w, cell_d)
                    note_parts.append(f"{get_translation('cell_perimeter', lang)}: {cp:.0f} mm  ·  {get_translation('max', lang)}: {_max_perim} mm")
                # (circular duct perimeter already added above when itype=="d")
                elif max_area is not None:
                    note_parts.append(f"{get_translation('max_area', lang)}: {max_area} m²")
                    if _max_side:
                        note_parts.append(f"{get_translation('max_side', lang)}: {_max_side} mm")

                note_text = "  ·  ".join(note_parts)

                # For fryer with drip board with unequal rows, replace note with per-row details
                if appliance == "Fryer with drip board" and needs_split:
                    cell_d_bot_note = vals.get("_cell_d_bot", cell_d)
                    cell_d_top_note = cell_d  # upper rows
                    if rows > 1 and abs(cell_d_top_note - cell_d_bot_note) > 0.5:
                        area_top = (cell_w / 1000) * (cell_d_top_note / 1000)
                        area_bot = (cell_w / 1000) * (cell_d_bot_note / 1000)
                        row_label = (
                            get_translation("upper_row", lang)
                            if rows == 2
                            else get_translation("upper_rows", lang, count=rows - 1)
                        )
                        dim_note = ui.div(
                            {"class": "sections-note", "style": "margin-top:2px;"},
                            f"{row_label}: {cell_w:.0f}×{cell_d_top_note:.0f} mm ({area_top:.4f} m²)  ·  "
                            f"{get_translation('bottom_row_drip', lang)}: {cell_w:.0f}×{cell_d_bot_note:.0f} mm ({area_bot:.4f} m²)"
                        )
                        note_text = ""  # suppress the generic note above
                    else:
                        dim_note = ui.div()
                else:
                    dim_note = ui.div()

                if appliance == "Range top" and vals.get("_shelf_nozzle_h") is not None:
                    _nh  = vals["_shelf_nozzle_h"]
                    _off = vals.get("_shelf_offset", 0)
                    _from_inner = round(cell_d / 2 + _off)
                    if round(_off) == 0:
                        _pos_note = get_translation("position_nozzle_center", lang)
                    elif rows > 1:
                        _pos_note = get_translation("position_nozzle_inner_row", lang, distance=_from_inner)
                    else:
                        _pos_note = get_translation("position_nozzle_inner", lang, distance=_from_inner)
                    placement_text = get_translation("range_nozzle_placement", lang, height=_nh, position=_pos_note)
                else:
                    placement_text = get_nozzle_placement(appliance, lang)
                sections_block = ui.div(
                    {"class": "sections-neutral"},
                    ui.div(
                        {"class": "sections-neutral-title"},
                        f"{n_sections} {get_translation('section_plural' if n_sections > 1 else 'section_singular', lang)}",
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
                    ok_parts = [f"c = {c_val:.1f} mm  ·  {get_translation('distance_limit', lang)}: {_distance} mm"]
                    _shelf_nozzle_h = vals.get("_shelf_nozzle_h")
                elif info.get("max_width") is not None:
                    ok_parts = [f"{get_translation('width', lang)}: {w_mm} mm  ·  {get_translation('length', lang)}: {d_mm} mm  ·  {get_translation('max', lang)}: {info['max_width']} mm / {info['max_length']/1000:.0f} m"]
                elif _max_perim is not None and itype == "d":
                    ok_parts = [f"{get_translation('diameter', lang)} {vals.get('dia')} mm ≤ {get_translation('max', lang).lower()} {info.get('max_dia')} mm"]
                elif _max_perim is not None:
                    ok_parts = [f"{get_translation('cell_perimeter', lang)}: {cell_perimeter(w_mm, d_mm):.0f} mm  ·  {get_translation('max', lang)}: {_max_perim} mm"]
                elif max_area is not None:
                    ok_parts = [f"{get_translation('area', lang)}: {area_m2:.4f} m²  ·  {get_translation('max', lang)}: {max_area} m²"]
                    _max_side = info.get("max_side")
                    if _max_side:
                        ok_parts.append(f"{get_translation('max_side', lang)}: {_max_side} mm")
                else:
                    ok_parts = [f"{get_translation('area', lang)}: {area_m2:.4f} m²"]
                if appliance == "Range top" and vals.get("_shelf_nozzle_h") is not None:
                    _nh  = vals["_shelf_nozzle_h"]
                    _off = vals.get("_shelf_offset", 0)
                    _from_inner = round(d_mm / 2 + _off)
                    if round(_off) == 0:
                        _pos_note = get_translation("position_nozzle_center", lang)
                    else:
                        _pos_note = get_translation("position_nozzle_inner", lang, distance=_from_inner)
                    placement_text = get_translation("range_nozzle_placement", lang, height=_nh, position=_pos_note)
                else:
                    placement_text = get_nozzle_placement(appliance, lang)
                sections_block = ui.div(
                    {"class": "sections-neutral"},
                    ui.div(
                        {"class": "sections-neutral-title"},
                        f"1 {get_translation('section_singular', lang)}",
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
                    abs_desc = get_translation("abs_diameter_exceeds", lang, value=abs_val, limit=abs_lim)
                elif info.get("abs_max_area") is not None and area_m2 is not None and area_m2 > info["abs_max_area"]:
                    abs_lim  = info["abs_max_area"]
                    abs_desc = get_translation("abs_area_exceeds", lang, value=area_m2, limit=abs_lim)
                else:
                    abs_lim  = info.get("abs_max_width")
                    abs_val  = vals.get("width")
                    abs_desc = get_translation("abs_width_exceeds", lang, value=abs_val, limit=abs_lim)
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
                        get_translation("cannot_be_protected", lang, appliance=appliance_label.lower()),
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
                           ui.div({"class": "result-inline-stat-label"}, get_translation("nozzle", lang)),
                           ui.div({"class": "result-inline-stat-value", "style": "font-size:1rem;"}, nozzle_label),
                           ui.div({"class": "result-inline-stat-unit"}, ""))
                )
            if flow is not None:
                qty        = vals.get("qty") or 1
                total_flow = n_sections * flow * qty
                stat_tiles.append(
                    ui.div({"class": "result-inline-stat"},
                           ui.div({"class": "result-inline-stat-label"}, get_translation("flow", lang)),
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
                labels.append(get_translation("nozzle", lang))
            if info.get("flow") is not None:
                labels.append(get_translation("flow", lang))
            stats = ui.div(
                {"class": "result-inline-grid"},
                *[ui.div({"class": "result-inline-stat"},
                         ui.div({"class": "result-inline-stat-label"}, lbl),
                         ui.div({"class": "result-inline-stat-value"}, "—"))
                  for lbl in labels]
            )
            if itype == "d":
                hint = get_translation("hint_diameter", lang)
            elif itype == "wl_drip":
                hint = get_translation("hint_width_length_drip", lang)
            else:
                hint = get_translation("hint_width_length", lang)
            footprint = ui.div(
                {"class": "result-inline-dims", "style": "opacity:0.4; margin-top:6px;"},
                hint
            )

        shelf_warning = ui.div()
        if vals and vals.get("_shelf_infeasible"):
            _sh  = vals.get("shelf_height", 0)
            _soh = vals.get("shelf_overhang", 0)
            _sa  = math.degrees(math.atan2(_soh, _sh))
            shelf_warning = ui.div(
                {"style": "margin-top:8px; padding:10px 12px; background:rgba(227,0,15,0.18); "
                           "border:1.5px solid rgba(227,0,15,0.5); border-radius:4px;"},
                ui.div(
                    {"style": "font-family:'Barlow Condensed',sans-serif; font-size:10px; "
                              "letter-spacing:0.12em; text-transform:uppercase; "
                              "color:#ff6b6b; font-weight:700; margin-bottom:4px;"},
                    get_translation("shelf_infeasible_title", lang) + f" ({_sa:.1f}°)"
                ),
                ui.div(
                    {"style": "font-size:12px; color:rgba(245,240,232,0.85); font-weight:500;"},
                    get_translation("shelf_infeasible_message", lang),
                ),
            )
        return ui.div(
            {"class": "result-card-inline"},
            ui.div(
                {"class": "result-inline-header"},
                ui.div({"class": "result-inline-icon"}, icon),
                ui.div(
                    ui.div({"class": "result-inline-name"}, appliance_label),
                    ui.div({"class": "result-inline-subtitle"}, get_translation("dimensions", lang)),
                ),
            ),
            stats,
            footprint,
            sections_block,
            abs_warning,
            shelf_warning,
        )

    # ── Register a static card renderer per slot ────────────────
    def _register_card(idx):
        @output(id=f"card_{idx}")
        @render.ui
        def _card():
            try:
                selected = getattr(input, f"appliance_{idx}")()
            except Exception:
                selected = None
            return appliance_card_ui(idx, current_lang(), selected)

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

    # Register card renderers and remove observers for all possible slots upfront
    for _i in range(1, MAX_APPLIANCES + 1):
        _register_card(_i)
        _register_remove(_i)

    # ── Register a result renderer for a slot ────────────────────
    def _register_result(idx):
        @output(id=f"result_{idx}")
        @render.ui
        def _result():
            return build_inline_result(idx, current_lang())

    # ── Register dynamic input fields renderer for a slot ───────────
    def _register_inputs(idx):
        @output(id=f"inputs_{idx}")
        @render.ui
        def _inputs():
            suffix = f"_{idx}"
            lang = current_lang()
            try:
                appliance = getattr(input, f"appliance{suffix}")()
            except Exception:
                appliance = None
            if not appliance:
                return ui.div()
            info = APPLIANCES[appliance]
            itype = info["input_type"]
            # Helper to get current value safely
            def get_val(field):
                return None  # Don't read current values to avoid re-rendering on input changes
            if itype == "d":
                return ui.div(
                    ui.div(
                        {"class": "input-row"},
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"dia{suffix}", get_translation("diameter", lang), value=get_val("dia"), min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"qty{suffix}", get_translation("quantity", lang), value=get_val("qty") or 1, min=1, max=999),
                        ),
                    ),
                )
            elif itype == "wl_drip":
                return ui.div(
                    ui.div(
                        {"class": "input-row"},
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"width{suffix}", get_translation("width", lang), value=get_val("width"), min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"depth{suffix}", get_translation("depth", lang), value=get_val("depth"), min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                    ),
                    ui.div(
                        {"class": "input-row", "style": "margin-top:4px;"},
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"drip{suffix}", get_translation("drip_board_depth", lang), value=get_val("drip"), min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"qty{suffix}", get_translation("quantity", lang), value=get_val("qty") or 1, min=1, max=999),
                        ),
                    ),
                )
            else:
                depth_label = get_translation("length", lang) if appliance in ("Plenum", "Plenum V-style") else get_translation("depth", lang)
                shelf_row = ui.div()
                if appliance == "Range top":
                    shelf_row = ui.div(
                        {"class": "input-row", "style": "margin-top:4px;"},
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"shelf_height{suffix}", get_translation("shelf_height", lang), value=get_val("shelf_height"), min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"shelf_overhang{suffix}", get_translation("shelf_overhang", lang), value=get_val("shelf_overhang"), min=0, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                    )
                return ui.div(
                    ui.div(
                        {"class": "input-row"},
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"width{suffix}", get_translation("width", lang), value=get_val("width"), min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                        ui.div(
                            {"class": "form-group"},
                            ui.input_numeric(f"depth{suffix}", depth_label, value=get_val("depth"), min=1, max=9999),
                            ui.div({"class": "unit-hint"}, "mm"),
                        ),
                    ),
                    shelf_row,
                    ui.div(
                        {"class": "form-group", "style": "margin-top:4px; max-width:50%;"},
                        ui.input_numeric(f"qty{suffix}", get_translation("quantity", lang), value=get_val("qty") or 1, min=1, max=999),
                    ),
                )

    # Register result and input renderers for all possible slots upfront
    for _i in range(1, MAX_APPLIANCES + 1):
        _register_result(_i)
        _register_inputs(_i)

    # ── Build result data for summary table ───────────────────────
    def build_result(idx, lang):
        appliance, vals = read_inputs(idx)
        if not appliance:
            return None, None
        summary = summarize_slot(appliance, vals, APPLIANCES)
        if summary is None:
            return None, None
        info = APPLIANCES[appliance]
        appliance_label = get_appliance_label(appliance, lang)
        row_data = (
            appliance_label,
            info["icon"],
            summary["qty"],
            summary["nozzle_str"],
            summary["total_flow"],
            summary["nozzle_count"],
            summary["nozzle_type"],
        )
        return None, row_data

    # ── Render summary table only ─────────────────────────────────
    @output
    @render.ui
    def summary_panel():
        current = slots.get()
        table_rows = []
        total_flow = 0

        nozzle_totals = {}  # nozzle_type -> total count
        lang = current_lang()
        for idx in current:
            _, row_data = build_result(idx, lang)
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
                get_translation("nozzles", lang) + " " + ",  ".join(nozzle_parts),
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
            ui.div({"class": "summary-title"}, get_translation("system_summary", lang)),
            ui.tags.table(
                {"class": "summary-table"},
                ui.tags.thead(
                    ui.tags.tr(
                        ui.tags.th(""),
                        ui.tags.th(get_translation("hazard", lang)),
                        ui.tags.th(get_translation("qty", lang)),
                        ui.tags.th(get_translation("nozzle", lang)),
                        ui.tags.th(get_translation("flow", lang)),
                    )
                ),
                ui.tags.tbody(
                    *table_rows,
                    ui.tags.tr(
                        {"class": "total-row"},
                        ui.tags.td(""),
                        ui.tags.td(get_translation("total", lang)),
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
                    get_translation("save_as_pdf", lang),
                    onclick="window.print()",
                    class_="btn-pdf",
                ),
                ui.tags.button(
                    get_translation("save_system_summary", lang),
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


