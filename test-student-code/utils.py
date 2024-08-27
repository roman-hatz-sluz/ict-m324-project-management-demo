import os
import subprocess
import time
import html
from datetime import datetime

def list_large_files(directory, size_limit_mb=1):
    large_files = []
    size_limit_bytes = size_limit_mb * 1024 * 1024
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            if file_size > size_limit_bytes:
                relative_path = os.path.relpath(file_path, directory)
                # Only keep the last two parts of the path
                shortened_path = os.path.join(*relative_path.split(os.sep)[-2:])
                large_files.append(f"{shortened_path} ({file_size / (1024 * 1024):.2f} MB)")
    return "<br>".join(sorted(large_files))

def check_folder_structure(folder_path):
    errors = []
    error_count = 0
    
    # Check for HTML files in the main directory
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    if not html_files:
        errors.append("Keine HTML Dateien im Hauptverzeichnis.")
        error_count += 1
    
    # Check for CSS files in the css folder
    css_folder = os.path.join(folder_path, 'css')
    if not os.path.isdir(css_folder):
        errors.append("CSS Ordner 'css' fehlt.")
        error_count += 1
    else:
        css_files = [f for f in os.listdir(css_folder) if f.endswith('.css')]
        if not css_files:
            errors.append("Keine CSS Dateien in 'css' Ordner.")
            error_count += 1
    
    # Check for JS files in the js folder
    js_folder = os.path.join(folder_path, 'js')
    if not os.path.isdir(js_folder):
        errors.append("Ordner 'js' fehlt.")
        error_count += 1
    else:
        js_files = [f for f in os.listdir(js_folder) if f.endswith('.js')]
        if not js_files:
            errors.append("Keine JS Dateien im 'js' Ordner.")
            error_count += 1
    
    # Check for image files in the images folder
    images_folder = os.path.join(folder_path, 'images')
    if not os.path.isdir(images_folder):
        errors.append("'images' Ordner fehlt.")
        error_count += 1
    else:
        image_files = [f for f in os.listdir(images_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if not image_files:
            errors.append("'images' Ordner existiert, aber es gibt keine Bilddateien.  ")
            error_count += 1
    
    # Check if common.css exists and is used in at least two HTML files
    common_css_path = os.path.join(css_folder, 'common.css')
    if os.path.exists(common_css_path):
        usage_count = 0
        for html_file in html_files:
            with open(os.path.join(folder_path, html_file), 'r', encoding='utf-8') as file:
                content = file.read()
                if 'common.css' in content:
                    usage_count += 1
        if usage_count < 2:
            errors.append("'common.css' existiert, wird aber nur einmal eingebunden.")
            error_count += 1
    else:
        errors.append("'common.css' fehlt im 'css' Ordner.")
        error_count += 1

    # Summary text
    summary_text = error_count.__str__() + " Fehler gefunden:<br>" + "<br>".join(errors) if errors else "Super, alle Regeln wurden eingehalten."
    
    return summary_text
def check_unused_files(folder_path):
    all_files = []
    used_files = set()

    # Gather all files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.endswith('.md'):
                all_files.append(os.path.relpath(os.path.join(root, file), folder_path))

    # Check for usage
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.html', '.js', '.css', '.php')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for target_file in all_files:
                        if target_file in content:
                            used_files.add(target_file)

    # Find unused files
    unused_files = set(all_files) - used_files
    return '\n'.join(sorted(unused_files))
