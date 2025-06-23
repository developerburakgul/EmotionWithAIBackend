from datetime import datetime
from typing import Dict, List
import unicodedata
from Constants.DateFormats import WHATSAPP_DATE_FORMAT

# Ek olarak:
ALTERNATIVE_WHATSAPP_DATE_FORMAT = "%d.%m.%Y %H:%M:%S"

from Helpers.FormatDate import format_datetime
from Helpers.MessageGroupManager import MessageGroupManager
from Models.GroupMessage import GroupMessage
from Models.Message import Message


class Parser:

    @staticmethod
    def removeControlCharacters(input_text: str) -> str:
        """Metin string'inden kontrol karakterlerini temizle."""
        return ''.join(c for c in input_text if not unicodedata.category(c).startswith('C'))

    @staticmethod
    def parse_messages(input_text: str) -> List[Message]:
        """WhatsApp formatındaki mesajları metin string'inden ayrıştır ve Message modeli olarak döndür.
        Format: [DD.MM.YYYY HH:MM:SS] Sender: Message

        Raises:
            ValueError: Mesaj formatı geçersiz olduğunda veya parse edilemediğinde
        """
        messages = []
        for line in input_text.splitlines():
            line = Parser.removeControlCharacters(line.strip())
            if not line:  # Boş satırları atla
                continue

            try:
                # Mesaj formatını kontrol et: [tarih] gönderici: metin
                if not (line.startswith('[') and '] ' in line and ': ' in line):
                    continue  # Geçersiz format, bu satırı atla

                # WhatsApp formatını parse et
                timestamp_str, rest = line.split("] ", 1)
                timestamp_str = timestamp_str[1:]  # Başındaki [ karakterini kaldır
                sender, text = rest.split(": ", 1)

                # Tarih formatını parse et
                try:
                    timestamp = datetime.strptime(timestamp_str, WHATSAPP_DATE_FORMAT)
                except ValueError:
                    try:
                        timestamp = datetime.strptime(timestamp_str, ALTERNATIVE_WHATSAPP_DATE_FORMAT)
                    except ValueError:
                        continue  # Tarih formatı uyuşmazsa satırı atla

                # Özel durumları filtrele
                if any(phrase in text.lower() for phrase in [
                    "sticker omitted",
                    "voice call",
                    "view once message"
                ]):
                    continue

                messages.append(Message(
                    timestamp=format_datetime(timestamp),  # ISO 8601 formatında string
                    sender=sender,
                    text=text
                ))
            except (ValueError, IndexError) as e:
                # Hatalı satırı atla, loglama yapılabilir
                print(f"Uyarı: Geçersiz mesaj formatı atlandı: {line}. Hata: {str(e)}")
                continue

        if not messages:
            raise ValueError("Hiçbir geçerli mesaj bulunamadı.")

        return messages
    

    @staticmethod 
    def groupMessages(raw_messages: List[Message]) -> Dict[str, List[GroupMessage]]:
        """Mesajları 5 dakikalık zaman aralığına göre gruplar
        
        Returns:
            Dict[str, List[GroupMessage]]: Gönderici bazlı gruplanmış mesajlar
        """
        # Benzersiz gönderici listesini oluştur
        senders = set(msg.sender for msg in raw_messages)
        
        # Her gönderici için boş liste içeren sözlük oluştur
        groups: Dict[str, List[GroupMessage]] = {
            sender: [] for sender in senders
        }
        current_group = None

        for msg in raw_messages:
            if not current_group or not current_group.can_append(msg):
                if current_group:
                    groups[current_group.sender].append(current_group.to_group_message())
                current_group = MessageGroupManager(msg)
            else:
                current_group.append_message(msg)

        if current_group:
            groups[current_group.sender].append(current_group.to_group_message())

        return groups
# Models/Message.py
        
if __name__ == "__main__":
    print("✅ Parser başarıyla çalıştı.")
    # Örnek kullanım
    sample_text = """
    [14.03.2025, 00:46:54] Burak Gül: Kanka napıyon ya
[28.03.2025, 20:48:38] Nizamet Özkan: https://teams.live.com/l/invite/FEAJ7YsNpdlRe-tjAY
[28.03.2025, 20:53:41] Burak Gül: kanka teams hesabı ayarlaryıp geliyom hemen
[3.04.2025, 21:17:47] Nizamet Özkan: Yayin yok mu
[3.04.2025, 21:29:57] Nizamet Özkan: Alooo
[3.04.2025, 21:32:14] Burak Gül: Kanka sivastayom
[3.04.2025, 21:32:35] Nizamet Özkan: Unuttular yayini hala baslamadi xd
[3.04.2025, 21:32:54] Burak Gül: Yok be kanka
[3.04.2025, 21:33:04] Burak Gül: Gündeö karışık diye sonra
[3.04.2025, 21:33:20] Nizamet Özkan: Nasil yani
[3.04.2025, 21:34:19] Burak Gül: Şimdi yapmıycaz erteleyelim dedik
‎[3.04.2025, 22:01:11] Nizamet Özkan: ‎sticker omitted
[25.04.2025, 21:28:54] Nizamet Özkan: Tunay abi nasildi
[25.04.2025, 23:11:28] Burak Gül: Girmedim kral
‎[25.04.2025, 23:26:00] Nizamet Özkan: ‎sticker omitted
[1.05.2025, 21:18:18] Nizamet Özkan: Geldim yayina kgg :D
[1.05.2025, 21:19:53] Burak Gül: Olum gerildim hdjdjd
[1.05.2025, 21:20:38] Nizamet Özkan: DDGDASGDADGG
[1.05.2025, 21:20:42] Nizamet Özkan: Devaam
[1.05.2025, 22:06:22] Nizamet Özkan: Kafa yaktirmak istersen yayin sinuna dogru build settingsden swift6 acip build denettir :D tum swift6 checkleride minimaldan complete alsin
[1.05.2025, 22:06:50] Burak Gül: Yok şuan kafanyakmaya gerek yok
[1.05.2025, 22:06:54] Nizamet Özkan: GEVDHDHDBHDHD
[19.05.2025, 19:50:39] Nizamet Özkan: Sa
[19.05.2025, 19:50:47] Burak Gül: As kanka
[19.05.2025, 19:50:51] Nizamet Özkan: Baba içerde
[19.05.2025, 19:50:52] Nizamet Özkan: ;)
[19.05.2025, 19:51:22] Burak Gül: Ne içerisi kanka
[19.05.2025, 19:51:23] Burak Gül: Anlamadım
[19.05.2025, 19:51:34] Nizamet Özkan: İc :)
[19.05.2025, 19:51:43] Burak Gül: Hdjdjdjdjjd
[19.05.2025, 19:51:47] Burak Gül: Kanka bende sessizde
[19.05.2025, 19:51:50] Burak Gül: Farketmedim
[19.05.2025, 19:51:53] Nizamet Özkan: BDBBDBDHDBDBDJD
[19.05.2025, 19:52:08] Burak Gül: Boş kanka zaten ‎<This message was edited>
[19.05.2025, 19:52:26] Burak Gül: ‎You sent a view once message. For added privacy, you can only open it on your phone.
[19.05.2025, 19:52:47] Nizamet Özkan: OOOOOOOO
[19.05.2025, 19:52:49] Nizamet Özkan: HO
[19.05.2025, 19:53:07] Burak Gül: Eyvallah
[19.05.2025, 19:53:11] Burak Gül: 😂
[25.05.2025, 22:04:51] Nizamet Özkan: ‎Missed voice call. ‎Click to call back
[25.05.2025, 22:06:53] Burak Gül: Kanka metrodayım
[25.05.2025, 22:07:01] Nizamet Özkan: Oh okeyy
[25.05.2025, 22:07:08] Nizamet Özkan: Muhabbete aramistim
"""
    messages = Parser.parse_messages(sample_text)
    grouped_messages = Parser.groupMessages(messages)
    
    # İstenilen kullanıcıların mesajlarını görüntüle
    for sender, msgs in grouped_messages.items():
        print(f"{sender} Mesajları: {len(msgs)}")
        for msg in msgs:
            print(f"{msg.start_time} - {msg.end_time} | {msg.sender}: {msg.text}")

