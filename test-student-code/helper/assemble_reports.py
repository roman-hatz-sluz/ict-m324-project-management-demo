import os
import glob
from datetime import datetime

# Directories
dir_excel = '../../__ignore/2024/excel'
dir_txt = '../../__ignore/2024/qualitative'
dir_code = '../../__ignore/2024/code-report'
output_path = '../../__ignore/2024/reports'
styles_path = '../../test-student-code/styles.css'
image_path = '../../test-student-code/image.html'

# Execute gen_excel_reports.py
exec(open("gen_excel_reports.py").read())

# Helper function to read file content
def read_file_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

# Read CSS styles
styles_content = read_file_content(styles_path)

# Process each HTML file in dir_excel
for excel_file in glob.glob(os.path.join(dir_excel, '*.html')):
    group_name = os.path.splitext(os.path.basename(excel_file))[0]
    
    # Find corresponding files in other directories
    txt_file = glob.glob(os.path.join(dir_txt, f'{group_name}*'))[0]
    code_file = glob.glob(os.path.join(dir_code, f'{group_name}*'))[0]
    
    # Read contents of the files
    excel_content = read_file_content(excel_file)
    txt_content = read_file_content(txt_file).replace('\n', '<br>')
    code_content = read_file_content(code_file)
    
    # Create HTML header
    header = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{group_name} - Bewertung Projektarbeit LBV_M291</title>
        <style>
            {styles_content}
        </style>
    </head>
    <body>
        <div class="container">
          <div class="header">  
            <div class="timestamp">{datetime.now().strftime("%Y-%m-%d %H:%M")} - Projektarbeit LBV M291 - BBZW Sursee - Roman Hatz - MMA21</div>
            { read_file_content(image_path)}
            <h2>Gruppe: {group_name}</h2>
            Bewertung der Projektarbeit Modul 291 "Oberflächen (UIs) mit Webtechnologien entwickeln"
          </div>
    """
    
    # Merge contents with headings
    merged_content = f"""
    {header}
    <h1>Bewertung</h1>
    {excel_content}
    <br><br>
    <h1>Qualitatives Feedback</h1>
    {txt_content}
    <br><br>
    <h1>Code Report (Code Bewertung)</h1>
    {code_content}
    </div></body></html>
    """
    
    # Write to new HTML file in output_path
    output_file = os.path.join(output_path, f'{group_name}-bewertung.html')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(merged_content)
