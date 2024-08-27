 #!/bin/bash

directory="./students-code"
line_length=80
line_character="-"
formatted_line=$(printf '%*s\n' "$line_length" | tr ' ' "$line_character")

for folder in "$directory"/*; do
  if [[ -d "$folder" ]]; then
    folder_name=$(basename "$folder")
    echo "process $folder_name ..."
    purifycss=$(./node_modules/.bin/purifycss  -ri $folder/**/*.css $folder/**/*.{html,js}  -o /dev/null)
    csslint=$(rm -f output.css; find "$folder"  -name '*.css' -type f -exec cat {} \; > output.css; node_modules/.bin/csslint --config=.csslint  --quiet ./output.css)
    htmlhint=$(node_modules/.bin/htmlhint --config .htmlhint "$folder")
    eslint=$(node_modules/.bin/eslint $folder)
    rm -f ./student-reports/${folder_name}.txt
    cat << EOF > ./student-reports/${folder_name}.txt
${formatted_line}
${folder}
${formatted_line}
--------- HTML Checker ---------
${htmlhint}


--------- CSS Checker ---------
${csslint}


--------- CSS Purify ---------
${purifycss}


--------- JS Checker ---------
${eslint}
EOF
 
   sleep 1
    
  fi
done

 

