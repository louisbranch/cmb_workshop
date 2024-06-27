import nbformat
import os

def extract_markdown_cells(notebook_path, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    with open(notebook_path, 'r', encoding='utf-8') as nb_file:
        nb_content = nbformat.read(nb_file, as_version=4)
    
    markdown_cells = []
    for cell in nb_content['cells']:
        if cell['cell_type'] == 'markdown':
            markdown_cells.append(cell['source'])
    
    for idx, block in enumerate(markdown_cells, 1):
        md_file_path = os.path.join(output_folder, f"{idx}.md")
        with open(md_file_path, 'w', encoding='utf-8') as md_file:
            md_file.write(block)

    print(f"Extracted {len(markdown_cells)} markdown cells to {output_folder}")

notebook_path = 'notebook.ipynb'
output_folder = 'cmb/content/en_CA/'
extract_markdown_cells(notebook_path, output_folder)
