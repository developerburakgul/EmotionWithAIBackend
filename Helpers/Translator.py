from deep_translator import GoogleTranslator

class TextTranslator:
    def __init__(self, source_lang: str = 'auto', target_lang: str = 'en'):
        self.source_lang = source_lang
        self.target_lang = target_lang

    def translate_to_english(self, text: str) -> str:
        if not text:
            raise ValueError("Text cannot be empty")

        try:
            translator = GoogleTranslator(source=self.source_lang, target=self.target_lang)
            return translator.translate(text)
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")


# 🟢 Main blok artık class'ın dışında
if __name__ == '__main__':
    translator = TextTranslator(source_lang='tr', target_lang='en')
    try:
        translated_text = translator.translate_to_english("Merhaba, nasılsın?")
        print("Translated text:", translated_text)
    except Exception as e:
        print("Error:", e)