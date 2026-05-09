# KitchenXCalc

KitchenXCalc is a Python Shiny application for simplified KitchenX system design. It lets a user add kitchen hazards, enter appliance dimensions, calculate required protection sections, and produce a system summary with nozzle and flow totals.

## Run Locally

From the repository root:

```powershell
python -m shiny run kitchen_appliances_app/app.py
```

Then open the local URL printed by Shiny.

## Project Structure

- `kitchen_appliances_app/app.py` is the Shiny entrypoint.
- `kitchen_appliances_app/layout.py` defines the top-level UI layout.
- `kitchen_appliances_app/server.py` wires Shiny reactive state, input readers, and renderers.
- `kitchen_appliances_app/components.py` contains reusable UI component builders.
- `kitchen_appliances_app/calculations.py` contains pure calculation helpers.
- `kitchen_appliances_app/svg.py` renders the hazard section diagrams.
- `kitchen_appliances_app/data.py` stores appliance constants.
- `kitchen_appliances_app/translations.py` stores language labels and helpers.
- `kitchen_appliances_app/www/` contains static assets such as CSS, JavaScript, and images.
- `tests/` contains calculation tests.

## Development Notes

The current UI is the source of truth. Refactors should preserve existing Shiny IDs, CSS classes, localStorage keys, print behavior, translations, formulas, and visual layout unless a feature request explicitly changes them.

Run tests with:

```powershell
python -m unittest discover tests
```

Calculation changes should usually be made in `calculations.py` first, then surfaced through `server.py` or `components.py`.
