from multiprocessing import Pool
from typing import List, Union
from transformers import pipeline
from Models.GroupMessage import GroupMessage
from Models.Client.GroupMessageClient import GroupMessageClient
from Models.Emotion import Emotion

class EmotionAnalyzer:
    def __init__(self, num_processes=4):
        self.num_processes = num_processes
        self.classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True
        )

    def analyze_message(self, text: str) -> Emotion:
        """Tek bir mesaj için duygu analizi yapar"""
        result = self.classifier(text)[0]
        return Emotion(sentiments=result)

    def analyze_batch(self, messages: List) -> List[Emotion]:
        """Mesaj grubunu analiz eder"""
        return [self.analyze_message(msg.text) for msg in messages]

    def analyze_messages(self, messages: List) -> List[Emotion]:
        """Birden fazla mesaj için paralel duygu analizi yapar"""
        if len(messages) < 100:  # Küçük veri setleri için normal işlem
            return self.analyze_batch(messages)
        
        # Mesajları chunk'lara böl
        chunk_size = len(messages) // self.num_processes
        chunks = [messages[i:i + chunk_size] for i in range(0, len(messages), chunk_size)]
        
        # Paralel işleme
        with Pool(processes=self.num_processes) as pool:
            results = pool.map(self.analyze_batch, chunks)
        
        # Sonuçları düzleştir
        return [item for sublist in results for item in sublist]

    def analyze_group_messages(self, group_messages: List[GroupMessage]) -> List[GroupMessageClient]:
        """GroupMessage listesi için duygu analizi yapar ve GroupMessageClient listesi döndürür"""
        results = []
        
        for group_message in group_messages:
            emotion = self.analyze_message(group_message.text)
            client_message = GroupMessageClient(
                sender=group_message.sender,
                start_time=group_message.start_time,
                end_time=group_message.end_time,
                emotion=emotion,
                messageCount=group_message.count
            )
            results.append(client_message)
            
        return results

    def analyze_group_messages_parallel(self, group_messages: List[GroupMessage]) -> List[GroupMessageClient]:
        """Büyük GroupMessage grupları için paralel duygu analizi yapar"""
        if len(group_messages) < 100:
            return self.analyze_group_messages(group_messages)
            
        # Mesajları chunk'lara böl
        chunk_size = len(group_messages) // self.num_processes
        chunks = [group_messages[i:i + chunk_size] for i in range(0, len(group_messages), chunk_size)]
        
        # Paralel işleme
        with Pool(processes=self.num_processes) as pool:
            results = pool.map(self.analyze_group_messages, chunks)
            
        # Sonuçları düzleştir
        return [item for sublist in results for item in sublist]