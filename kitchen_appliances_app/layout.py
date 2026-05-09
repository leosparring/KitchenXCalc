"""Top-level Shiny UI layout."""

import base64
from pathlib import Path

from shiny import ui

from data import MAX_APPLIANCES
from translations import LANGUAGE_OPTIONS


_logo_path = Path(__file__).parent / "www" / "logo.png"
_LOGO_SRC = "data:image/png;base64," + base64.b64encode(_logo_path.read_bytes()).decode()

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@300;400;500;600;700&display=swap",
        ),
        ui.tags.link(rel="stylesheet", href="styles.css"),
    ),
    ui.div(
        {"class": "app-wrapper"},
        ui.div(
            {"class": "header"},
            ui.div(
                {"style": "display:flex;align-items:flex-start;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:20px;"},
                ui.div(
                    {"style": "display:flex;align-items:center;gap:12px;flex-wrap:wrap;"},
                    ui.tags.img(src=_LOGO_SRC, alt="KitchenX", style="height:clamp(36px,8vw,60px);display:block;"),
                    ui.div(
                        ui.output_ui("header_title"),
                        ui.output_ui("header_description"),
                    ),
                ),
                ui.div(
                    {"class": "language-switcher"},
                    ui.div(
                        {"class": "language-picker", "id": "language_picker"},
                        ui.output_ui("language_indicator"),
                        ui.div(
                            {"class": "language-drop", "id": "language_dropdown"},
                            ui.div(
                                {"style": "display:none;"},
                                ui.input_select("language", "", choices=LANGUAGE_OPTIONS, selected="en"),
                            ),
                            *[
                                ui.tags.button(
                                    {
                                        "type": "button",
                                        "class": "language-item",
                                        "onclick": f"selectLanguage('{key}')",
                                    },
                                    value,
                                )
                                for key, value in LANGUAGE_OPTIONS.items()
                            ],
                        ),
                    ),
                    ui.output_ui("language_label"),
                ),
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
            ui.output_ui("add_button"),
        ),
        ui.output_ui("summary_panel"),
    ),
    ui.tags.script(src="autosave.js"),
)



