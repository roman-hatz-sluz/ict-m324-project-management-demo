# one long md files for all groups, split in files, only executed once

input_file = '../../review24.md'

# Read the entire content of the input file
with open(input_file, 'r') as file:
    content = file.read()

# Split the content by the marker '--'
sections = content.split('--')

for section in sections:
    if section.strip():
        lines = section.strip().split('\n')
        if len(lines) > 1:
            # The first line after the marker is the filename
            filename = f"{lines[0].strip()}.txt"
            # The rest is the content of the new file
            file_content = '\n'.join(lines[1:]).strip()
            # Write to the new file
            with open(filename, 'w') as new_file:
                new_file.write(f"{filename}\nQualitatives Feedback:\n\n{file_content}")
