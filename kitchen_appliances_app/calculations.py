"""Pure calculation helpers for KitchenXCalc."""

import math

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


def compute_sections_range_top_shelf(w_mm, d_mm, distance, shelf_height_mm, shelf_overhang_mm):
    """
    Range top with shelf constraint.
    shelf_angle = arctan(shelf_overhang / shelf_height).

    For each candidate section size (cw x cd):
      1. Compute the minimum forward offset at nozzle_h=1020 that clears the shelf:
             offset_min = max(0, 1020 * tan(shelf_angle) - cd/2)
         This is the smallest offset needed; using a higher nozzle always needs >= this offset.
      2. Check c at that offset: compute_c(cw, cd + 2*offset_min) < distance.
         If c fails here it will fail at any lower nozzle_h too, so skip to next section size.
      3. Find the maximum nozzle_h where depth_angle > shelf_angle at offset_min:
             nozzle_h_max = (cd/2 + offset_min) / tan(shelf_angle)   (capped at 1020)
         The allowed placement range is 690 to nozzle_h_max.
         If nozzle_h_max < 690 the shelf cannot be cleared at any allowed height; skip.

    Returns (rows, cols, cell_w, cell_d, n_total, max_nozzle_h, offset_min).
    """
    tan_shelf = math.tan(math.atan2(shelf_overhang_mm, shelf_height_mm))

    for total in range(1, 200):
        for rows in range(1, total + 1):
            cols = math.ceil(total / rows)
            if rows * cols != total:
                continue
            cw = w_mm / cols
            cd = d_mm / rows

            # Step 1: minimum offset at the LOWEST nozzle height (690) — gives smallest offset,
            # smallest effective depth, and therefore best (smallest) c.
            # offset(h) = max(0, h * tan_shelf - cd/2) increases with h, so h=690 is best.
            min_offset = max(0.0, 690 * tan_shelf - cd / 2)

            # Physically impossible: offset exceeds half the section depth
            if min_offset > cd / 2:
                continue

            # Step 2: c check at h=690 (best possible c for this section).
            # If it fails here no nozzle height can help — skip to more sections.
            if compute_c(cw, cd + 2 * min_offset) >= distance:
                continue

            # Step 3: find the maximum nozzle height where c is still satisfied.
            # c(h) = compute_c(cw, cd + 2*offset(h)) increases with h.
            # Binary-search or linear scan for largest h in [690, 1020] where c < distance.
            max_nozzle_h = 690
            for h in range(691, 1021):
                off_h = max(0.0, h * tan_shelf - cd / 2)
                if off_h > cd / 2:
                    break
                if compute_c(cw, cd + 2 * off_h) >= distance:
                    break
                max_nozzle_h = h

            # The offset to use is the one at max_nozzle_h (smallest offset that still clears
            # shelf at the chosen height — use the offset corresponding to max_nozzle_h)
            best_offset = max(0.0, max_nozzle_h * tan_shelf - cd / 2)

            return rows, cols, cw, cd, rows * cols, max_nozzle_h, best_offset

    # Infeasible: no section layout can satisfy both shelf and c constraints
    return None


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








def compute_area(appliance, vals, appliances):
    """Compute the protected area in square metres from a slot input dictionary."""
    if vals is None:
        return None
    info = appliances[appliance]
    itype = info["input_type"]
    if itype == "d":
        dia = vals.get("dia")
        if not dia:
            return None
        return math.pi * (dia / 2000) ** 2
    w = vals.get("width")
    d = vals.get("depth")
    if not w or not d:
        return None
    return (w / 1000) * (d / 1000)


def calculate_slot(appliance, vals, appliances):
    """Return the shared calculation state used by inline results and summary rows."""
    if not appliance or vals is None:
        return None

    info = appliances[appliance]
    itype = info["input_type"]
    area_m2 = compute_area(appliance, vals, appliances)
    if area_m2 is None:
        return None

    max_area = info["max_area"]
    rows = cols = n_sections = 1
    cell_w = vals.get("width") or vals.get("dia") or 1
    cell_d = vals.get("depth") or vals.get("dia") or 1
    needs_split = False
    section_area = area_m2
    violation_msgs = []

    if itype == "d":
        dia = vals.get("dia") or 1
        max_dia = info.get("max_dia")
        max_perim = info.get("max_perim")
        if max_dia is not None and dia > max_dia:
            needs_split = True
            rows, cols, cell_w, cell_d, n_sections = compute_sections_perimeter(dia, dia, max_perim)
            section_area = area_m2 / n_sections
            violation_msgs = [f"diameter {dia} mm > max {max_dia} mm"]
            if max_perim:
                cp = cell_perimeter(cell_w, cell_d)
                violation_msgs.append(f"cell perimeter: {cp:.0f} mm < {max_perim} mm ?")
        elif max_area is not None and area_m2 > max_area:
            n_sections_area = math.ceil(area_m2 / max_area)
            rows, cols = optimal_circle_grid(n_sections_area)
            n_sections = rows * cols
            needs_split = True
            section_area = area_m2 / n_sections
            violation_msgs = [f"area {area_m2:.4f} m? > max {max_area} m?"]
    else:
        w_mm = vals.get("width") or 1
        d_mm = vals.get("depth") or 1
        max_side = info.get("max_side")
        distance = info.get("distance")
        cell_w, cell_d = w_mm, d_mm

        if distance is not None:
            shelf_h = vals.get("shelf_height") or 0
            shelf_oh = vals.get("shelf_overhang") or 0
            has_shelf = shelf_h > 0 and shelf_oh > 0
            c_val = compute_c(w_mm, d_mm)
            dist_exceeded = c_val >= distance
            if has_shelf:
                shelf_result = compute_sections_range_top_shelf(w_mm, d_mm, distance, shelf_h, shelf_oh)
                if shelf_result is None:
                    vals["_shelf_infeasible"] = True
                    rows, cols, n_sections = 1, 1, 1
                    cell_w, cell_d = w_mm, d_mm
                    needs_split = False
                else:
                    rows, cols, cell_w, cell_d, n_sections, shelf_nozzle_h, shelf_offset = shelf_result
                    needs_split = n_sections > 1
                    vals["_shelf_nozzle_h"] = shelf_nozzle_h
                    vals["_shelf_offset"] = shelf_offset
            elif dist_exceeded:
                rows, cols, cell_w, cell_d, n_sections = compute_sections_distance(w_mm, d_mm, distance)
                needs_split = True
            section_area = (w_mm * d_mm / 1e6) / n_sections
            if dist_exceeded:
                violation_msgs.append(f"c = {c_val:.1f} mm ? distance {distance} mm")
        elif info.get("max_width") is not None:
            max_width = info["max_width"]
            max_length = info["max_length"]
            min_cols = info.get("min_cols", 1)
            abs_max_width = info.get("abs_max_width")
            w_exceeded = w_mm > max_width
            d_exceeded = d_mm > max_length
            needs_split = w_exceeded or d_exceeded or (min_cols > 1)
            rows, cols, cell_w, cell_d, n_sections = compute_sections_plenum(w_mm, d_mm, max_width, max_length, min_cols)
            section_area = (w_mm * d_mm / 1e6) / n_sections
            if w_exceeded:
                violation_msgs.append(f"width {w_mm} mm > max {max_width} mm")
            if d_exceeded:
                violation_msgs.append(f"length {d_mm} mm > max {max_length} mm")
            if min_cols > 1 and not w_exceeded:
                violation_msgs.append(f"minimum {min_cols} width sections required")
        elif itype == "wl_drip" and info.get("max_area_body") is not None:
            drip_mm = vals.get("drip") or 0
            max_area_body = info["max_area_body"]
            max_side_body = info["max_side_body"]
            max_area_drip = info["max_area_drip"]
            max_side_drip = info["max_side_drip"]
            needs_split = drip_needs_split(w_mm, d_mm, drip_mm, max_area_body, max_side_body, max_area_drip, max_side_drip)
            if needs_split:
                rows, cols, cell_w, cell_d, n_sections, cell_d_bot = compute_sections_drip(
                    w_mm, d_mm, drip_mm, max_area_body, max_side_body, max_area_drip, max_side_drip
                )
            else:
                rows, cols, n_sections = 1, 1, 1
                cell_w, cell_d = w_mm, d_mm
                cell_d_bot = d_mm
            vals["_cell_d_bot"] = cell_d_bot
            vals["_rows"] = rows
            vals["_cols"] = cols
            section_area = (w_mm * d_mm / 1e6) / n_sections
            if needs_split:
                violation_msgs.append(f"body: {(w_mm/1000)*(d_mm/1000):.4f} m?, drip row: {cell_w:.0f}?{cell_d_bot:.0f} mm")
        else:
            max_perim_rect = info.get("max_perim")
            area_exceeded = max_area is not None and area_m2 > max_area
            side_exceeded = max_side is not None and (w_mm > max_side or d_mm > max_side)
            perim_exceeded = max_perim_rect is not None and cell_perimeter(w_mm, d_mm) >= max_perim_rect
            needs_split = area_exceeded or side_exceeded or perim_exceeded
            if perim_exceeded and not area_exceeded and not side_exceeded:
                rows, cols, cell_w, cell_d, n_sections = compute_sections_perimeter(w_mm, d_mm, max_perim_rect)
            elif needs_split:
                rows, cols, cell_w, cell_d, n_sections = compute_sections(w_mm, d_mm, max_area or 1e9, max_side)
            section_area = (w_mm * d_mm / 1e6) / n_sections if needs_split else area_m2
            if area_exceeded:
                violation_msgs.append(f"area {area_m2:.4f} m? > max {max_area} m?")
            if side_exceeded:
                exc_sides = []
                if w_mm > max_side:
                    exc_sides.append(f"width {w_mm} mm")
                if d_mm > max_side:
                    exc_sides.append(f"length {d_mm} mm")
                violation_msgs.append(f"{' & '.join(exc_sides)} > max side {max_side} mm")
            if perim_exceeded:
                violation_msgs.append(f"perimeter {cell_perimeter(w_mm,d_mm):.0f} mm ? max {max_perim_rect} mm")

    return {
        "area_m2": area_m2,
        "rows": rows,
        "cols": cols,
        "cell_w": cell_w,
        "cell_d": cell_d,
        "n_sections": n_sections,
        "needs_split": needs_split,
        "section_area": section_area,
        "violation_msgs": violation_msgs,
    }


def summarize_slot(appliance, vals, appliances):
    """Return nozzle/flow summary data for one completed slot."""
    calc = calculate_slot(appliance, vals, appliances)
    if calc is None:
        return None
    info = appliances[appliance]
    n_sections = calc["n_sections"]
    nozzle = info.get("nozzle")
    flow = info.get("flow")
    qty = vals.get("qty") or 1
    total_flow = (n_sections * flow * qty) if flow is not None else None
    nozzle_str = f"{n_sections}x {nozzle}" if nozzle is not None else None
    nozzle_count = n_sections * qty if nozzle is not None else 0
    return {
        "qty": qty,
        "nozzle_str": nozzle_str,
        "total_flow": total_flow,
        "nozzle_count": nozzle_count,
        "nozzle_type": nozzle,
        "calculation": calc,
    }
