import pandas as pd
from pyautogui import click, locateOnScreen, moveTo, hotkey
import os
import pyperclip
import time
from datetime import datetime

SHEET_NAME = "nnc_oportunidades"
SHEET_ID = "1_E98ODQlImmtrDubwZU2fEWNjXBzNrP4l-AucYd07K4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
MONTHS = {1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho", 7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"}
CURRENT_MONTH = datetime.now().month
CURRENT_DAY = datetime.now().day

# Column names
COLUMN_OPPORTUNITY_NAME = "Nome da oportunidade"
COLUMN_PROMOTING_INSTITUTION = "Instituição promotora"
COLUMN_LOCATION_COUNTRY = "Local e País"
COLUMN_GRANT_OR_FEE = "Bolsa/ Recurso/ Verba concedida ou Taxa de inscrição"
COLUMN_OPPORTUNITY_TYPE = "Tipo da oportunidade"
COLUMN_TARGET_AUDIENCE = "Público-alvo"
COLUMN_WEBSITE = "Site"
COLUMN_PERIOD = "Período"
COLUMN_APPLICATION_DEADLINE = "Deadline para aplicação"
COLUMN_REQUIRED_DOCUMENTS = "Documentos necessários"

data = pd.read_csv(SHEET_URL)

deadline_list = data.loc[:, COLUMN_APPLICATION_DEADLINE]
current_summary_months = [MONTHS[CURRENT_MONTH], MONTHS[CURRENT_MONTH+1]]
summary_rows = [row if any(month in row for month in current_summary_months) else None for row in deadline_list]

message_parts = [f"🌟 *Oportunidades Acadêmicas - {MONTHS[CURRENT_MONTH].capitalize()} e {MONTHS[CURRENT_MONTH+1].capitalize()}* 🌟\n"]
current_index = 1
for index, row_content in enumerate(summary_rows):
    if row_content is not None:
        row = data.iloc[index]
        message_parts.append(f"{current_index}️⃣ *{row[COLUMN_OPPORTUNITY_NAME]}*\n"
                             f"- 🏛️ _Instituição_: {row[COLUMN_PROMOTING_INSTITUTION]}\n"
                             f"- 🌍 _Local/Pais_: {row[COLUMN_LOCATION_COUNTRY]}\n"
                             f"- 💰 _Bolsa/Taxa_: {row[COLUMN_GRANT_OR_FEE]}\n"
                             f"- 📆 _Período_: {row[COLUMN_PERIOD]}\n"
                             f"- 🗓️ _Deadline_: {row[COLUMN_APPLICATION_DEADLINE]}\n"
                             f"- 📄 _Documentos Necessários_: {row[COLUMN_REQUIRED_DOCUMENTS]}\n"
                             f"- 🌐 _Site_: {row[COLUMN_WEBSITE]}\n")
        current_index += 1

message_parts.append("⚠️ Vocês podem encontrar uma descrição com mais detalhes dessas oportunidades na seguinte planilha: https://docs.google.com/spreadsheets/d/1_E98ODQlImmtrDubwZU2fEWNjXBzNrP4l-AucYd07K4/edit?usp=sharing")
final_message = "\n".join(message_parts)

def findtextbox() -> None:
    """click on text box"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        firefox = locateOnScreen(os.path.join(dir_path, "Firefox_logo.png"))
        moveTo(firefox[0], firefox[1])
        click()
    except Exception:
        print("Firefox not found")
        exit()

    # Open web.whatsapp.com in a new tab 
    try:
        hotkey('ctrl', 't')
        pyperclip.copy("https://web.whatsapp.com/accept?code=CnrBPNWyz1Q3BVTTrpgpf6")
        hotkey('ctrl', 'v')
        hotkey('enter')
    except Exception:
        print("Failed to open whatsapp web")
        exit()
    time.sleep(10)

    try:
        location = locateOnScreen(os.path.join(dir_path, "pywhatkit_smile.png"))
        moveTo(location[0] + 150, location[1] + 5)
        click()
    except Exception:
        print("Failed to find text box")
        exit()
    
    # Delete previous message
    hotkey('ctrl', 'a')
    hotkey('backspace')
    pyperclip.copy(final_message)
    hotkey('ctrl', 'v')
    hotkey('enter')

findtextbox()