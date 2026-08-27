# AI-Powered Job Search with Semantic Search + LLM Reasoning

A CLI-based AI job search application that allows users to search for jobs using natural language instead of exact keywords. The system combines **semantic search, vector embeddings, PostgreSQL/pgvector, and Gemini LLM reasoning** to find and explain the most relevant jobs.

## 🚀 Features

* 🔎 Natural-language job search
* 🧠 Semantic similarity using vector embeddings
* 🗄️ PostgreSQL + pgvector for vector storage and search
* 🤖 Gemini LLM-powered job analysis and recommendations
* 📊 Match scores based on semantic similarity
* 💬 Human-readable explanations of why jobs match
* 🔄 LLM model fallback for improved resilience
* 🖥️ Rich terminal-based CLI interface

## 🏗️ Architecture

```text
User Query
    ↓
Sentence Transformer
    ↓
Query Embedding (384 dimensions)
    ↓
PostgreSQL + pgvector
    ↓
Cosine Similarity Search
    ↓
Top-K Relevant Jobs
    ↓
Gemini LLM
    ↓
Match Analysis + Recommendation
    ↓
Rich CLI Output
```

## 🛠️ Tech Stack

| Component       | Technology                                 |
| --------------- | ------------------------------------------ |
| Language        | Python 3.13                                |
| Database        | PostgreSQL                                 |
| Vector Database | pgvector                                   |
| Embeddings      | Sentence Transformers (`all-MiniLM-L6-v2`) |
| LLM             | Google Gemini                              |
| LLM SDK         | `google-genai`                             |
| CLI UI          | Rich                                       |
| Configuration   | python-dotenv                              |

## 🧠 AI Pipeline

### 1. Query Understanding

The user enters a natural-language query such as:

```text
remote Python developer job with high salary
```

### 2. Embedding Generation

The query is converted into a 384-dimensional vector using:

```text
all-MiniLM-L6-v2
```

Job descriptions are embedded using the same model.

### 3. Semantic Search

The query embedding is compared against job embeddings stored in PostgreSQL using pgvector.

Cosine distance is used to identify the most semantically relevant jobs.

```sql
ORDER BY embedding <=> query_embedding
```

### 4. LLM Reasoning

The top matching jobs are passed to Gemini, which analyzes:

* Skill compatibility
* Job requirements
* Query relevance
* Potential gaps
* Overall match

The LLM then provides a human-readable recommendation.

## 📁 Project Structure

```text
.
├── main.py
├── setup.sql
├── setup_db.py
├── requirements.txt
├── .env.example
├── .gitignore
└── src/
    ├── ...
    └── ...
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <project-directory>
```

### 2. Create a virtual environment

```bash
python3.13 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

```env
GEMINI_API_KEY=your_gemini_api_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_search
DB_USER=postgres
DB_PASSWORD=your_password
```

**Do not commit `.env` to Git.**

### 5. Setup PostgreSQL and pgvector

Make sure PostgreSQL is running and the `pgvector` extension is installed.

Run the database setup:

```bash
python setup_db.py
```

Or execute the SQL setup manually:

```bash
psql -U postgres -d job_search -f setup.sql
```

### 6. Run the application

```bash
python main.py
```

Example:

```text
Enter job search query:
> remote python job with high salary

Searching for relevant jobs...

Top Matches

1. Senior Python Backend Developer
   Match Score: 91%

   AI Analysis:
   Strong match based on Python, backend development,
   remote work and experience requirements.
```

## 🔐 Environment Variables

| Variable         | Description           |
| ---------------- | --------------------- |
| `GEMINI_API_KEY` | Google Gemini API key |
| `DB_HOST`        | PostgreSQL host       |
| `DB_PORT`        | PostgreSQL port       |
| `DB_NAME`        | Database name         |
| `DB_USER`        | PostgreSQL username   |
| `DB_PASSWORD`    | PostgreSQL password   |

Keep credentials in `.env` and never commit them to the repository.

## 🎯 AI Skills Demonstrated

* Semantic Search
* Vector Embeddings
* Retrieval-Augmented Generation (RAG)
* LLM Integration
* Prompt Engineering
* Vector Database Design
* Cosine Similarity Search
* PostgreSQL + pgvector
* LLM Error Handling and Model Fallback
* Modular AI Application Architecture

## 📌 Example Use Cases

```text
"remote Python developer"
```

```text
"senior backend engineer with cloud experience"
```

```text
"machine learning job for someone with Python and TensorFlow"
```

```text
"high salary Java developer with remote work"
```

Unlike traditional keyword search, the system attempts to understand the **meaning and intent** of the query.

## 🔒 Git & Security

The repository includes a `.gitignore` that excludes:

```text
.env
.env.local
venv/
.venv/
__pycache__/
*.pyc
.cache/
*.log
.idea/
.vscode/
.DS_Store
```

Safe to commit:

```text
main.py
setup.py / setup_db.py
setup.sql
requirements.txt
src/
.env.example
.gitignore
README.md
```

Never commit:

```text
.env
API keys
Database passwords
Downloaded model/cache files
Virtual environments
```

## 📈 Future Improvements

* Job API/web scraping integration
* User profile/resume-based matching
* Salary normalization
* Location-aware job filtering
* Hybrid keyword + semantic search
* Job recommendation history
* Re-ranking using an LLM
* Evaluation metrics for search quality
* Web-based UI
* Automated job alerts

## 👨‍💻 Project Goal

The goal of this project is to demonstrate how **traditional information retrieval, vector databases, embeddings, and LLM reasoning can be combined into a practical end-to-end Generative AI application.**

> **Built an AI job search tool combining semantic vector search (Sentence Transformers + pgvector) with Gemini LLM reasoning to match jobs by meaning and explain why each result fits the user's query.**
