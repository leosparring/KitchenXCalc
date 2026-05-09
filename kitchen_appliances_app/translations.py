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
    "grid": {
        "en": "grid", "sv": "rutnät", "fi": "ruudukko", "no": "rutenett", "de": "Raster",
    },
    "max": {
        "en": "Max", "sv": "Max", "fi": "Maks.", "no": "Maks", "de": "Max.",
    },
    "limit": {
        "en": "Limit", "sv": "Gräns", "fi": "Raja", "no": "Grense", "de": "Grenze",
    },
    "cell_perimeter": {
        "en": "Cell perimeter", "sv": "Cellomkrets", "fi": "Solun ympärysmitta", "no": "Celleomkrets", "de": "Zellenumfang",
    },
    "each_section": {
        "en": "Each section", "sv": "Varje sektion", "fi": "Jokainen osio", "no": "Hver seksjon", "de": "Jeder Abschnitt",
    },
    "max_width": {
        "en": "Max width", "sv": "Max bredd", "fi": "Maks. leveys", "no": "Maks bredde", "de": "Max. Breite",
    },
    "max_length": {
        "en": "Max length", "sv": "Max längd", "fi": "Maks. pituus", "no": "Maks lengde", "de": "Max. Länge",
    },
    "max_area": {
        "en": "Max area", "sv": "Max area", "fi": "Maks. pinta-ala", "no": "Maks areal", "de": "Max. Fläche",
    },
    "max_side": {
        "en": "Max side", "sv": "Max sida", "fi": "Maks. sivu", "no": "Maks side", "de": "Max. Seite",
    },
    "area": {
        "en": "Area", "sv": "Area", "fi": "Pinta-ala", "no": "Areal", "de": "Fläche",
    },
    "distance_limit": {
        "en": "Distance limit", "sv": "Avståndsgräns", "fi": "Etäisyysraja", "no": "Avstandsgrense", "de": "Abstandsgrenze",
    },
    "upper_row": {
        "en": "Upper row", "sv": "Övre rad", "fi": "Ylärivi", "no": "Øvre rad", "de": "Obere Reihe",
    },
    "upper_rows": {
        "en": "Upper {count} rows", "sv": "Övre {count} rader", "fi": "Ylemmät {count} riviä", "no": "Øvre {count} rader", "de": "Obere {count} Reihen",
    },
    "bottom_row_drip": {
        "en": "Bottom row (drip)", "sv": "Nedre rad (dropp)", "fi": "Alarivi (tippa)", "no": "Nedre rad (drypp)", "de": "Untere Reihe (Tropfbereich)",
    },
    "position_nozzle_center": {
        "en": "Position the nozzle centrally above its section.",
        "sv": "Placera munstycket centrerat ovanför sin sektion.",
        "fi": "Sijoita suutin keskelle osion yläpuolelle.",
        "no": "Plasser dysen sentrert over seksjonen.",
        "de": "Positionieren Sie die Düse mittig über ihrem Abschnitt.",
    },
    "position_nozzle_inner": {
        "en": "Position the nozzle {distance} mm from the inner (back) edge of the section to maintain line of sight past the shelf.",
        "sv": "Placera munstycket {distance} mm från sektionens inre (bakre) kant för att behålla fri sikt förbi hyllan.",
        "fi": "Sijoita suutin {distance} mm osion sisäreunasta (takareunasta), jotta näkölinja hyllyn ohi säilyy.",
        "no": "Plasser dysen {distance} mm fra seksjonens indre (bakre) kant for å beholde fri sikt forbi hyllen.",
        "de": "Positionieren Sie die Düse {distance} mm von der inneren (hinteren) Abschnittskante entfernt, damit die Sichtlinie am Regal vorbei frei bleibt.",
    },
    "position_nozzle_inner_row": {
        "en": "Position the innermost row of nozzles {distance} mm from the inner (back) edge of the section to maintain line of sight past the shelf. All other nozzles should be placed centrally above their section.",
        "sv": "Placera den innersta raden munstycken {distance} mm från sektionens inre (bakre) kant för att behålla fri sikt förbi hyllan. Alla andra munstycken ska placeras centrerat ovanför sin sektion.",
        "fi": "Sijoita sisin suutinten rivi {distance} mm osion sisäreunasta (takareunasta), jotta näkölinja hyllyn ohi säilyy. Muut suuttimet sijoitetaan keskelle oman osionsa yläpuolelle.",
        "no": "Plasser den innerste raden med dyser {distance} mm fra seksjonens indre (bakre) kant for å beholde fri sikt forbi hyllen. Alle andre dyser skal plasseres sentrert over sin seksjon.",
        "de": "Positionieren Sie die innerste Düsenreihe {distance} mm von der inneren (hinteren) Abschnittskante entfernt, damit die Sichtlinie am Regal vorbei frei bleibt. Alle anderen Düsen sollten mittig über ihrem Abschnitt platziert werden.",
    },
    "range_nozzle_placement": {
        "en": "Nozzle placed 690 to {height} mm above its section, aiming straight down. {position}",
        "sv": "Munstycke placerat 690 till {height} mm ovanför sin sektion, riktat rakt nedåt. {position}",
        "fi": "Suutin sijoitetaan 690-{height} mm osion yläpuolelle ja suunnataan suoraan alas. {position}",
        "no": "Dyse plasseres 690 til {height} mm over seksjonen, rettet rett ned. {position}",
        "de": "Düse 690 bis {height} mm über ihrem Abschnitt platzieren, gerade nach unten ausrichten. {position}",
    },
    "abs_diameter_exceeds": {
        "en": "Diameter {value} mm exceeds maximum {limit} mm", "sv": "Diameter {value} mm överstiger max {limit} mm", "fi": "Halkaisija {value} mm ylittää maksimin {limit} mm", "no": "Diameter {value} mm overstiger maks {limit} mm", "de": "Durchmesser {value} mm überschreitet Maximum {limit} mm",
    },
    "abs_area_exceeds": {
        "en": "Area {value:.4f} m² exceeds maximum {limit} m²", "sv": "Area {value:.4f} m² överstiger max {limit} m²", "fi": "Pinta-ala {value:.4f} m² ylittää maksimin {limit} m²", "no": "Areal {value:.4f} m² overstiger maks {limit} m²", "de": "Fläche {value:.4f} m² überschreitet Maximum {limit} m²",
    },
    "abs_width_exceeds": {
        "en": "Width {value} mm exceeds maximum {limit} mm", "sv": "Bredd {value} mm överstiger max {limit} mm", "fi": "Leveys {value} mm ylittää maksimin {limit} mm", "no": "Bredde {value} mm overstiger maks {limit} mm", "de": "Breite {value} mm überschreitet Maximum {limit} mm",
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



NOZZLE_PLACEMENT_LABELS = {
    "Fryer": {
        "en": "Nozzle placed 690 to 1200 mm above the top of its section, aiming at the section center.",
        "sv": "Munstycke placeras 690 till 1200 mm ovanför sektionens ovansida och riktas mot sektionens centrum.",
        "fi": "Suutin sijoitetaan 690-1200 mm osion yläpuolelle ja suunnataan osion keskelle.",
        "no": "Dyse plasseres 690 til 1200 mm over toppen av seksjonen og rettes mot seksjonens sentrum.",
        "de": "Düse 690 bis 1200 mm über der Oberkante des Abschnitts platzieren und auf die Abschnittsmitte ausrichten.",
    },
    "Fryer with drip board": {
        "en": "Nozzle placed 690 to 1200 mm above the top of its section, aiming at the section center.",
        "sv": "Munstycke placeras 690 till 1200 mm ovanför sektionens ovansida och riktas mot sektionens centrum.",
        "fi": "Suutin sijoitetaan 690-1200 mm osion yläpuolelle ja suunnataan osion keskelle.",
        "no": "Dyse plasseres 690 til 1200 mm over toppen av seksjonen og rettes mot seksjonens sentrum.",
        "de": "Düse 690 bis 1200 mm über der Oberkante des Abschnitts platzieren und auf die Abschnittsmitte ausrichten.",
    },
    "Wok": {
        "en": "Nozzle placed 690 to 1200 mm above the wok, aiming at the center.",
        "sv": "Munstycke placeras 690 till 1200 mm ovanför woken och riktas mot centrum.",
        "fi": "Suutin sijoitetaan 690-1200 mm wokin yläpuolelle ja suunnataan keskelle.",
        "no": "Dyse plasseres 690 til 1200 mm over woken og rettes mot sentrum.",
        "de": "Düse 690 bis 1200 mm über dem Wok platzieren und auf die Mitte ausrichten.",
    },
    "Tilt skillet": {
        "en": "Nozzle placed 690 to 1200 mm above its section, aiming at the section center. Position should be at the front so that there is a clear line from the nozzle to the entire hazard area with the lid in open position.",
        "sv": "Munstycke placeras 690 till 1200 mm ovanför sin sektion och riktas mot sektionens centrum. Placeringen ska vara framtill så att det finns fri sikt från munstycket till hela riskytan med locket öppet.",
        "fi": "Suutin sijoitetaan 690-1200 mm osion yläpuolelle ja suunnataan osion keskelle. Sijoitus tehdään etureunaan, jotta suuttimelta on vapaa näkölinja koko riskialueelle kannen ollessa auki.",
        "no": "Dyse plasseres 690 til 1200 mm over seksjonen og rettes mot seksjonens sentrum. Plasseringen skal være foran slik at det er fri sikt fra dysen til hele fareområdet med lokket åpent.",
        "de": "Düse 690 bis 1200 mm über dem Abschnitt platzieren und auf die Abschnittsmitte ausrichten. Die Position sollte vorne liegen, damit bei geöffnetem Deckel eine freie Sichtlinie von der Düse zum gesamten Gefahrenbereich besteht.",
    },
    "Griddle": {
        "en": "Nozzle placed 760 to 1020 mm above its section, 0 to 50 mm from the edge, aiming at the section center.",
        "sv": "Munstycke placeras 760 till 1020 mm ovanför sin sektion, 0 till 50 mm från kanten, riktat mot sektionens centrum.",
        "fi": "Suutin sijoitetaan 760-1020 mm osion yläpuolelle, 0-50 mm reunasta, ja suunnataan osion keskelle.",
        "no": "Dyse plasseres 760 til 1020 mm over seksjonen, 0 til 50 mm fra kanten, rettet mot seksjonens sentrum.",
        "de": "Düse 760 bis 1020 mm über dem Abschnitt platzieren, 0 bis 50 mm von der Kante entfernt, auf die Abschnittsmitte ausrichten.",
    },
    "Gas or electric broiler": {
        "en": "Nozzle placed 500 to 1020 mm above its section, aiming at the section center.",
        "sv": "Munstycke placeras 500 till 1020 mm ovanför sin sektion och riktas mot sektionens centrum.",
        "fi": "Suutin sijoitetaan 500-1020 mm osion yläpuolelle ja suunnataan osion keskelle.",
        "no": "Dyse plasseres 500 til 1020 mm over seksjonen og rettes mot seksjonens sentrum.",
        "de": "Düse 500 bis 1020 mm über dem Abschnitt platzieren und auf die Abschnittsmitte ausrichten.",
    },
    "Range top": {
        "en": "Nozzle placed centrally 690 to 1020 mm above its section, aiming straight down. If there is a shelf, ensure there is a clear line from the nozzle to the entire surface area.",
        "sv": "Munstycke placeras centrerat 690 till 1020 mm ovanför sin sektion och riktas rakt nedåt. Om det finns en hylla, säkerställ fri sikt från munstycket till hela ytan.",
        "fi": "Suutin sijoitetaan keskelle 690-1020 mm osion yläpuolelle ja suunnataan suoraan alas. Jos hylly on käytössä, varmista vapaa näkölinja suuttimelta koko pinta-alalle.",
        "no": "Dyse plasseres sentrert 690 til 1020 mm over seksjonen og rettes rett ned. Hvis det finnes en hylle, må det være fri sikt fra dysen til hele overflaten.",
        "de": "Düse mittig 690 bis 1020 mm über dem Abschnitt platzieren und gerade nach unten ausrichten. Falls ein Regal vorhanden ist, eine freie Sichtlinie von der Düse zur gesamten Fläche sicherstellen.",
    },
    "Plenum": {
        "en": "Nozzle placed maximum 150 mm from the start of the plenum, 50 to 100 mm from the filters, aiming horizontally. For multiple nozzles, they must aim in the same direction with linear separation of maximum 3 m.",
        "sv": "Munstycke placeras maximalt 150 mm från plenumets början, 50 till 100 mm från filtren, riktat horisontellt. Vid flera munstycken ska de riktas åt samma håll med högst 3 m linjärt avstånd.",
        "fi": "Suutin sijoitetaan enintään 150 mm plenumosan alusta, 50-100 mm suodattimista, ja suunnataan vaakasuoraan. Useiden suutinten tulee osoittaa samaan suuntaan enintään 3 m lineaarisella etäisyydellä.",
        "no": "Dyse plasseres maksimalt 150 mm fra starten av plenumet, 50 til 100 mm fra filtrene, rettet horisontalt. Ved flere dyser skal de rettes samme vei med maksimal lineær avstand på 3 m.",
        "de": "Düse maximal 150 mm vom Beginn des Plenums und 50 bis 100 mm von den Filtern entfernt platzieren, horizontal ausrichten. Mehrere Düsen müssen in dieselbe Richtung zeigen, mit maximal 3 m linearem Abstand.",
    },
    "Plenum V-style": {
        "en": "Nozzle placed maximum 150 mm from the start of the plenum, 50 to 100 mm from the filters, aiming horizontally. For multiple nozzles, they must aim in the same direction with linear separation of maximum 3 m.",
        "sv": "Munstycke placeras maximalt 150 mm från plenumets början, 50 till 100 mm från filtren, riktat horisontellt. Vid flera munstycken ska de riktas åt samma håll med högst 3 m linjärt avstånd.",
        "fi": "Suutin sijoitetaan enintään 150 mm plenumosan alusta, 50-100 mm suodattimista, ja suunnataan vaakasuoraan. Useiden suutinten tulee osoittaa samaan suuntaan enintään 3 m lineaarisella etäisyydellä.",
        "no": "Dyse plasseres maksimalt 150 mm fra starten av plenumet, 50 til 100 mm fra filtrene, rettet horisontalt. Ved flere dyser skal de rettes samme vei med maksimal lineær avstand på 3 m.",
        "de": "Düse maximal 150 mm vom Beginn des Plenums und 50 bis 100 mm von den Filtern entfernt platzieren, horizontal ausrichten. Mehrere Düsen müssen in dieselbe Richtung zeigen, mit maximal 3 m linearem Abstand.",
    },
    "Circular duct": {
        "en": "Nozzle placed centrally in its section, 50 to 200 mm into the duct, aiming straight up.",
        "sv": "Munstycke placeras centrerat i sin sektion, 50 till 200 mm in i kanalen, riktat rakt uppåt.",
        "fi": "Suutin sijoitetaan keskelle osiota, 50-200 mm kanavan sisään, ja suunnataan suoraan ylöspäin.",
        "no": "Dyse plasseres sentrert i seksjonen, 50 til 200 mm inn i kanalen, rettet rett opp.",
        "de": "Düse mittig im Abschnitt platzieren, 50 bis 200 mm in den Kanal hinein, gerade nach oben ausrichten.",
    },
    "Rectangular duct": {
        "en": "Nozzle placed centrally in its section, 50 to 200 mm into the duct, aiming straight up.",
        "sv": "Munstycke placeras centrerat i sin sektion, 50 till 200 mm in i kanalen, riktat rakt uppåt.",
        "fi": "Suutin sijoitetaan keskelle osiota, 50-200 mm kanavan sisään, ja suunnataan suoraan ylöspäin.",
        "no": "Dyse plasseres sentrert i seksjonen, 50 til 200 mm inn i kanalen, rettet rett opp.",
        "de": "Düse mittig im Abschnitt platzieren, 50 bis 200 mm in den Kanal hinein, gerade nach oben ausrichten.",
    },
}

def get_translation(key, lang, **kwargs):
    text = TRANSLATIONS.get(key, {}).get(lang) or TRANSLATIONS.get(key, {}).get("en") or key
    return text.format(**kwargs) if kwargs else text



def get_nozzle_placement(appliance, lang):
    labels = NOZZLE_PLACEMENT_LABELS.get(appliance, {})
    return labels.get(lang) or labels.get("en") or ""

def get_appliance_label(appliance, lang):
    return APPLIANCE_LABELS.get(lang, {}).get(appliance, APPLIANCE_LABELS["en"].get(appliance, appliance))


def get_appliance_choices(lang):
    labels = APPLIANCE_LABELS.get(lang, APPLIANCE_LABELS["en"])
    choices = {"": get_translation("select_hazard_placeholder", lang)}
    choices.update({key: labels.get(key, key) for key in APPLIANCES})
    return choices


def normalize_language(value):
    return value if value in LANGUAGE_OPTIONS else "en"


