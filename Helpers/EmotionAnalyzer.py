import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from multiprocessing import Pool, get_context
from typing import List
from transformers import pipeline, AutoTokenizer
from Models.GroupMessage import GroupMessage
from Models.Client.GroupMessageClient import GroupMessageClient
from Models.Emotion import Emotion
import time

# Global değişken (her process'te bir kez oluşur)
_classifier = None
_tokenizer = None

def get_classifier():
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None
        )
    return _classifier

# Tokenizer'ı global olarak yükle
def get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
    return _tokenizer

def truncate_text(text, max_tokens=512):
    tokenizer = get_tokenizer()
    tokens = tokenizer.encode(text, add_special_tokens=False)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        text = tokenizer.decode(tokens)
    return text

def analyze_message_static(args):
    text, sender, start_time, end_time, count = args
    text = truncate_text(text, 512)  # Uzun mesajı kes
    classifier = get_classifier()
    result = classifier(text)[0]
    emotion = Emotion(sentiments=result)
    return GroupMessageClient(
        sender=sender,
        start_time=start_time,
        end_time=end_time,
        emotion=emotion,
        messageCount=count
    )

class EmotionAnalyzer:
    def __init__(self, num_processes=2):  # 2 veya 3 deneyebilirsin
        self.num_processes = num_processes

    def analyze_message(self, text: str) -> Emotion:
        classifier = get_classifier()
        result = classifier(text)[0]
        return Emotion(sentiments=result)

    def analyze_batch(self, messages: List) -> List[Emotion]:
        classifier = get_classifier()
        return [Emotion(sentiments=classifier(msg.text)[0]) for msg in messages]

    def analyze_messages(self, messages: List) -> List[Emotion]:
        if len(messages) < 100:
            return self.analyze_batch(messages)
        chunk_size = len(messages) // self.num_processes
        chunks = [messages[i:i + chunk_size] for i in range(0, len(messages), chunk_size)]
        with get_context("spawn").Pool(processes=self.num_processes) as pool:
            results = pool.map(self.analyze_batch, chunks)
        return [item for sublist in results for item in sublist]

    def analyze_group_messages(self, group_messages: List[GroupMessage]) -> List[GroupMessageClient]:
        results = []
        classifier = get_classifier()
        for group_message in group_messages:
            emotion = Emotion(sentiments=classifier(group_message.text)[0])
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
        start_time = time.time()
        if len(group_messages) < 100:
            result = self.analyze_group_messages(group_messages)
        else:
            args = [
                (msg.text, msg.sender, msg.start_time, msg.end_time, msg.count)
                for msg in group_messages
            ]
            with get_context("spawn").Pool(processes=self.num_processes) as pool:
                result = pool.map(analyze_message_static, args)
        end_time = time.time()
        print(f"analyze_group_messages_parallel süresi: {end_time - start_time:.2f} saniye")
        return result