"""SVG rendering helpers for appliance section diagrams."""

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

    elif appliance == "Range top":
        # scale encoded as complex: real=offset_px, imag=mm_to_px scale factor
        offset_px = scale.real if isinstance(scale, complex) else 0
        shifted_cy = cy + offset_px
        shifted_cx = cx
        arm2 = arm
        cross = (
            f'<line x1="{shifted_cx-arm2:.1f}" y1="{shifted_cy:.1f}" x2="{shifted_cx+arm2:.1f}" y2="{shifted_cy:.1f}" '
            f'stroke="#E3000F" stroke-width="1.5"/>'
            f'<line x1="{shifted_cx:.1f}" y1="{shifted_cy-arm2:.1f}" x2="{shifted_cx:.1f}" y2="{shifted_cy+arm2:.1f}" '
            f'stroke="#E3000F" stroke-width="1.5"/>'
        )
        circle = (
            f'<circle cx="{shifted_cx:.1f}" cy="{shifted_cy:.1f}" r="{r:.1f}" '
            f'fill="#E3000F" stroke="#E3000F" stroke-width="1"/>'
        )
        # Dashed white line from nozzle position toward upper-left corner, stopping 130mm from each edge
        # Only drawn when both section dimensions exceed 260mm
        mm_scale = scale.imag if isinstance(scale, complex) else 1.0
        cell_w_mm = cell_w_px / mm_scale if mm_scale else 0
        cell_h_mm = cell_h_px / mm_scale if mm_scale else 0
        if cell_w_mm > 260 and cell_h_mm > 260:
            stop_x = ox + 130 * mm_scale
            stop_y = oy + 130 * mm_scale
            mid_x = (shifted_cx + stop_x) / 2 + 4
            mid_y = (shifted_cy + stop_y) / 2 - 4
            c_line = (
                f'<line x1="{shifted_cx:.1f}" y1="{shifted_cy:.1f}" '
                f'x2="{stop_x:.1f}" y2="{stop_y:.1f}" '
                f'stroke="white" stroke-width="1" stroke-dasharray="3 2" opacity="0.8"/>'
                f'<text x="{mid_x:.1f}" y="{mid_y:.1f}" '
                f'font-family="Barlow,sans-serif" font-size="8" fill="white" opacity="0.8">c</text>'
            )
        else:
            c_line = ""
        return c_line + cross + circle
    else:
        circle = (
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
            f'fill="#E3000F" stroke="#E3000F" stroke-width="1"/>'
        )
        return cross_svg() + circle


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
                # For Range top with shelf: only innermost row (r==0) gets offset
                if appliance == "Range top":
                    _row_offset = (vals.get("_shelf_offset", 0) or 0) if r == 0 else 0
                    _rt_scale_arg = complex(_row_offset * scale, scale)
                else:
                    _rt_scale_arg = scale
                nozzle_elements.append(nozzle_symbols_svg(cell_cx, cell_cy, cell_w_px, cell_h_px, appliance, x, y, _rt_scale_arg))
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

        # Shelf line: horizontal dashed line inset shelf_overhang mm from top
        if appliance == "Range top":
            shelf_oh_mm = vals.get("shelf_overhang") or 0
            if shelf_oh_mm > 0:
                shelf_px = shelf_oh_mm * scale
                shelf_y  = PAD + shelf_px
                elements.append(
                    f'<line x1="{PAD:.1f}" y1="{shelf_y:.1f}" '
                    f'x2="{PAD + rect_w:.1f}" y2="{shelf_y:.1f}" '
                    f'stroke="rgba(255,255,255,0.9)" stroke-width="1.5" stroke-dasharray="5 3"/>'
                )

        elems_svg = "\n  ".join(elements)
        return (
            f'<svg viewBox="0 0 {SVG_W} {svg_h}" width="{SVG_W}" height="{svg_h}" '
            f'xmlns="http://www.w3.org/2000/svg" style="display:block;margin:10px 0 4px;">\n'
            f'  {elems_svg}\n</svg>'
        )

