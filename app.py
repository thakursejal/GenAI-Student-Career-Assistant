# ============================================================
# 🤖 GenAI Student & Career Assistant
# Codomax Digital Solutions Internship - Module 6
# ============================================================

import json
import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from huggingface_hub import InferenceClient

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="GenAI Student & Career Assistant",
    page_icon="🤖",
    layout="wide"
)

# ============================================================
# HUGGING FACE CONFIGURATION
# ============================================================

HF_TOKEN = st.secrets["HF_TOKEN"]

MODEL = "openai/gpt-oss-120b:fastest"

client = InferenceClient(
    api_key=HF_TOKEN
)
# ============================================================
# RAG COMPONENTS
# ============================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

chroma_client = chromadb.Client()

pdf_collection = chroma_client.get_or_create_collection(
    name="uploaded_documents"
)

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ============================================================
# KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_BASE = [
    {
        "topic": "study",
        "text": """
        Effective study planning starts by identifying learning goals,
        breaking large subjects into smaller topics, and creating a
        realistic study schedule. Active recall, spaced repetition,
        practice questions, and regular revision can improve learning.
        """
    },
    {
        "topic": "career",
        "text": """
        Building an AI and machine learning career requires strong
        programming fundamentals, knowledge of mathematics and machine
        learning concepts, practical project experience, and a portfolio.
        GitHub projects, internships, technical practice, and continuous
        learning can help demonstrate practical skills.
        """
    },
    {
        "topic": "coding",
        "text": """
        Good programming practice involves understanding the problem,
        designing an algorithm, writing readable code, testing the solution,
        handling errors, and improving the solution when necessary.
        Python is widely used in artificial intelligence and machine learning.
        """
    },
    {
        "topic": "rag",
        "text": """
        Retrieval-Augmented Generation, or RAG, combines information
        retrieval with a large language model. Relevant information is
        retrieved from a knowledge source and provided as context to the
        language model before generating an answer.
        """
    },
    {
        "topic": "genai",
        "text": """
        Generative AI systems use machine learning models to generate
        content such as text, code, images, or other outputs. Large
        language models can understand and generate natural language
        based on patterns learned during training.
        """
    }
]
# ============================================================
# 📄 PDF DOCUMENT PROCESSING
# ============================================================

def extract_pdf_text(uploaded_file):
    """Extract text from an uploaded PDF."""

    reader = PdfReader(uploaded_file)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def chunk_text(text, chunk_size=800):
    """Split document text into manageable chunks."""

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def process_pdf(uploaded_file):
    """Extract, chunk, embed and store a PDF."""

    text = extract_pdf_text(uploaded_file)

    if not text.strip():
        return 0

    chunks = chunk_text(text)

    # Create embeddings
    embeddings = embedding_model.encode(
        chunks
    ).tolist()

    # Create unique IDs for this document
    document_name = uploaded_file.name

    ids = [
        f"{document_name}_{i}"
        for i in range(len(chunks))
    ]

    # Store in ChromaDB
    pdf_collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return len(chunks)


def search_pdf_knowledge(query, top_k=3):
    """Retrieve relevant information from uploaded PDFs."""

    if pdf_collection.count() == 0:
        return ""

    query_embedding = embedding_model.encode(
        [query]
    ).tolist()[0]

    results = pdf_collection.query(
        query_embeddings=[query_embedding],
        n_results=min(
            top_k,
            pdf_collection.count()
        )
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    if not documents:
        return ""

    return "\n\n".join(documents)

# ============================================================
# 🔍 COMBINED KNOWLEDGE SEARCH
# ============================================================

def search_knowledge(query):
    """
    Search both the built-in knowledge base
    and uploaded PDF documents.
    """

    # --------------------------------------------
    # Search built-in knowledge
    # --------------------------------------------

    query_words = set(
        query.lower().split()
    )

    scored_documents = []

    for item in KNOWLEDGE_BASE:

        text_words = set(
            item["text"].lower().split()
        )

        score = len(
            query_words.intersection(text_words)
        )

        scored_documents.append(
            (
                score,
                item["topic"],
                item["text"]
            )
        )

    scored_documents.sort(
        key=lambda x: x[0],
        reverse=True
    )

    built_in_results = [
        item
        for item in scored_documents[:2]
        if item[0] > 0
    ]

    built_in_context = "\n\n".join(
        f"[{topic.upper()}]\n{text.strip()}"
        for _, topic, text in built_in_results
    )

    # --------------------------------------------
    # Search uploaded PDF documents
    # --------------------------------------------

    pdf_context = search_pdf_knowledge(
        query,
        top_k=3
    )

    # --------------------------------------------
    # Combine results
    # --------------------------------------------

    contexts = []

    if built_in_context:
        contexts.append(
            "BUILT-IN KNOWLEDGE:\n"
            + built_in_context
        )

    if pdf_context:
        contexts.append(
            "UPLOADED DOCUMENT CONTEXT:\n"
            + pdf_context
        )

    if not contexts:
        return (
            "No relevant information was found "
            "in the available knowledge sources."
        )

    return "\n\n".join(contexts)


# ============================================================
# 🧮 CALCULATOR TOOL
# ============================================================

def calculator(expression):

    try:

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return f"Calculation result: {result}"

    except Exception:

        return "Unable to calculate the expression."


# ============================================================
# 📝 TASK MANAGEMENT TOOLS
# ============================================================

def add_task(task):

    st.session_state.tasks.append(task)

    return f"Task added successfully: {task}"


def list_tasks():

    if not st.session_state.tasks:
        return "No tasks found."

    result = "Current tasks:\n"

    for i, task in enumerate(
        st.session_state.tasks,
        start=1
    ):

        result += f"{i}. {task}\n"

    return result


def remove_task(task_number):

    try:

        task_number = int(task_number)

        if 1 <= task_number <= len(
            st.session_state.tasks
        ):

            removed = st.session_state.tasks.pop(
                task_number - 1
            )

            return f"Task removed: {removed}"

        return "Invalid task number."

    except Exception:

        return "Invalid task number."


# ============================================================
# TOOL DEFINITIONS
# ============================================================

tools = [

    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression such as 125 * 32"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a task to the task list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "Task to add"
                    }
                },
                "required": ["task"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all current tasks.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "remove_task",
            "description": "Remove a task by task number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_number": {
                        "type": "integer",
                        "description": "Task number"
                    }
                },
                "required": ["task_number"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search the internal knowledge base for study, career, coding, RAG and GenAI information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Question or topic to search"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool(tool_name, arguments):

    if tool_name == "calculator":

        return calculator(
            arguments.get("expression", "")
        )

    elif tool_name == "add_task":

        return add_task(
            arguments.get("task", "")
        )

    elif tool_name == "list_tasks":

        return list_tasks()

    elif tool_name == "remove_task":

        return remove_task(
            arguments.get("task_number")
        )

    elif tool_name == "search_knowledge":

        return search_knowledge(
            arguments.get("query", "")
        )

    return "Unknown tool."


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a professional GenAI Student & Career Assistant.

You help users with:

1. Study and learning
2. Career development
3. Programming and coding
4. Generative AI
5. RAG concepts
6. Task management
7. Mathematical calculations
8. Questions about uploaded documents

You are also an AI agent with access to tools.

IMPORTANT RULES:

- Understand the user's intent before answering.
- Use tools whenever the request requires an action.
- Use search_knowledge for study, career, coding, RAG,
  GenAI, or uploaded-document questions when relevant.
- Use calculator for mathematical calculations.
- Use task tools when the user asks to add, list, or remove tasks.
- Never claim an action was completed unless the tool executed successfully.
- If multiple actions are requested, complete all required actions.
- When search_knowledge returns information from an uploaded document,
  use that retrieved context to answer the user's question.
- Treat retrieved document context as the primary source for
  document-specific questions.
- Do not invent information that is not supported by the retrieved context.
- If the retrieved context does not contain enough information,
  clearly tell the user that the information was not found.
- Give clear, practical, and structured answers.
"""


# ============================================================
# AI AGENT
# ============================================================

def run_agent(user_request, max_steps=5):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_request
        }
    ]

    activity = []

    for step in range(max_steps):

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=tools,

            tool_choice="auto",

            max_tokens=500
        )

        assistant_message = response.choices[0].message

        # ----------------------------------------------------
        # No more tools required
        # ----------------------------------------------------

        if not getattr(
            assistant_message,
            "tool_calls",
            None
        ):

            return (
                assistant_message.content,
                activity
            )

        messages.append(
            assistant_message
        )

        # ----------------------------------------------------
        # Execute requested tools
        # ----------------------------------------------------

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

            except Exception:

                arguments = {}

            activity.append(
                f"🛠️ Tool selected: {tool_name}"
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            activity.append(
                f"📤 Result: {result}"
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

    return (
        "The agent reached the maximum number of steps.",
        activity
    )


# ============================================================
# USER INTERFACE
# ============================================================

st.title("🤖 GenAI Student & Career Assistant")

st.markdown(
    """
### Your AI-powered learning and career companion

This application combines:

**🧠 LLM + ✨ Prompt Engineering + 📚 RAG + 🛠️ Tools + 🤖 AI Agents**
"""
)
# ============================================================
# 📄 PDF UPLOAD & DOCUMENT RAG
# ============================================================

st.subheader("📄 Chat With Your Documents")

st.write(
    "Upload a PDF and the AI Agent will extract, process, "
    "and retrieve relevant information from it."
)

uploaded_pdf = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    help="Upload a PDF to add its content to the RAG knowledge base."
)

if uploaded_pdf is not None:

    if st.button("📚 Process PDF"):

        with st.spinner(
            "📄 Processing your document..."
        ):

            try:

                chunk_count = process_pdf(
                    uploaded_pdf
                )

                if chunk_count > 0:

                    st.success(
                        f"✅ PDF processed successfully! "
                        f"{chunk_count} text chunks added to the knowledge base."
                    )

                    st.session_state.pdf_processed = True

                else:

                    st.warning(
                        "⚠️ No readable text was found in the PDF."
                    )

            except Exception as e:

                st.error(
                    f"❌ Unable to process the PDF: {e}"
                )

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🧰 Agent Tools")

    st.write("📚 Knowledge Search")
    st.write("🧮 Calculator")
    st.write("📝 Task Manager")
    st.write("🤖 AI Agent")

    st.divider()

    st.subheader("📋 Current Tasks")

    if st.session_state.tasks:

        for i, task in enumerate(
            st.session_state.tasks,
            start=1
        ):

            st.write(
                f"{i}. {task}"
            )

    else:

        st.write("No tasks yet.")

    st.divider()

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask about study, career, coding, AI, RAG or tasks..."
)


if user_input:

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)

    # --------------------------------------------------------
    # Run agent
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Agent is thinking..."
        ):

            try:

                answer, activity = run_agent(
                    user_input
                )

                st.markdown(answer)

                if activity:

                    with st.expander(
                        "🔎 View Agent Activity"
                    ):

                        for item in activity:

                            st.write(item)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                error_message = (
                    "⚠️ Something went wrong while "
                    "processing your request."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Built by Thakur Sejal | Codomax Digital Solutions Internship | Module 6"
)
