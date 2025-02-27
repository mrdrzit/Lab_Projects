import pandas as pd
from pyautogui import click, locateOnScreen, moveTo, hotkey
import webbrowser
import pyperclip
import time
import locale
from datetime import datetime

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8") 

def parse_deadline(date_str):
    try:
        return datetime.strptime(date_str, "%d de %B de %Y")
    except ValueError:
        return None  
    
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
COLUMN_ALREADY_NOTIFIED = "Foi notificado no grupo"

NEXT_MONTH = CURRENT_MONTH + 1 if CURRENT_MONTH < 12 else 1
CURRENT_SUMMARY_MONTHS = [MONTHS[CURRENT_MONTH], MONTHS[NEXT_MONTH]]

# Read the data
data = pd.read_csv(SHEET_URL)

# Create a new dataframe with parsed deadlines
data_with_dates = data.copy()
data_with_dates[COLUMN_APPLICATION_DEADLINE] = data_with_dates[COLUMN_APPLICATION_DEADLINE].astype(str).apply(parse_deadline)

# Filter out opportunities that have already been notified
unnotified_data = data_with_dates[data_with_dates[COLUMN_ALREADY_NOTIFIED] == 0]

# Drop rows where the deadline couldn't be parsed (NaT values)
filtered_data = unnotified_data.dropna(subset=[COLUMN_APPLICATION_DEADLINE])

# Reset index to preserve original indices as a column
filtered_data = filtered_data.reset_index()

# Add a column to identify if the deadline is in the current month
filtered_data['is_current_month'] = filtered_data[COLUMN_APPLICATION_DEADLINE].dt.strftime('%B %Y') == CURRENT_SUMMARY_MONTHS[0]

# Sort by: 1) whether it's in the current month (ascending, so False comes first), 2) deadline (ascending)
sorted_data = filtered_data.sort_values(by=['is_current_month', COLUMN_APPLICATION_DEADLINE])

# Group by opportunity name and keep the first (earliest) entry for each group
unique_opportunities = sorted_data.groupby(COLUMN_OPPORTUNITY_NAME, as_index=False).first()

# Trim the list to at most 8 items, prioritizing non-current month opportunities
if len(unique_opportunities) > 8:
    unique_opportunities = unique_opportunities.head(8)

# Get the original indices from the 'index' column
indices_to_mark = sorted(unique_opportunities['index'].tolist())

# Use the indices to retrieve the corresponding rows from the original dataframe
final_message_dataframe = data.loc[indices_to_mark]


message_parts = [f"🌟 *Oportunidades Acadêmicas - {CURRENT_SUMMARY_MONTHS[0].capitalize()} e {CURRENT_SUMMARY_MONTHS[1].capitalize()}* 🌟\n"]
current_index = 1
for index, row_content in enumerate(unique_opportunities):
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

# print(final_message)

def findtextbox() -> None:
    """click on text box"""
    try:
        webbrowser.open("https://markdownlivepreview.com/")
        # webbrowser.open("https://web.whatsapp.com/accept?code=CnrBPNWyz1Q3BVTTrpgpf6")
    except Exception:
        print("Failed to open whatsapp web")
    time.sleep(3)
    
    # Delete previous message
    hotkey('ctrl', 'a')
    hotkey('backspace')
    pyperclip.copy(final_message)
    hotkey('ctrl', 'v')
    hotkey('enter')

findtextbox()