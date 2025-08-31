# CrewAI Agentic RAG System

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.108.0-orange.svg)](https://www.crewai.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.44.0-red.svg)](https://streamlit.io/)

An intelligent Retrieval-Augmented Generation (RAG) system built with CrewAI, featuring custom PDF document search, web search integration, and multiple user interfaces. This project demonstrates advanced agent orchestration for information retrieval and synthesis.

## 🌟 Features

### Core Functionality
- **Multi-Source Information Retrieval**: Combines PDF document search with web search capabilities
- **Agent-Based Architecture**: Uses specialized agents for retrieval and response synthesis
- **Vector Database Integration**: Employs Qdrant for efficient document chunk storage and similarity search
- **Flexible Search Strategy**: Prioritizes PDF content, falls back to web search when needed
- **Sequential Processing**: Ensures coherent information flow between agents

### User Interfaces
- **Command-Line Interface**: Simple CLI for quick queries (`main.py`)
- **Web Interface**: Interactive Streamlit app with PDF upload and chat functionality (`app_llama.py`)
- **Real-time Streaming**: Progressive response display in web interface

### Technical Features
- **Custom PDF Processing**: Uses MarkItDown for robust PDF text extraction
- **Intelligent Chunking**: Recursive text splitting with overlap for optimal retrieval
- **Multiple LLM Support**: Configurable language models (Ollama, OpenAI, etc.)
- **Tool Integration**: SerperDev and Firecrawl for web search
- **Environment Configuration**: Secure API key management with dotenv

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  Retriever Agent │───▶│ Response Synth  │
│                 │    │                  │    │   Agent         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │                           │
                              ▼                           ▼
                       ┌─────────────┐            ┌─────────────┐
                       │ PDF Search  │            │   Synthesis │
                       │   Tool      │            │             │
                       └─────────────┘            └─────────────┘
                              │
                              ▼
                       ┌─────────────┐
                       │ Web Search  │
                       │   Tool      │
                       └─────────────┘
```

### Components

#### Agents
- **Retriever Agent**: Handles information gathering from PDF and web sources
- **Response Synthesizer Agent**: Processes retrieved information into coherent responses

#### Tools
- **DocumentSearchTool**: Custom tool for PDF content search using Qdrant
- **SerperDevTool**: Web search integration
- **FirecrawlSearchTool**: Advanced web scraping and search

#### Configuration
- **agents.yaml**: Agent role definitions and backstories
- **tasks.yaml**: Task descriptions and expected outputs

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Ollama (for local LLM support)
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Monish-Nallagondalla/crewai_agentic_rag.git
   cd crewai_agentic_rag
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env  # Create if not exists
   ```

   Edit `.env` with your API keys:
   ```env
   SERPER_API_KEY=your_serper_api_key
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   ```

5. **Start Ollama (for local LLM)**
   ```bash
   ollama serve
   ollama pull llama3.2  # Pull the required model
   ```

## 📖 Usage

### Command-Line Interface

Run a simple query:
```bash
python src/agentic_rag/main.py
```

The default query is: "Who is Elon Musk and what is his net worth?"

### Web Interface

1. **Start the Streamlit app**
   ```bash
   streamlit run app_llama.py
   ```

2. **Access the interface**
   - Open http://localhost:8501 in your browser
   - Upload a PDF document in the sidebar
   - Wait for indexing to complete
   - Start chatting with your document

### Features in Web Interface
- **PDF Upload**: Drag and drop PDF files for indexing
- **Real-time Chat**: Interactive conversation with the RAG system
- **Progress Indicators**: Visual feedback during processing
- **Chat History**: Persistent conversation history

## ⚙️ Configuration

### Agent Configuration (`src/agentic_rag/config/agents.yaml`)

```yaml
retriever_agent:
  role: "Retrieve relevant information..."
  goal: "Retrieve the most relevant information..."
  backstory: "You're a meticulous analyst..."

response_synthesizer_agent:
  role: "Response synthesizer agent..."
  goal: "Synthesize the retrieved information..."
  backstory: "You're a skilled communicator..."
```

### Task Configuration (`src/agentic_rag/config/tasks.yaml`)

```yaml
retrieval_task:
  description: "Retrieve the most relevant information..."
  expected_output: "The most relevant information in form of text..."
  agent: retriever_agent

response_task:
  description: "Synthesize the final response..."
  expected_output: "A concise and coherent response..."
  agent: response_synthesizer_agent
```

### Customizing the PDF Search Tool

Modify chunk size and overlap in `src/agentic_rag/tools/custom_tool.py`:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,      # Adjust chunk size
    chunk_overlap=50,    # Adjust overlap
    # ... other parameters
)
```

## 🔧 Development

### Project Structure
```
crewai_agentic_rag/
├── src/
│   └── agentic_rag/
│       ├── __init__.py
│       ├── crew.py              # Main CrewAI setup
│       ├── main.py              # CLI entry point
│       ├── config/
│       │   ├── agents.yaml      # Agent configurations
│       │   └── tasks.yaml       # Task configurations
│       └── tools/
│           ├── __init__.py
│           └── custom_tool.py   # Custom PDF search tool
├── app_llama.py                 # Streamlit web interface
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
├── README.md                    # This file
├── assets/                      # Static assets
│   └── deep-seek.png
├── knowledge/                   # Knowledge base documents
│   └── dspy.pdf
└── flow_diagram.svg             # Architecture diagram
```

### Adding New Tools

1. Create a new tool class in `src/agentic_rag/tools/`
2. Inherit from `BaseTool` and implement the required methods
3. Add the tool to the agent's tool list in `crew.py`

### Extending Agents

1. Add new agent configuration in `agents.yaml`
2. Create the agent method in `crew.py` with `@agent` decorator
3. Define corresponding tasks in `tasks.yaml`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add type hints for new functions
- Write comprehensive docstrings
- Add unit tests for new features
- Update documentation for API changes

## 📊 Performance & Metrics

### Current Capabilities
- **PDF Processing**: Handles various PDF formats using MarkItDown
- **Chunking Strategy**: 512-character chunks with 50-character overlap
- **Vector Storage**: In-memory Qdrant for fast retrieval
- **Search Accuracy**: Semantic similarity-based retrieval
- **Response Quality**: Agent-based synthesis for coherent answers

### Known Limitations
- In-memory vector storage (suitable for small documents)
- Single PDF support per session (web interface)
- Sequential processing (no parallel retrieval)

## 🔒 Security

- API keys stored securely in environment variables
- No sensitive data logged in application output
- Input validation for file uploads
- Secure temporary file handling

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://www.crewai.com/) - Multi-agent framework
- [Qdrant](https://qdrant.tech/) - Vector database
- [Streamlit](https://streamlit.io/) - Web app framework
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [MarkItDown](https://github.com/microsoft/markitdown) - PDF processing

## 📞 Support

For questions, issues, or contributions:
- Open an issue on GitHub
- Check the documentation in this README
- Review the code comments for implementation details


---

**Made with ❤️ using CrewAI and modern AI tools**
