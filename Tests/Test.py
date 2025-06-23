from Helpers.Parser import Parser
from Helpers.EmotionAnalyzer import EmotionAnalyzer
import json
from datetime import datetime


if __name__ == "__main__":
    print("✅ Parser başarıyla çalıştı.")
    # Örnek kullanım
    sample_text = """
[14.03.2025, 00:46:54] Burak Gül: Kanka napıyon ya
[14.03.2025, 00:47:54] Burak Gül: nasılsın 
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
    # 1. Parser kontrolü
    messages = Parser.parse_messages(sample_text)


    # 2. GroupMessages kontrolü
    grouped_messages = Parser.groupMessages(messages)
    
    sender1Messages = grouped_messages.get("Burak Gül", [])
    sender2Messages = grouped_messages.get("Nizamet Özkan", [])
    
    print("\n=== Burak Gül'ün Ham Mesajları ===")
    for msg in sender1Messages:
        print(f"Text: {msg.text}")
    
    print("\n=== Nizamet Özkan'ın Ham Mesajları ===")
    for msg in sender2Messages:
        print(f"Text: {msg.text}")

    # 3. Emotion Analyzer kontrolü
    analyzer = EmotionAnalyzer()
    
    print("\n=== Burak Gül'ün Analiz Sonuçları ===")
    sender1Results = analyzer.analyze_group_messages_parallel(sender1Messages)
    for i, (msg, result) in enumerate(zip(sender1Messages, sender1Results)):
        print(f"\nMesaj {i+1}:")
        print(f"Ham mesaj: {msg.text}")
        print(f"Analiz sonucu: {result.emotion.sentiments}")
    
    print("\n=== Nizamet Özkan'ın Analiz Sonuçları ===")
    sender2Results = analyzer.analyze_group_messages_parallel(sender2Messages)
    for i, (msg, result) in enumerate(zip(sender2Messages, sender2Results)):
        print(f"\nMesaj {i+1}:")
        print(f"Ham mesaj: {msg.text}")
        print(f"Analiz sonucu: {result.emotion.sentiments}")

    print("✅ Duygu analizi başarıyla tamamlandı.")
    print(f"Burak Gül mesaj sayısı: {len(sender1Results)}")
    print(f"Nizamet Özkan mesaj sayısı: {len(sender2Results)}")










