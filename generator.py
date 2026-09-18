from pathlib import Path
import pandas as pd

# Wczytujemy dane z pliku CSV
csv_file = 'dane.csv'
df = pd.read_csv(csv_file)

for index, row in df.iterrows():
    slug_raw = row.get('slug')
    url_raw = row.get('URL (Canonical / Link)')

    # Pomijamy puste wiersze lub gwiazdki
    if pd.isna(slug_raw) or not str(slug_raw).strip() or str(slug_raw).strip() == '*':
        continue

    slug = str(slug_raw).strip()
    url = str(url_raw).strip() if not pd.isna(url_raw) else ''

    layout_type = (
        str(row.get('layout', 'page')).strip()
        if not pd.isna(row.get('layout'))
        else 'page'
    )

    # 1. Obsługa strony głównej (Homepage)
    if slug == '' or url.endswith('reklamai.lt/'):
        folder_path = Path('content')
        file_name = '_index.md'
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / file_name
    # 2. Obsługa stron typu 'list' (kategorie główne, np. spauda, kartono-sprendimai-reklamai)
    elif layout_type == 'list' or slug in ['spauda', 'kartono-sprendimai-reklamai']:
        folder_path = Path('content') / slug
        folder_path.mkdir(parents=True, exist_ok=True)
        file_name = '_index.md'
        file_path = folder_path / file_name
    # 3. Zwykłe podstrony jako pojedyncze pliki .md w folderze content/ (zapobiega 404)
    else:
        folder_path = Path('content')
        folder_path.mkdir(parents=True, exist_ok=True)
        file_name = f"{slug}.md"
        file_path = folder_path / file_name

    # Bezpieczne pobieranie pól tekstowych
    safe_h1 = (
        str(row.get('H1', '')).replace('"', '\\"')
        if not pd.isna(row.get('H1'))
        else ''
    )
    safe_description = (
        str(row.get('meta_description', '')).replace('"', '\\"')
        if not pd.isna(row.get('meta_description'))
        else ''
    )
    safe_title = (
        str(row.get('meta_title', '')).replace('"', '\\"')
        if not pd.isna(row.get('meta_title'))
        else ''
    )
    menu_title = (
        str(row.get('menu_title', '')).replace('"', '\\"')
        if not pd.isna(row.get('menu_title'))
        else ''
    )

    # Waga (weight)
    weight_val = row.get('weight', 10)
    try:
        weight_val = (
            int(float(weight_val))
            if not pd.isna(weight_val) and str(weight_val).strip() != ''
            else 10
        )
    except ValueError:
        weight_val = 10

    # Draft
    draft_val = str(row.get('draft', 'false')).strip().lower()
    if draft_val not in ['true', 'false']:
        draft_val = 'false'

    # TREŚĆ (content) z pliku CSV
    page_content = (
        str(row.get('content', ''))
        if not pd.isna(row.get('content'))
        else ''
    )

    # Składamy Frontmatter oraz wklejamy właściwą treść pod spodem
    # Dodajemy layout i type, aby motyw Hugo poprawnie wyświetlił treść w _index.md
    file_content = f"""---
title: "{safe_h1}"
slug: "{slug}"
menu_title: "{menu_title}"
meta_title: "{safe_title}"
description: "{safe_description}"
robots: "{row.get('robots', 'index, follow')}"
layout: "{layout_type}"
weight: {weight_val}
draft: {draft_val}
---

{page_content}
"""

    # Zapisujemy plik .md z treścią
    with open(file_path, 'w', encoding='utf-8') as out:
        out.write(file_content)

print(
    'Sukces! Wszystkie pliki wygenerowane poprawnie, struktura dostosowana pod Hugo.'
)
