import csv
import os
from pathlib import Path

# Ścieżka do pliku CSV z tabelek
csv_file = 'dane.csv'

with open(csv_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Wyciągamy slug i url, żeby ustalić ścieżkę
        slug = row['slug'].strip()
        url = row['URL (Canonical / Link)'].strip()

        # Pomijamy stronę główną lub traktujemy ją osobno
        if slug == '' or url.endswith('reklamai.lt/'):
            folder_path = Path('content')
            file_name = '_index.md'
        else:
            # Tworzymy strukturę folderów na podstawie sluga (zawsze _index.md dla poprawnych list w Blowfish)
            folder_path = Path('content') / slug
            file_name = '_index.md'

        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / file_name

        # Składamy Frontmatter dla Hugo (pojedyncze cudzysłowy dla description chronią przed cudzysłowami w treści)
        frontmatter = f"""---
title: "{row['H1']}"
slug: "{slug}"
description: '{row['meta_description']}'
robots: "{row['robots']}"
layout: "{row['layout']}"
weight: {row.get('weight', 10) or 10}
draft: {row['draft'].lower()}
---
"""
        # Zapisujemy plik .md
        with open(file_path, 'w', encoding='utf-8') as out:
            out.write(frontmatter)

print("Gotowe! Wszystkie pliki i foldery Markdown zostały wygenerowane.")
