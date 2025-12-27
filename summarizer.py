from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re

tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

def get_summary(text_to_summarize, max_summary_length=150):
    if len(text_to_summarize.strip()) < 50:
        raise ValueError("Text too short to summarize.")

    text_to_summarize = re.sub(r"\s+", " ", text_to_summarize)

    # Tokenize without truncation
    inputs = tokenizer(text_to_summarize, return_tensors="pt", truncation=False)
    input_ids = inputs["input_ids"][0]

    summaries = []

    for i in range(0, len(input_ids), 1024):
        chunk_ids = input_ids[i:i + 1024]

        chunk_inputs = {
            "input_ids": chunk_ids.unsqueeze(0),
            "attention_mask": torch.ones_like(chunk_ids).unsqueeze(0)
        }

        summary_ids = model.generate(
            **chunk_inputs,
            max_length=max_summary_length,
            min_length=50,
            do_sample=False
        )

        summaries.append(
            tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        )

    return " ".join(summaries)


# def chunk_text(text, tokenizer, max_tokens=1024):
#     tokens = tokenizer(text, return_tensors="pt", truncation=False)
#     input_ids = tokens["input_ids"][0]
#
#     chunks = []
#     for i in range(0, len(input_ids), max_tokens):
#         chunk_ids = input_ids[i:i + max_tokens]
#         chunks.append(tokenizer.decode(chunk_ids, skip_special_tokens=True))
#
#     return chunks
#
#
# def get_summary(text_to_summarize, tokenizer=tokenizer):
#     chunks = chunk_text(text_to_summarize, tokenizer)
#
#     summaries = [
#         summarizer(chunk, max_length=700, min_length=100, do_sample=False)[0]["summary_text"]
#         for chunk in chunks
#     ]
#
#     return " ".join(summaries)
