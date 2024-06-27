import os
import re
from IPython.display import display, Markdown

class I18N:
    def __init__(self, base_path="content", images_url='', default_lang="en_CA"):
        self.base_path = base_path
        self.images_url = images_url
        self.current_lang = default_lang

    def set_lang(self, lang):
        self.current_lang = lang

    def load_markdown(self, filename):
        """Load Markdown file for the current language setting."""
        filepath = os.path.join(self.base_path, self.current_lang, f"{filename}.md")
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Warning: File not found for {filepath}")
            return ""

    def display_markdown(self, filename):
        """Display Markdown content in the Jupyter notebook."""
        try:
            from google.colab import output # type: ignore
            output.no_vertical_scroll()
        except ImportError:
            pass

        md_content = self.load_markdown(filename)
        if self.images_url != "":
            md_content = re.sub(r'<img src="media/', f'<img src="{self.images_url}/', md_content)

        display(Markdown(md_content))

# Create a default instance of I18N that can be imported and used elsewhere
i18n = I18N()