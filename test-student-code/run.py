import os
import subprocess
import time
import html
from datetime import datetime
from utils import list_large_files, check_folder_structure, check_unused_files

directory = "./students-code"
line_length = 80
line_character = "-"
formatted_line = line_character * line_length

def read_file(file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    rel_file_path = os.path.join(current_dir, file_path)
    with open(rel_file_path, 'r', encoding='utf-8') as file:
        return file.read()

def count_lines(file_extension, folder_path):
    total_lines = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    total_lines += sum(1 for _ in f)
    return total_lines

def generate_html_report(folder_name, folder_path, htmlhint, htmlvalidate, csslint, purifycss, eslint, unused_files_report, js_lines, css_lines, html_lines):
    html_content = f"""
            <h2>Repository:{folder_name}</h2>
           <h3>Verwendung und Dateigrösse</h3>
            Folgende Dateien werden nicht verwendet: 
            <pre>{unused_files_report}</pre>
            Folgende Dateien sind zu gross:
            <pre>{list_large_files(folder_path)}</pre>

            <h3> Ordnerstruktur / Vorgaben</h3>
          
                {check_folder_structure(folder_path)}
  <br> <i style="font-size: 14px"> Siehe https://github.com/roman-hatz-sluz/ict-m291-vorlagen/blob/main/README.md </i> 
            
            <h3>Zeilenzählung der Dateien im Projekt</h3>
            <ul>
                <li>JavaScript-Dateien: {js_lines} Zeilen</li>
                <li>CSS-Dateien: {css_lines} Zeilen</li>
                <li>HTML-Dateien: {html_lines} Zeilen</li>
            </ul>
           
           <h3>HTML</h3>
              Testet die Code Qualität von HTML entsprechend den Vorgaben.  
            <pre>{html.escape(htmlhint)}</pre>
           <pre>{html.escape(htmlvalidate)}</pre>
            <h3>JS</h3>
             Testet die Code Qualität von JS entsprechend den Vorgaben.  
            <pre>{eslint}</pre>

           
            <h3>CSS</h3>
            Testet die Code Qualität von CSS.  
            Beispiele: "@import not allowed" oder "Expected RBRACE"
            <pre>{stylelint}</pre>
            <pre>{csslint}</pre>
            Testet, ob das CSS kompakter geschrieben werden kann. 
            <pre>{purifycss}</pre>

<br><br>   
       
    """
    return html_content

for folder in os.listdir(directory):
    folder_path = os.path.join(directory, folder)
    if os.path.isdir(folder_path):
        print(f"Processing {folder}...")

        purifycss = subprocess.run(
            ['./node_modules/.bin/purifycss', '-ri'] + 
            [f"{folder_path}/**/*.css", f"{folder_path}/**/*.html", '-o', '/dev/null'], 
            capture_output=True, text=True
        ).stdout

        csslint = subprocess.run(
            f"rm -f output.css; find {folder_path} -name '*.css' -type f -exec cat {{}} \\; > output.css; node node_modules/.bin/csslint --config=.csslint --quiet ./output.css", 
            shell=True, capture_output=True, text=True
        ).stdout

        htmlhint = subprocess.run(
            ['node_modules/.bin/htmlhint', '--config', '.htmlhint', folder_path], 
            capture_output=True, text=True
        ).stdout

        eslint = subprocess.run(
            ['node_modules/.bin/eslint', folder_path], 
            capture_output=True, text=True
        ).stdout

        
        stylelint_command = f'node_modules/.bin/stylelint "{folder_path}/**/*.css"'
        stylelint = subprocess.run(
            stylelint_command,
            shell=True,
            capture_output=True,
            text=True
        )
        stylelint_tmp = stylelint.stdout + stylelint.stderr
        stylelint = stylelint_tmp.replace('\n', '<br>')

        htmlvalidate = subprocess.run(
            ['node_modules/.bin/html-validate', folder_path], 
            capture_output=True, text=True
        ).stdout
        

        unused_files_report = check_unused_files(folder_path)

        js_lines = count_lines('.js', folder_path)
        css_lines = count_lines('.css', folder_path)
        html_lines = count_lines('.html', folder_path)
        
        report_path = f"./student-reports/{folder}.html"
        html_content = generate_html_report(folder, folder_path, htmlhint, htmlvalidate, csslint, purifycss, eslint, unused_files_report, js_lines, css_lines, html_lines)
      
        with open(report_path, 'w') as report_file:
            report_file.write(html_content)

        os.remove('output.css')
        time.sleep(1)
