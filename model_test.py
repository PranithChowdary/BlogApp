from transformers import pipeline
sentiment_task = pipeline("sentiment-analysis",model=model_path, tokenizer=model_path)
data = ["I love you", "I hate you"]
print(a)
print(a)