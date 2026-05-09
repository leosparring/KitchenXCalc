"""Translation tables and label helpers."""

from data import APPLIANCES

LANGUAGE_OPTIONS = {
    "en": "EN",
    "sv": "SV",
    "fi": "FI",
    "no": "NO",
    "de": "DE",
}

TRANSLATIONS = {
    "app_title": {
        "en": "Calculation Tool",
        "sv": "Beräkningsverktyg",
        "fi": "Laskentatyökalu",
        "no": "Beregning",
        "de": "Berechnungstool",
    },
    "app_description": {
        "en": "Simplified system design for KitchenX",
        "sv": "Förenklad systemdesign för KitchenX",
        "fi": "Yksinkertaistettu järjestelmäsuunnittelu KitchenX:lle",
        "no": "Forenklet systemdesign for KitchenX",
        "de": "Vereinfachte Systemauslegung für KitchenX",
    },
    "language_label": {
        "en": "Language",
        "sv": "Språk",
        "fi": "Kieli",
        "no": "Språk",
        "de": "Sprache",
    },
    "select_hazard": {
        "en": "Select Hazard",
        "sv": "Välj risk",
        "fi": "Valitse risk",
        "no": "Velg fare",
        "de": "Gefahr wählen",
    },
    "select_hazard_placeholder": {
        "en": "— choose one —",
        "sv": "— välj en —",
        "fi": "— valitse yksi —",
        "no": "— velg en —",
        "de": "— wähle eine —",
    },
    "hazard_card_title": {
        "en": "Hazard {idx}",
        "sv": "Risk {idx}",
        "fi": "Riskialue {idx}",
        "no": "Fare {idx}",
        "de": "Gefahr {idx}",
    },
    "remove_button": {
        "en": "Remove",
        "sv": "Ta bort",
        "fi": "Poista",
        "no": "Fjern",
        "de": "Entfernen",
    },
    "add_another_hazard": {
        "en": "Add Another Hazard",
        "sv": "Lägg till en till risk",
        "fi": "Lisää toinen riski",
        "no": "Legg til en fare til",
        "de": "Weitere Gefahr hinzufügen",
    },
    "diameter": {
        "en": "Diameter",
        "sv": "Diameter",
        "fi": "Halkaisija",
        "no": "Diameter",
        "de": "Durchmesser",
    },
    "width": {
        "en": "Width",
        "sv": "Bredd",
        "fi": "Leveys",
        "no": "Bredde",
        "de": "Breite",
    },
    "depth": {
        "en": "Depth",
        "sv": "Djup",
        "fi": "Syvyys",
        "no": "Dybde",
        "de": "Tiefe",
    },
    "length": {
        "en": "Length",
        "sv": "Längd",
        "fi": "Pituus",
        "no": "Lengde",
        "de": "Länge",
    },
    "drip_board_depth": {
        "en": "Drip Board Depth",
        "sv": "Droppbrädans djup",
        "fi": "Tiputuslevyn syvyys",
        "no": "Dryppbrettdybde",
        "de": "Tiefe der Tropfblech",
    },
    "shelf_height": {
        "en": "Shelf Height",
        "sv": "Hyllhöjd",
        "fi": "Hyllykorkeus",
        "no": "Hyllehøyde",
        "de": "Regalhöhe",
    },
    "shelf_overhang": {
        "en": "Shelf Overhang",
        "sv": "Hylla utstick",
        "fi": "Hyllyn ulkonema",
        "no": "Hylleutspring",
        "de": "Regalüberhang",
    },
    "quantity": {
        "en": "Quantity",
        "sv": "Antal",
        "fi": "Määrä",
        "no": "Antall",
        "de": "Menge",
    },
    "dimensions": {
        "en": "Dimensions",
        "sv": "Mått",
        "fi": "Mitat",
        "no": "Mål",
        "de": "Abmessungen",
    },
    "select_hazard_hint": {
        "en": "← select a hazard",
        "sv": "← välj en risk",
        "fi": "← valitse riski",
        "no": "← velg en fare",
        "de": "← wählen Sie eine Gefahr",
    },
    "hint_diameter": {
        "en": "Enter diameter to calculate",
        "sv": "Ange diameter för att beräkna",
        "fi": "Anna halkaisija laskentaa varten",
        "no": "Angi diameter for å beregne",
        "de": "Geben Sie den Durchmesser ein, um zu berechnen",
    },
    "hint_width_length_drip": {
        "en": "Enter width, length & drip depth",
        "sv": "Ange bredd, längd och droppdjup",
        "fi": "Anna leveys, pituus ja tiputussyvyys",
        "no": "Angi bredde, lengde og dryppdybde",
        "de": "Geben Sie Breite, Länge und Tropftiefen ein",
    },
    "hint_width_length": {
        "en": "Enter width & length to calculate",
        "sv": "Ange bredd och längd för att beräkna",
        "fi": "Anna leveys ja pituus laskentaa varten",
        "no": "Angi bredde og lengde for å beregne",
        "de": "Geben Sie Breite und Länge ein, um zu berechnen",
    },
    "system_summary": {
        "en": "System Summary",
        "sv": "Systemöversikt",
        "fi": "Järjestelmän yhteenveto",
        "no": "Systemoversikt",
        "de": "Systemübersicht",
    },
    "hazard": {
        "en": "Hazard",
        "sv": "Risk",
        "fi": "Riski",
        "no": "Fare",
        "de": "Gefahr",
    },
    "qty": {
        "en": "Qty",
        "sv": "Antal",
        "fi": "Määrä",
        "no": "Antall",
        "de": "Stück",
    },
    "nozzle": {
        "en": "Nozzle",
        "sv": "Nozzle",
        "fi": "Nozzeli",
        "no": "Dyse",
        "de": "Düse",
    },
    "flow": {
        "en": "Flow",
        "sv": "Flöde",
        "fi": "Virtaus",
        "no": "Flow",
        "de": "Durchfluss",
    },
    "total": {
        "en": "Total",
        "sv": "Totalt",
        "fi": "Yhteensä",
        "no": "Totalt",
        "de": "Summe",
    },
    "nozzles": {
        "en": "Nozzles:",
        "sv": "Munstycken:",
        "fi": "Suuttimet:",
        "no": "Dyser:",
        "de": "Düsen:",
    },
    "save_as_pdf": {
        "en": "⬇ Save as PDF",
        "sv": "⬇ Spara som PDF",
        "fi": "⬇ Tallenna PDF",
        "no": "⬇ Lagre som PDF",
        "de": "⬇ Als PDF speichern",
    },
    "save_system_summary": {
        "en": "⬇ Save System Summary",
        "sv": "⬇ Spara systemöversikt",
        "fi": "⬇ Tallenna järjestelmän yhteenveto",
        "no": "⬇ Lagre systemoversikt",
        "de": "⬇ Systemübersicht speichern",
    },
    "section_singular": {
        "en": "section",
        "sv": "sektion",
        "fi": "osio",
        "no": "seksjon",
        "de": "Abschnitt",
    },
    "section_plural": {
        "en": "sections",
        "sv": "sektioner",
        "fi": "osioita",
        "no": "seksjoner",
        "de": "Abschnitte",
    },
    "cannot_be_protected": {
        "en": "The {appliance} cannot be protected.",
        "sv": "{appliance} kan inte skyddas.",
        "fi": "{appliance} ei voida suojata.",
        "no": "{appliance} kan ikke beskyttes.",
        "de": "{appliance} kann nicht geschützt werden.",
    },
    "shelf_infeasible_title": {
        "en": "Shelf constraint infeasible",
        "sv": "Hyllkonstruktionen är inte möjlig",
        "fi": "Hyllyn rajoitus ei ole mahdollinen",
        "no": "Hyllebegrensningen er ikke mulig",
        "de": "Regalbeschränkung nicht möglich",
    },
    "shelf_infeasible_message": {
        "en": "No section layout can satisfy both the shelf angle and the c constraint. Reduce shelf overhang, increase shelf height, or reduce appliance dimensions.",
        "sv": "Ingen sektionlayout kan uppfylla både hyllvinkeln och c-kravet. Minska utstick, öka hyllhöjden eller minska apparatens mått.",
        "fi": "Yksikään osion asettelu ei voi täyttää sekä hyllyn kulmaa että c-rajoitusta. Vähennä hyllyn ulkonemaa, nosta hyllykorkeutta tai pienennä laitteen mittoja.",
        "no": "Ingen seksjonsoppsett kan tilfredsstille både hyllevinkelen og c-begrensningen. Reduser hylleutspring, øk hyllehøyde eller reduser apparatets dimensjoner.",
        "de": "Kein Abschnittslayout kann sowohl den Regalwinkel als auch die c-Beschränkung erfüllen. Reduzieren Sie den Regalüberhang, erhöhen Sie die Regalhöhe oder verringern Sie die Gerätemaße.",
    },
}

APPLIANCE_LABELS = {
    "en": {
        key: key for key in APPLIANCES
    },
    "sv": {
        "Fryer": "Fritös",
        "Fryer with drip board": "Fritös med droppbräda",
        "Griddle": "Grillplatta",
        "Gas or electric broiler": "Gasspis eller elektrisk grill",
        "Range top": "Spishäll",
        "Wok": "Wok",
        "Tilt skillet": "Hällstekpanna",
        "Circular duct": "Cirkulär kanal",
        "Rectangular duct": "Rektangulär kanal",
        "Plenum": "Plenum",
        "Plenum V-style": "Plenum V-stil",
    },
    "fi": {
        "Fryer": "Fritös",
        "Fryer with drip board": "Fritös med droppkant",
        "Griddle": "Stekbord",
        "Gas or electric broiler": "Gas- eller elgrill",
        "Range top": "Spishäll",
        "Wok": "Wok",
        "Tilt skillet": "Tiltpanna",
        "Circular duct": "Cirkulär kanal",
        "Rectangular duct": "Rektangulär kanal",
        "Plenum": "Plenum",
        "Plenum V-style": "Plenum V-stil",
    },
    "no": {
        "Fryer": "Friterer",
        "Fryer with drip board": "Friterer med dryppbrett",
        "Griddle": "Stekebord",
        "Gas or electric broiler": "Gass- eller elektrisk grill",
        "Range top": "Komfyrtopp",
        "Wok": "Wok",
        "Tilt skillet": "Vippepanne",
        "Circular duct": "Sirkulær kanal",
        "Rectangular duct": "Rektangulær kanal",
        "Plenum": "Plenum",
        "Plenum V-style": "Plenum V-stil",
    },
    "de": {
        "Fryer": "Fritteuse",
        "Fryer with drip board": "Fritteuse mit Tropfblech",
        "Griddle": "Grillplatte",
        "Gas or electric broiler": "Gas- oder Elektrogrill",
        "Range top": "Kochfeld",
        "Wok": "Wok",
        "Tilt skillet": "Schwenkpfanne",
        "Circular duct": "Rundkanal",
        "Rectangular duct": "Rechteckkanal",
        "Plenum": "Plenum",
        "Plenum V-style": "Plenum V-Stil",
    },
}


def get_translation(key, lang, **kwargs):
    text = TRANSLATIONS.get(key, {}).get(lang) or TRANSLATIONS.get(key, {}).get("en") or key
    return text.format(**kwargs) if kwargs else text


def get_appliance_label(appliance, lang):
    return APPLIANCE_LABELS.get(lang, {}).get(appliance, APPLIANCE_LABELS["en"].get(appliance, appliance))


def get_appliance_choices(lang):
    labels = APPLIANCE_LABELS.get(lang, APPLIANCE_LABELS["en"])
    choices = {"": get_translation("select_hazard_placeholder", lang)}
    choices.update({key: labels.get(key, key) for key in APPLIANCES})
    return choices


def normalize_language(value):
    return value if value in LANGUAGE_OPTIONS else "en"


