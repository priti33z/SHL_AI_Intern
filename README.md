# SHL AI Intern Assignment

## AI-Powered SHL Assessment Recommendation System

---

## Overview

This project is an AI-powered recommendation system developed as part of the SHL AI Intern Assignment.

The application recommends the most suitable SHL assessments based on a user's hiring requirements using Semantic Search (FAISS + Sentence Transformers) and generates natural language explanations using Google's Gemini LLM.

Instead of relying on keyword matching, the system understands the meaning of the user's query and returns the closest matching SHL assessments.

---

# Features

- Semantic Search using Sentence Transformers
- Fast similarity search using FAISS
- Gemini AI generated recommendation explanation
- FastAPI REST API
- SHL Product Catalog integration
- JSON API responses
- Health Check endpoint
- Easy to extend with more assessments

---

# Tech Stack

Backend
- Python
- FastAPI

Vector Search
- FAISS

Embedding Model
- Sentence Transformers
- all-MiniLM-L6-v2

LLM
- Google Gemini 1.5 Flash

Other Libraries
- Pydantic
- Pickle
- Uvicorn
- python-dotenv

---

# Project Structure

```
SHL_AI_Intern/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── retriever.py
│   ├── build_index.py
│   ├── chat_logic.py
│   ├── llm.py
│   ├── search.py
│   └── read_catalog.py
│
├── catalog/
│   └── SHL_Catalog.csv
│
├── data/
│   ├── catalog.pkl
│   └── shl.index
│
├── venv/
│
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

# How I Built This Project

## Step 1 — Project Setup

Created a new Python virtual environment.

```bash
python -m venv venv
```

Activated virtual environment.

Windows

```bash
venv\Scripts\activate
```

Installed required packages.

```bash
pip install -r requirements.txt
```

---

## Step 2 — Read SHL Assessment Catalog

The SHL product catalog was loaded from CSV.

Each assessment contains:

- Name
- Description
- URL
- Job Levels
- Categories
- Duration

Created

```
app/read_catalog.py
```

to verify the dataset.

---

## Step 3 — Generate Embeddings

Used

```
sentence-transformers
```

with model

```
all-MiniLM-L6-v2
```

Every assessment description was converted into vector embeddings.

Example

```python
model.encode(description)
```

---

## Step 4 — Build FAISS Vector Index

Created

```
app/build_index.py
```

Tasks performed

- Read catalog
- Generate embeddings
- Create FAISS Index
- Save vector database

Generated files

```
data/catalog.pkl
```

and

```
data/shl.index
```

These files are used during searching.

---

## Step 5 — Implement Semantic Search

Created

```
app/retriever.py
```

This module

- Loads embedding model
- Loads FAISS index
- Converts user query into embedding
- Finds nearest assessments
- Returns Top-5 recommendations

---

## Step 6 — Build FastAPI Backend

Created

```
app/main.py
```

API Endpoints

GET

```
/health
```

Returns

```json
{
    "status":"ok"
}
```

POST

```
/chat
```

Receives user messages and returns recommendations.

---

## Step 7 — Integrate Google Gemini

Created

```
app/llm.py
```

Configured

- API Key
- Gemini Model

Used

```python
google.generativeai
```

to generate natural language responses.

Environment variable

```
GEMINI_API_KEY
```

stored inside

```
.env
```

---

## Step 8 — Chat Logic

Created

```
app/chat_logic.py
```

Workflow

User Query

↓

Semantic Search

↓

Top Matching Assessments

↓

Gemini Prompt

↓

Natural Explanation

↓

JSON Response

---

## Step 9 — Connect Everything

Flow

```
User

↓

FastAPI

↓

Retriever

↓

FAISS

↓

Top Assessments

↓

Gemini

↓

Final Response
```

---

# API Documentation

Run server

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

Swagger UI automatically generated.

---

# API Endpoints

## Health Check

GET

```
/health
```

Response

```json
{
    "status":"ok"
}
```

---

## Chat Endpoint

POST

```
/chat
```

Request

```json
{
    "messages":[
        {
            "role":"user",
            "content":"I am hiring a Java developer with 4 years of experience."
        }
    ]
}
```

Response

```json
{
    "reply":"For a Java developer with 4 years of experience, I recommend the following SHL assessments...",
    "recommendations":[
        {
            "name":"Java 8 (New)",
            "url":"https://www.shl.com/products/product-catalog/view/java-8-new/",
            "test_type":"Knowledge & Skills"
        }
    ],
    "end_of_conversation":false
}
```

---

# Example Queries Tested

- Hiring Java Developer
- Hiring Python Developer
- Aptitude Test for Freshers
- Communication Skills Assessment
- Sales Executive Hiring
- Cognitive Ability Test
- SQL Developer
- Customer Support Assessment

---

# Challenges Faced

- Python import errors
- FastAPI module structure
- FAISS index loading
- Relative imports
- Gemini API integration
- NameError during API integration
- JSON response formatting

All issues were resolved by organizing the project into modular files and using proper package imports.

---

# Future Improvements

- Conversation memory
- Multi-turn chat
- Filters based on experience level
- Streamlit frontend
- Docker support
- Cloud deployment
- Better ranking using reranking models

---

# Installation

Clone repository

```bash
git clone <repository-url>
```

Move into project

```bash
cd SHL_AI_Intern
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create

```
.env
```

Add

```
GEMINI_API_KEY=YOUR_API_KEY
```

Run

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

# Screenshots

(Add screenshots here)

- Project Structure
- Swagger UI
- Health Endpoint
- Java Developer Response
- Freshers Aptitude Response
- Terminal Output

---

# Author

**Priti Zaware**

SHL AI Intern Assignment

2026