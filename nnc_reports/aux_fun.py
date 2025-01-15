import requests as req
import pandas as pd

SHEET_NAME = "nnc_oportunidades"
SHEET_ID = "1_E98ODQlImmtrDubwZU2fEWNjXBzNrP4l-AucYd07K4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:xslx&sheet={SHEET_NAME}"

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

meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
data = pd.read_excel(SHEET_URL)

deadline_list = data.loc[:, COLUMN_APPLICATION_DEADLINE]
