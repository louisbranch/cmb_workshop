import os
import re
import json
from IPython.display import display, Markdown

class I18N:
    _instance = None  # Private class variable to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(I18N, cls).__new__(cls)
        return cls._instance

    def __init__(self, base_path="content", images_url='', locale="en_CA", translations_path="translations"):
        # Initialize only if it hasn't been done for the singleton instance
        if not hasattr(self, 'initialized'):
            self.base_path = base_path
            self.images_url = images_url
            self.locale = locale
            self.translations_path = translations_path
            self.translations = self.load_translations()
            self.initialized = True  # Avoid reinitializing in case of multiple instantiation

            # Set locale, which also loads translations
            self.set_locale(locale)

    def load_translations(self):
        filepath = os.path.join(self.translations_path, f"{self.locale}.json")
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Warning: Translation file not found for locale {self.locale}. Using default (en_CA).")
            return {}

    def gettext(self, key):
        return self.translations.get(key, key)

    def set_locale(self, locale):
        """Update the locale and reload translations."""
        self.locale = locale
        self.translations = self.load_translations()
        
    def load_markdown(self, filename):
        """Load Markdown file for the current language setting."""
        filepath = os.path.join(self.base_path, self.locale, f"{filename}.md")
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