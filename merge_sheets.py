import pandas as pd

# Pfad zur Excel-Datei
file_path = 'Literature_Proseminar_Gamification_merged_r2review.xlsx'

# Öffnen der Excel-Datei
excel_data = pd.ExcelFile(file_path)

# Relevante Sheets finden
relevant_sheets = [s for s in excel_data.sheet_names if s[0].isdigit()]

# Definiere die relevanten Felder
relevant_fields = ["Title", "Abstract", "Authors", "Publication Year", "Times Cited, All Databases"]

# DataFrame für zusammengeführte Daten
merged_data = pd.DataFrame(columns=relevant_fields)

# Daten aus jedem relevanten Sheet extrahieren und fehlende Felder mit leeren Werten füllen
for sheet in relevant_sheets:
    # Daten aus dem Sheet lesen
    data = pd.read_excel(excel_data, sheet_name=sheet)

    # Nur relevante Felder extrahieren und fehlende Felder mit leeren Werten füllen
    data_relevant = data.reindex(columns=relevant_fields, fill_value='')

    # Kombiniere die relevanten Daten in das neue DataFrame
    merged_data = pd.concat([merged_data, data_relevant], ignore_index=True)

# Entferne Duplikate
merged_data_no_duplicates = merged_data.drop_duplicates()

# Schreibe die Daten ohne Duplikate in das Ziel-Sheet
with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    merged_data_no_duplicates.to_excel(writer, sheet_name="merged results no duplicates", index=False)

print("Merging completed successfully!")
