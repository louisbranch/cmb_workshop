from IPython.core.magic import register_cell_magic

@register_cell_magic
def skip_on_error(line, cell):
    try:
        exec(cell)
    except Exception as e:
        print(f"Error: {e}")