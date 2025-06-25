# EmotionWithAIBackend

A FastAPI backend for WhatsApp chat and single-message emotion analysis using transformer models and translation APIs.

**Model Used:**  
This project uses the [`j-hartmann/emotion-english-distilroberta-base`](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) transformer model for emotion classification.

## Features

- Analyze emotions in WhatsApp chat exports (multi-participant, Turkish or other languages supported)
- Analyze emotion for a single message
- Automatic translation to English before emotion analysis
- RESTful API endpoints

## Requirements

- Python 3.8+
- [Google Cloud Translation API credentials](https://cloud.google.com/translate/docs/setup)
- (Optional) DeepL or other translation API keys if you want to extend translation support

## Setup

1. **Clone the repository:**

   ```sh
   git clone <https://github.com/developerburakgul/EmotionWithAIBackend.git>
   cd EmotionWithAIBackend
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud Translation API credentials:**

   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a service account and download the JSON credentials file.
   - Place the credentials file at `Secret/google-credentials.json`.
   - Make sure the path in [`Secret/consts.py`](Secret/consts.py) matches your credentials file location:
     ```python
     GOOGLE_TRANSLATE_API_KEY = "/absolute/path/to/Secret/google-credentials.json"
     ```

5. **(Optional) Update `.gitignore` to avoid committing secrets:**
   - The `.gitignore` already ignores the `secret/` directory.

## How it works

1. **Message Parsing:**  
   WhatsApp chat text is parsed into individual messages and participants.

2. **Message Grouping:**  
   Messages are grouped by sender and time intervals for meaningful analysis.

3. **Translation:**  
   Each group of messages is translated to English using the Google Cloud Translation API.

4. **Emotion Analysis:**  
   The translated message groups are analyzed using the transformer model  
   **Model:** [`j-hartmann/emotion-english-distilroberta-base`](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base)

5. **Results:**  
   The API returns a structured JSON with emotion results for each participant and message group.

---

### WhatsApp Chat Emotion Analysis Endpoint (`/api/v1/analyze/whatsapp`)

This endpoint processes WhatsApp chat exports as follows:

- **Parsing:** The raw WhatsApp chat text is parsed into individual messages and participants.
- **Grouping:** Messages are grouped by sender and by time intervals for context-aware analysis.
- **Translation:** Each group of messages is translated to English (if not already in English) using the Google Cloud Translation API.
- **Emotion Analysis:** The translated message groups are analyzed using the `j-hartmann/emotion-english-distilroberta-base` transformer model.
- **Response:** The API returns a structured JSON with emotion results for each participant and message group.

---

## Running the API

Start the FastAPI server using `uvicorn`:

```sh
uvicorn main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## API Endpoints

### 1. Get Model Max Input Size

- **GET** `/api/v1/model/max-input-size`
- Returns the maximum input size (tokens) supported by the emotion model.

### 2. WhatsApp Chat Emotion Analysis

- **POST** `/api/v1/analyze/whatsapp`
- **Body:**
  ```json
  {
    "text": "<Paste your WhatsApp chat export here>"
  }
  ```
- **Response:** Returns emotion analysis for each participant, grouped by time.

### 3. One-Time (Single Message) Emotion Analysis

- **POST** `/api/v1/analyze/one-time`
- **Body:**
  ```json
  {
    "text": "Your message here"
  }
  ```
- **Response:** Returns emotion analysis for the message.

## Testing

You can run the test script in [`Tests/Test.py`](Tests/Test.py) to check the parser and emotion analyzer logic:

```sh
python Tests/Test.py
```

## Notes

- Make sure your Google Cloud credentials file is valid and the path is correct.
- The translation API is required for non-English messages.
- For production, consider securing your API endpoints.

## License

MIT License (or specify your license here)
