# 🤖 GenAI Student & Career Assistant

### Codomax Digital Solutions Internship — Module 6: GenAI Capstone Project

An AI-powered Student & Career Assistant that combines Large Language Models, Prompt Engineering, RAG, Embeddings, Vector Databases, AI Agents, and Tool Calling into a single interactive application.

---

## 🌐 Live Demo

🚀 Try the application:

https://genai-student-career-assistant.streamlit.app/

---

## 🎯 Project Overview

The GenAI Student & Career Assistant is designed to help users with:

- 📚 Study and learning assistance
- 💼 Career guidance
- 💻 Programming and coding questions
- 🤖 Generative AI concepts
- 📄 Questions about uploaded documents
- 📝 Task management
- 🧮 Mathematical calculations

The application uses an AI agent that understands the user's request, decides whether a tool or knowledge retrieval is required, executes the appropriate action, and generates a final response.

---

## ✨ Key Features

### 🧠 Large Language Model

Uses a Hugging Face Inference API with:

**Model:** `openai/gpt-oss-120b:fastest`

The LLM generates natural-language responses and processes retrieved context and tool results.

### ✨ Prompt Engineering

A structured system prompt guides the assistant to:

- Understand user intent
- Provide clear and practical responses
- Use tools when required
- Use retrieved document context
- Avoid unsupported claims
- Handle multiple requested actions

### 📚 Retrieval-Augmented Generation (RAG)

The application supports document-based question answering.

RAG Pipeline:

```text
PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Semantic Retrieval
    ↓
Relevant Context
    ↓
LLM
    ↓
Grounded Answer
```

### 📄 Chat With Your Documents

Users can upload a PDF through the Streamlit interface.

The application:

1. Extracts text from the PDF
2. Splits the text into chunks
3. Generates embeddings
4. Stores chunks in ChromaDB
5. Retrieves relevant information
6. Provides retrieved context to the AI agent
7. Generates an answer using the LLM

The application only processes documents explicitly uploaded by the user.

### 🤖 AI Agent

The AI agent understands the user's request and decides which action is required.

```text
User Request
     ↓
Understand Intent
     ↓
AI Agent Decision
     ↓
┌──────────────┬──────────────┬──────────────┐
│              │              │
RAG Search   Calculator   Task Manager
│              │              │
└──────────────┴──────────────┘
     ↓
Process Result
     ↓
Final AI Response
```

---

## 🛠️ Available Tools

### 🧮 Calculator

Performs mathematical calculations.

Example:

```text
125 * 32
```

### 📝 Add Task

Adds a task to the task manager.

Example:

```text
Add a task called Complete my GenAI capstone project
```

### 📋 List Tasks

Displays the tasks currently stored by the application.

### 🗑️ Remove Task

Removes a task using its task number.

### 📚 Knowledge Search

Searches available knowledge sources for relevant information.

The search can use:

- Built-in knowledge
- Uploaded PDF documents

---

## 🔄 Complete Agent Workflow

```text
👤 User Request
       ↓
🧠 Understand Request
       ↓
✨ Prompt Processing
       ↓
🤖 AI Agent Decision
       ↓
┌───────────────┬────────────────┬────────────────┐
│               │                │
💬 LLM        📚 RAG           🛠️ Tools
│               │                │
│          PDF Retrieval     Calculator
│          ChromaDB          Task Manager
│          Context           Other Actions
│               │                │
└───────────────┴────────────────┴────────────────┘
       ↓
📊 Process Results
       ↓
🤖 Generate Final Response
       ↓
💬 User
```

---

## 🧩 Technologies Used

- Python
- Streamlit
- Hugging Face
- LLM APIs
- Sentence Transformers
- ChromaDB
- PyPDF
- Embeddings
- Retrieval-Augmented Generation
- Function Calling
- AI Agents
- Google Colab
- GitHub

---

## 🔐 Security

The Hugging Face API token is stored securely using Streamlit Secrets.

The token is not stored in the source code or GitHub repository.

Example:

```toml
HF_TOKEN = "your_token_here"
```

Never commit a real API token to GitHub.

---

## 📁 Project Structure

```text
GenAI-Student-Career-Assistant/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/thakursejal/GenAI-Student-Career-Assistant.git
```

### 2. Open the project

```bash
cd GenAI-Student-Career-Assistant
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Hugging Face token

Create Streamlit secrets:

```toml
HF_TOKEN = "your_hugging_face_token"
```

### 5. Run the application

```bash
streamlit run app.py
```

---

## 🎓 Modules Integrated

### Module 1
**Generative AI Foundations**

### Module 2
**Prompt Engineering & AI Productivity**

### Module 3
**LLM APIs & Application Development**

### Module 4
**RAG, Embeddings & Vector Databases**

### Module 5
**AI Agents, Tools & Automation**

### Module 6
**GenAI Capstone Project**

---

## 📊 Capstone Requirements Demonstrated

| Requirement | Implementation |
|---|---|
| Generative AI Application | Student & Career Assistant |
| LLM API | Hugging Face Inference API |
| Prompt Engineering | Structured System Prompt |
| RAG | Document Retrieval Pipeline |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| Document Processing | PyPDF |
| AI Agent | Tool Selection & Execution |
| Tools | Calculator & Task Manager |
| Multi-step Workflow | Agent-based execution |
| Web Application | Streamlit |
| Live Deployment | Streamlit Community Cloud |

---

## 🎯 Learning Outcomes

Through this project, I demonstrated practical understanding of:

- Generative AI application development
- LLM API integration
- Prompt engineering
- Embeddings and semantic retrieval
- Retrieval-Augmented Generation
- Vector databases
- Document question answering
- Function and tool calling
- AI agent workflows
- Multi-step task execution
- Streamlit application development
- Secure API key management
- Cloud deployment

---

## 👩‍💻 Author

**Thakur Sejal**

B.Tech — Artificial Intelligence & Machine Learning

**Codomax Digital Solutions Internship**

---

## 🔗 Project Links

🌐 Live Application:
https://genai-student-career-assistant.streamlit.app/

💻 GitHub Repository:
https://github.com/thakursejal/GenAI-Student-Career-Assistant

---

## ⭐ Project Summary

The GenAI Student & Career Assistant demonstrates how multiple Generative AI concepts can be combined into one practical application.

It integrates LLMs, Prompt Engineering, RAG, Embeddings, ChromaDB, AI Agents, Tool Calling, Document Processing, and Streamlit to create an interactive AI assistant for learning and career-related tasks.
