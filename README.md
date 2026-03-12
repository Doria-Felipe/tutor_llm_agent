# Tutor LLM Agent

A **local AI tutor for learning German** powered by Retrieval-Augmented Generation (RAG), structured grammar lessons, and automated quizzes.

The system combines **YouTube transcripts, curated vocabulary datasets, and grammar explanations** to create an interactive learning assistant that runs entirely locally.

The goal of this project is to explore **LLM agents for education**, focusing on:

* retrieval-based learning
* structured lesson generation
* automated evaluation of LLM outputs

---

## Features

### Tutor Mode

Chat with a German learning assistant that explains grammar, vocabulary, and sentence structure.

### Vocabulary Mode

Explore vocabulary grouped by topics with examples and explanations.

### Grammar Mode

Structured grammar lessons derived from real language usage.

### Quiz Mode

Automatically generated quizzes to test comprehension and reinforce learning.

---

## Quick Start

### 1. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

### 2. Start Ollama

    ```bash
    ollama run qwen2.5:3b
    ```

### 3. Run the app

    ```bash
    streamlit run app/app.py
    ```

The application will open in your browser.

---

## Architecture

The project follows a modular structure:

## Project Architecture

    ```bash
        app/ → Streamlit interface 
            app.py
            sidebar.py
            session.py
            modes/ → Learning modes (tutor, vocab, grammar, quiz) 
                tutor_mode.py
                vocab_mode.py
                grammar_mode.py
                quiz_mode.py

        src/ → Core system components
            agent/
            rag/
            llm/
            embeddings/
            quiz/
            utils/
            youtube/

        pipelines/ → Dataset generation pipelines  
            g01_grammar_lessons.py
            g02_enrich_grammar_lessons.py
            v01_topics_vocab.py
            v02_enrich_vocab.py
            v03_clean_vocab_examples.py

        data/ → Structured datasets
            raw/
            vocab/
            lessons/
            eval/

        eval/ → Evaluation framework 
            e01_generate_agent_answers.py
            e02_evaluate_ragas.py
    ```

---

### Core System Components

* **Hybrid Retrieval**
  BM25 + vector embeddings for robust information retrieval.

* **Local LLM Inference**
  Runs with Ollama using models like `qwen2.5`.

* **Lesson Generation Pipeline**
  Structured grammar lessons generated from real German content.

* **Evaluation Framework**
  RAG pipelines evaluated with **RAGAS metrics**.

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

### YouTube Transcript Collection

Used to build the learning dataset.

    ```bash
        notebooks/y01_capturing_youtube_videos.ipynb
    ```

---

### Vocabulary Dataset

    ```bash
        python pipelines/v01_topics_vocab.py
        python pipelines/v02_enrich_vocab.py
        python pipelines/v03_clean_vocab_examples.py
    ```

These scripts:

1. generate topic-based vocabulary
2. enrich entries with examples
3. clean and structure the dataset

### Grammar Lesson Generation

    ```bash
        python pipelines/g01_grammar_lessons.py
        python pipelines/g02_enrich_grammar_lessons.py
    ```

These pipelines build structured grammar explanations used by the tutor.

---

## Evaluation

The system includes an evaluation pipeline using **RAGAS** to measure response quality.

Generate answers:

    ```bash
    python eval/e01_generate_agent_answers.py
    ```

Run evaluation:

    ```bash
        python eval/e02_evaluate_ragas.py
    ```

Metrics include:

* Answer Relevancy
* Faithfulness
* Context Precision

---

## Example Workflow

1. Collect transcripts from German learning videos
2. Generate structured grammar lessons
3. Build topic-based vocabulary datasets
4. Retrieve relevant information with RAG
5. Generate explanations with a local LLM
6. Evaluate the system using RAGAS metrics

---

## Future Improvements

* lesson progression system
* spaced repetition vocabulary
* improved retrieval reranking
* richer Streamlit UI
* multi-video lesson generation

---

## Tech Stack

* **Python**
* **Streamlit**
* **LangChain**
* **ChromaDB**
* **Ollama**
* **RAGAS**
* **SentenceTransformers**

---

## License

MIT
