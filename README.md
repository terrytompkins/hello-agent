# Hello Agent - AI Agent Demonstrations

A collection of AI agent examples demonstrating different levels of complexity, from basic API integration to sophisticated file system analysis with AI-powered question answering.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## 🤖 Agent Components

### 1. Hello Agent (`hello_agent.py`) - Basic Agent Demo

A minimal "hello world" agent that demonstrates the fundamental agent pattern:
- **Input** → **API Call** → **Process** → **Output**

**Features:**
- Fetches weather data from OpenWeatherMap API
- Processes and formats JSON responses
- Interactive command-line interface
- Error handling and user-friendly output

**Usage:**
```bash
python hello_agent.py
```

**Example Output:**
```
🤖 Hello Agent - Minimal AI Agent Demo
==================================================

📍 Querying weather for: London
🤖 Hello Agent is fetching weather data for: London
🌍 Weather in London, GB:
🌡️  Temperature: 15.2°C
☁️  Conditions: Partly cloudy
💧 Humidity: 65%
```

**Perfect for:** Introducing the concept of agents in presentations and demonstrations.

---

### 2. File System Agent (`file_agent.py`) - Advanced Analysis Agent

A sophisticated agent that analyzes file systems and answers questions using AI:
- Scans directory hierarchies
- Collects file metadata (types, sizes, structure)
- Uses OpenAI GPT to answer natural language questions
- Supports complex calculations and analysis

**Features:**
- Comprehensive file system scanning
- AI-powered question answering
- Support for mathematical calculations
- Detailed file type and size analysis
- Largest file identification

**Usage:**
```bash
# Basic usage
python file_agent.py /path/to/folder "What is the total size of all files?"

# With verbose output
python file_agent.py /path/to/folder "How many Python files are there?" --verbose

# Using environment variable for API key
export OPENAI_API_KEY="your-key"
python file_agent.py /path/to/folder "What's the average file size?"
```

**Example Questions:**
- "What is the total size of all files?"
- "How many Python files are there?"
- "What's the average file size?"
- "Show me the largest 5 files"
- "What file types are most common?"

**Example Output:**
```
Scanning directory: /path/to/folder
Question: What is the total size of all files?
Answer: Result: 2.5 MB (2,621,440 bytes)
```

---

### 3. Streamlit Web Interface (`streamlit_app.py`) - Web-Based Agent

A modern web interface for the File System Agent:
- Beautiful, interactive web UI
- Real-time file system analysis
- Chat-like interface for questions
- Visual file system statistics

**Features:**
- Drag-and-drop folder selection
- Real-time scanning progress
- Interactive question-answering
- File system visualization
- Responsive design

**Usage:**
```bash
streamlit run streamlit_app.py
```

**Access:** Open your browser to `http://localhost:8501`

---

## 📋 Requirements

- Python 3.7+
- OpenAI API key (for file_agent.py and streamlit_app.py)
- Internet connection (for API calls)

**Dependencies:**
- `openai>=1.0.0` - OpenAI API client
- `streamlit>=1.28.0` - Web interface framework
- `requests>=2.25.0` - HTTP requests for hello_agent.py
- `pathlib` - File system operations

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd hello-agent
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API key:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## 🎯 Use Cases

### For Presentations & Demos
1. Start with `hello_agent.py` to introduce basic agent concepts
2. Progress to `file_agent.py` to show AI-powered analysis
3. Demonstrate `streamlit_app.py` for modern web interfaces

### For Learning
- **Beginner**: Study `hello_agent.py` for basic API integration patterns
- **Intermediate**: Explore `file_agent.py` for AI integration and complex data processing
- **Advanced**: Examine the Streamlit app for modern web development patterns

### For Development
- Use as templates for building custom agents
- Reference patterns for API integration, error handling, and user interfaces
- Study the progression from simple to complex agent architectures

## 🛠️ Customization

### Adding New APIs to Hello Agent
Modify `hello_agent.py` to use different APIs:
- Replace the weather API with any REST API
- Update the `process_weather_data()` method for your data format
- Customize the output formatting

### Extending File System Agent
Enhance `file_agent.py` with:
- Additional file metadata collection
- Custom analysis functions
- Integration with other AI models
- Export capabilities (CSV, JSON, etc.)

### Customizing Streamlit Interface
Modify `streamlit_app.py` to:
- Add new visualization components
- Implement user authentication
- Add file upload capabilities
- Customize the UI theme

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For questions or issues, please open an issue on the repository.
