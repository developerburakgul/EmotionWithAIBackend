from Helpers.Parser import Parser
from Helpers.EmotionAnalyzer import EmotionAnalyzer
import json
from datetime import datetime


if __name__ == "__main__":
    print("✅ Parser başarıyla çalıştı.")
    # Örnek kullanım
    sample_text = """
[14.03.2025, 00:46:54] Burak Gül: Kanka napıyon ya
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










