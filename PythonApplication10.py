import pandas as pd
from datetime import datetime
import json

def clean_text(text):
    if not isinstance(text, str):
        return None
    if set(text.strip()) == {'*'}:
        return None
    return text.strip()

def parse_menu(csv_file):
    df = pd.read_csv(csv_file)
    days = df.iloc[0]
    menu = {}
    for col in range(0, len(df.columns)): 
        date_text = days.iloc[col]
        if not isinstance(date_text, str) or 'BREAKFAST' in date_text:
            continue
        date = datetime.strptime(date_text.strip(), '%d-%b-%y').strftime('%Y-%m-%d')
        breakfast_items = []
        lunch_items = []
        dinner_items = []
        current_section = None
        for idx in range(1, len(df)):
            item = clean_text(df.iloc[idx, col])
            row_header = clean_text(df.iloc[idx, 0])
            if row_header == 'BREAKFAST':
                current_section = 'breakfast'
                continue
            elif row_header == 'LUNCH':
                current_section = 'lunch'
                continue
            elif row_header == 'DINNER':
                current_section = 'dinner'
                continue
            if item:
                if current_section == 'breakfast':
                    breakfast_items.append(item)
                elif current_section == 'lunch':
                    lunch_items.append(item)
                elif current_section == 'dinner':
                    dinner_items.append(item)
        menu[date] = {
            "Breakfast": breakfast_items,
            "Lunch": lunch_items,
            "Dinner": dinner_items
        }
    
    return menu

def save_menu(menu_dict, filename='messmenu.json'):
    with open(filename, 'w') as f:
        json.dump(menu_dict, f, indent=2, ensure_ascii=False)
csv_file = r"C:\Users\aanya\Downloads\Mess Menu Sample - Sheet1.csv"
menu_dict = parse_menu(csv_file)
save_menu(menu_dict)