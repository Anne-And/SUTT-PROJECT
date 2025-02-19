import pandas as pd
from datetime import datetime
import json

def clean_text(text):
    if not isinstance(text, str):
        return None
    if set(text.strip()) == {'*'}:
        return None
    return text.strip()

def parse_menu(excel_file):
    df = pd.read_excel(excel_file, engine='openpyxl')
    df.iloc[0] = df.iloc[0].astype(str)
    days = df.iloc[0]
    
    menu = {}
    
    for col in range(0, len(df.columns)):
        date_text = str(days.iloc[col]).strip()
        if not date_text or 'BREAKFAST' in date_text:
            continue
        try:
            date = datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        except ValueError:
            continue
        
        breakfast_items, lunch_items, dinner_items = [], [], []
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
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(menu_dict, f, indent=2, ensure_ascii=False)

excel_file = r"C:\Users\aanya\Downloads\Mess Menu Sample.xlsx"
menu_dict = parse_menu(excel_file)
save_menu(menu_dict)
