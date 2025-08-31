import streamlit as st
import os
import tempfile
import gc
import base64
import time

from crewai import Agent, Crew, Process, Task, LLM
from src.agentic_rag.tools.custom_tool import DocumentSearchTool
from crewai_tools import FirecrawlSearchTool
from crewai_tools import SerperDevTool 
from dotenv import load_dotenv


try: 
    from firecrawl import FirecrawlApp
    FIRECRAWL_AVAILABLE = True
except ImportError:
    FIRECRAWL_AVAILABLE = False


@st.cache_resource
def load_llm():
    llm = LLM(
        model="ollama/llama3.2",
        base_url="http://localhost:11434"
    )
    return llm

def load_config(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

agents_config = load_config("src/agentic_rag/config/agents.yaml")
tasks_config = load_config("src/agentic_rag/config/tasks.yaml")


# ===========================
#   Define Agents & Tasks
# ===========================
def create_agents_and_tasks(pdf_tool):
    """Creates a Crew with the given PDF tool (if any) and a web search tool."""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
    
    # Check if Firecrawl is available before creating the tool
    if not FIRECRAWL_AVAILABLE:
        import subprocess
        try:
            subprocess.run(["pip", "install", "firecrawl-py"], check=True)
            from firecrawl import FirecrawlApp
        except subprocess.CalledProcessError:
            print("Firecrawl installation failed.")
            raise ImportError("Failed to install firecrawl-py package. Please install it manually using 'pip install firecrawl-py'")
        finally:
            print(f"FIRECRAWL_AVAILABLE after install attempt: {FIRECRAWL_AVAILABLE}")

    web_search_tool = None  # Define it outside the try block
    try:
        from firecrawl import FirecrawlApp
        print(f"FirecrawlApp after install attempt: {FirecrawlApp}")
        web_search_tool = FirecrawlSearchTool(
            api_key=api_key,
            params={
                "num_results": 5,  # Optional: number of results to return
                "include_domains": [],  # Optional: specific domains to search
                "exclude_domains": []  # Optional: domains to exclude
            }
        )
    except (NameError, ImportError) as e:
        print(f"FirecrawlApp is not defined or Firecrawl installation failed: {e}")
        web_search_tool = None  # Or some other fallback


    retriever_agent = Agent(
    config=agents_config["retriever_agent"],
    tools=[t for t in [pdf_tool, web_search_tool] if t],
    llm=load_llm(),
    verbose=True
    )

    response_synthesizer_agent = Agent(
    config=agents_config["response_synthesizer_agent"],
    llm=load_llm(),
    verbose=True
    )

    
    
    retrieval_task = Task(
    config=tasks_config["retrieval_task"],
    agent=retriever_agent
    )

    response_task = Task(
    config=tasks_config["response_task"],
    agent=response_synthesizer_agent
    )

    crew = Crew(
        agents=[retriever_agent, response_synthesizer_agent],
        tasks=[retrieval_task, response_task],
        process=Process.sequential,  # or Process.hierarchical
        verbose=True
    )
    return crew


# ===========================
#   Sidebar
# ===========================
with st.sidebar:
    st.header("Add Your PDF Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # If there's a new file and we haven't set pdf_tool yet...
        if st.session_state.pdf_tool is None:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                with st.spinner("Indexing PDF... Please wait..."):
                    st.session_state.pdf_tool = DocumentSearchTool(file_path=temp_file_path)
            
            st.success("PDF indexed! Ready to chat.")

        # Optionally display the PDF in the sidebar
        display_pdf(uploaded_file.getvalue(), uploaded_file.name)

    st.button("Clear Chat", on_click=reset_chat)

# ===========================
#   Main Chat Interface
# ===========================
st.markdown("""
    # Agentic RAG powered by <img src="data:image/png;base64,{}" width="120" style="vertical-align: -3px;">
""".format(base64.b64encode(open("assets/deep-seek.png", "rb").read()).decode()), unsafe_allow_html=True)

# Render existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask a question about your PDF...")

if prompt:
    # 1. Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Build or reuse the Crew (only once after PDF is loaded)
    if st.session_state.crew is None:
        st.session_state.crew = create_agents_and_tasks(st.session_state.pdf_tool)

    # 3. Get the response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get the complete response first
        with st.spinner("Thinking..."):
            inputs = {"query": prompt}
            result = st.session_state.crew.kickoff(inputs=inputs).raw
        
        # Split by lines first to preserve code blocks and other markdown
        lines = result.split('\n')
        for i, line in enumerate(lines):
            full_response += line
            if i < len(lines) - 1:  # Don't add newline to the last line
                full_response += '\n'
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.15)  # Adjust the speed as needed
        
        # Show the final response without the cursor
        message_placeholder.markdown(full_response)

    # 4. Save assistant's message to session
    st.session_state.messages.append({"role": "assistant", "content": result})