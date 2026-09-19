from pathlib import Path
import pandas as pd

# Wczytujemy dane z pliku CSV
csv_file = 'dane.csv'
df = pd.read_csv(csv_file)

# Usuwamy automatycznie puste kolumny "Unnamed"
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

for index, row in df.iterrows():
    slug_raw = row.get('slug')
    url_raw = row.get('URL (Canonical / Link)')

    if not pd.isna(slug_raw) and str(slug_raw).strip() == '*':
        continue
    if pd.isna(slug_raw) and (pd.isna(url_raw) or str(url_raw).strip() == ''):
        continue

    slug = str(slug_raw).strip() if not pd.isna(slug_raw) else ''
    url = str(url_raw).strip() if not pd.isna(url_raw) else ''
    layout_type = str(row.get('layout', 'page')).strip() if not pd.isna(row.get('layout')) else 'page'

    # Określanie ścieżek dla Hugo
    is_home = (slug == '' or url.endswith('reklamai.lt/'))
    if is_home:
        folder_path = Path('content')
        file_name = '_index.md'
        layout_type = 'home'
    elif layout_type == 'list' or slug in ['spauda', 'kartono-sprendimai-reklamai']:
        folder_path = Path('content') / slug
        file_name = '_index.md'
    else:
        folder_path = Path('content')
        file_name = f"{slug}.md"

    folder_path.mkdir(parents=True, exist_ok=True)
    file_path = folder_path / file_name

    def get_clean_val(col_name, default=''):
        val = row.get(col_name)
        if pd.isna(val) or str(val).strip().lower() == 'nan' or str(val).strip() == '':
            return default
        return str(val).strip().replace('"', '\\"')

    safe_h1 = get_clean_val('H1', 'UAB Primum')
    safe_description = get_clean_val('meta_description', '')
    safe_title = get_clean_val('meta_title', '')
    menu_title = get_clean_val('menu_title', '')
    robots_val = get_clean_val('robots', 'index, follow')
    page_content = get_clean_val('content', '')

    try:
        weight_val = int(float(row.get('weight', 10)))
    except ValueError:
        weight_val = 10

    draft_val = str(row.get('draft', 'false')).strip().lower()
    if draft_val not in ['true', 'false']:
        draft_val = 'false'

    # Generujemy czysty, poprawny plik Markdown
    file_content = f"""---
title: "{safe_h1}"
menu_title: "{menu_title}"
meta_title: "{safe_title}"
description: "{safe_description}"
robots: "{robots_val}"
layout: "{layout_type}"
weight: {weight_val}
draft: {draft_val}
---

{page_content}
"""

    with open(file_path, 'w', encoding='utf-8') as out:
        out.write(file_content)

print('Sukces! Pliki wygenerowane w czystym standardzie.')
