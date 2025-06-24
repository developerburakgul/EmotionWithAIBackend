import time
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.cloud import translate_v2 as gcloud_translate
from Secret.consts import GOOGLE_TRANSLATE_API_KEY

class TextTranslator:
    def __init__(self, source_lang: str = 'auto', target_lang: str = 'en'):
        self.source_lang = source_lang
        self.target_lang = target_lang

    def translate_to_english(self, text: str) -> str:
        if not text:
            raise ValueError("Text cannot be empty")
        try:
            translator = GoogleTranslator(source=self.source_lang, target=self.target_lang)
            result = translator.translate(text)
            time.sleep(0.1)  # Google'a yüklenmemek için küçük gecikme
            return result
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")

    def translate_messages_parallel(self, messages, max_workers=2):  # 2 thread ile sınırla
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_msg = {executor.submit(self.translate_to_english, msg.text): msg for msg in messages}
            for future in as_completed(future_to_msg):
                msg = future_to_msg[future]
                try:
                    msg.translated_text = future.result()
                except Exception as e:
                    msg.translated_text = msg.text  # Hata olursa orijinal metni kullan
        return messages


class GoogleCloudTextTranslator:
    def __init__(self, source_lang: str = 'auto', target_lang: str = 'en'):
        self.source_lang = source_lang
        self.target_lang = target_lang
        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_TRANSLATE_API_KEY
        self.client = gcloud_translate.Client()

    def translate_to_english(self, text: str) -> str:
        if not text:
            raise ValueError("Text cannot be empty")
        try:
            if self.source_lang == 'auto':
                # source_language parametresini göndermiyoruz, otomatik algılar
                result = self.client.translate(
                    text, target_language=self.target_lang
                )
            else:
                result = self.client.translate(
                    text, source_language=self.source_lang, target_language=self.target_lang
                )
            return result['translatedText']
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")

    def translate_messages_parallel(self, messages, max_workers=2):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_msg = {executor.submit(self.translate_to_english, msg.text): msg for msg in messages}
            for future in as_completed(future_to_msg):
                msg = future_to_msg[future]
                try:
                    msg.translated_text = future.result()
                except Exception:
                    msg.translated_text = msg.text
        return messages

    def translate_messages_batch(self, messages):
        texts = [msg.text for msg in messages]
        try:
            results = self.client.translate(texts, target_language=self.target_lang)
            for msg, translation in zip(messages, results):
                msg.translated_text = translation['translatedText']
        except Exception as e:
            for msg in messages:
                msg.translated_text = msg.text
        return messages


# 🟢 Main blok artık class'ın dışında
if __name__ == '__main__':
    translator = TextTranslator(source_lang='tr', target_lang='en')
    try:
        translated_text = translator.translate_to_english("Merhaba, nasılsın?")
        print("Translated text:", translated_text)
    except Exception as e:
        print("Error:", e)