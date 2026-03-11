# Tutor LLM Agent

A local AI tutor for learning German using retrieval-augmented generation (RAG), quizzes, and structured grammar lessons.

The system combines:

* YouTube transcripts
* curated vocabulary datasets
* grammar lessons
* a hybrid retrieval pipeline

to create an interactive learning assistant.

---

## Features

### Tutor Mode

Chat with a German learning assistant that explains grammar, vocabulary, and sentence structure.

### Vocabulary Mode

Explore vocabulary organized by topic with examples and explanations.

### Grammar Mode

Structured lessons generated from real language usage.

### Quiz Mode

Automatically generated quizzes to test comprehension.

---

## Architecture

The project follows a modular structure:

```bash
app/       → Streamlit interface  
app/modes/ → Learning modes (tutor, vocab, grammar, quiz)  
src/       → Core system components  
pipelines/ → Dataset generation pipelines  
eval/      → Evaluation framework  
data/      → Structured datasets  
```

Core components include:

* Hybrid retrieval (BM25 + vector search)
* Local LLM inference
* Agent-based lesson generation
* Automated evaluation using RAGAS

---

## Running the App

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the interface:

```bash
streamlit run app/app.py
```

---

## Data Pipelines

ChromaDB dataset:

```bash
y01_capturing_youtube_videos.ipynb
```

Vocabulary dataset:

```bash
python pipelines/v01_topics_vocab.py
python pipelines/v02_enrich_vocab.py
python pipelines/v03_clean_vocab_examples.py
```

Grammar lessons:

```bash
python pipelines/g01_grammar_lessons.py
python pipelines/g02_enrich_grammar_lessons.py
```

---

## Evaluation

The system can be evaluated using automated RAG metrics:

```bash
python eval/e01_generate_agent_answers.py
python eval/e02_evaluate_ragas.py
```

---

## Future Work

* lesson progression system
* spaced repetition vocabulary
* improved retrieval reranking
* better UI interaction
