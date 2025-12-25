from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

summarizer = pipeline(
    "summarization",
    model=model,
    tokenizer=tokenizer
)


def chunk_text(text, tokenizer, max_tokens=1024):
    tokens = tokenizer(text, return_tensors="pt", truncation=False)
    input_ids = tokens["input_ids"][0]

    chunks = []
    for i in range(0, len(input_ids), max_tokens):
        chunk_ids = input_ids[i:i + max_tokens]
        chunks.append(tokenizer.decode(chunk_ids, skip_special_tokens=True))

    return chunks


def get_summary(text_to_summarize, tokenizer=tokenizer):
    chunks = chunk_text(text_to_summarize, tokenizer)

    summaries = [
        summarizer(chunk, max_length=700, min_length=100, do_sample=False)[0]["summary_text"]
        for chunk in chunks
    ]

    return " ".join(summaries)
