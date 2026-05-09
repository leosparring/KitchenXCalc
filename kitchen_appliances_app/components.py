"""Reusable Shiny UI components for KitchenXCalc."""

from shiny import ui

from translations import get_appliance_choices, get_translation

def appliance_card_ui(idx, lang="en", selected=None):
    """Return UI for one hazard entry card. Input fields depend on selected hazard type."""
    suffix = f"_{idx}"
    remove_btn = (
        ui.input_action_button(
            f"remove{suffix}",
            f"✕ {get_translation('remove_button', lang)}",
            class_="btn-remove",
        )
        if idx > 1
        else ui.div()
    )
    select_args = {
        "choices": get_appliance_choices(lang),
    }
    if selected:
        select_args["selected"] = selected
    return ui.div(
        {"class": "card", "id": f"appliance-card-{idx}"},
        ui.div(
            {"class": "card-header"},
            ui.div({"class": "card-title"}, get_translation("hazard_card_title", lang, idx=idx)),
            remove_btn,
        ),
        ui.div(
            {"class": "form-group"},
            ui.input_select(
                f"appliance{suffix}",
                get_translation("select_hazard", lang),
                **select_args,
            ),
        ),
        # Dynamic input fields (incl. quantity) rendered after hazard selection
        ui.output_ui(f"inputs_{idx}"),
    )


