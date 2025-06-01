import re

class GeneralHelper:
    @staticmethod
    def checkParticipants(text: str, count: int = 2) -> bool:
        """ Verilen metinde kişi sayisini kontrol eder.
        Args:
            text (str): Kontrol edilecek metin.
            count (int): Beklenen kişi sayisi. Varsayilan 2.
        Returns:
            bool: Eğer metinde belirtilen kişi sayisi varsa True, yoksa False.
        """
        if text == "":
            raise ValueError(f"Text boş olamaz.")
        
        name_pattern = r"\[\d{2}\.\d{2}\.\d{4}, \d{2}:\d{2}:\d{2}\] (.*?):"
        names = re.findall(name_pattern, text)

        # Tekil kullanıcı isimlerini bul
        unique_names = set(names)
        if len(unique_names) == count:
            return True
        else:
            raise ValueError(f"Kişi sayisi {len(unique_names)} bulundu. {count} kişi olmali.")
        



try:
    with open("Helpers/MockDatas/_chat.txt", "r", encoding="utf-8") as f:
        chat_data = f.read()
    result = GeneralHelper.checkParticipants(chat_data, 2)
    print("✅ İki kişi var:", result)
except ValueError as e:
    print("❌ Hata:", e)