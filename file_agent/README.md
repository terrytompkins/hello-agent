# File System Agent - AI-Powered Analysis

An advanced AI agent that analyzes file systems and answers natural language questions using OpenAI GPT. This agent demonstrates sophisticated AI integration with complex data processing capabilities.

## 🎯 Purpose

This agent showcases advanced AI agent patterns, combining file system analysis with natural language processing to provide intelligent insights about directory structures and file metadata.

## 🏗️ Architecture

```
User Input → File System Agent → Directory Scan → AI Analysis → Intelligent Response
```

### **AI Agent Pattern**
1. **Input**: User provides folder path and natural language question
2. **Data Collection**: Scan file system and collect comprehensive metadata
3. **AI Analysis**: Send question and data to OpenAI GPT for processing
4. **Processing**: Execute calculations or provide direct answers
5. **Output**: AI-generated response with insights and visualizations

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

3. **Run the command-line agent:**
   ```bash
   python file_agent.py /path/to/folder "What is the total size of all files?"
   ```

4. **Or launch the web interface:**
   ```bash
   streamlit run streamlit_app.py
   ```

## 📋 Features

### **File System Analysis**
- **Comprehensive Scanning**: Recursively analyzes entire directory structures
- **Metadata Collection**: Gathers file types, sizes, and directory information
- **Performance Optimization**: Efficient handling of large file systems
- **Error Handling**: Graceful handling of permission errors and inaccessible files

### **AI-Powered Question Answering**
- **Natural Language Processing**: Understands questions in plain English
- **Intelligent Responses**: Provides contextual answers based on file system data
- **Calculation Engine**: Executes complex mathematical operations
- **Direct Answers**: Gives immediate responses for simple queries

### **Web Interface**
- **Modern UI**: Beautiful Streamlit-based web interface
- **Real-time Processing**: Live progress indicators and status updates
- **Interactive Visualizations**: Charts, tables, and statistics
- **Configuration Management**: Secure API key handling

## 💻 Usage Examples

### **Command Line Interface**

```bash
# Basic usage
python file_agent.py /path/to/folder "What is the total size of all files?"

# With verbose output
python file_agent.py /path/to/folder "How many Python files are there?" --verbose

# Using environment variable for API key
export OPENAI_API_KEY="your-key"
python file_agent.py /path/to/folder "What's the average file size?"
```

### **Example Questions**
- "What is the total size of all files?"
- "How many Python files are there?"
- "What's the average file size?"
- "Show me the largest 5 files"
- "What file types are most common?"
- "How many image files are in the directory?"
- "What is the total size of all image files?"

### **Example Output**
```
Scanning directory: /path/to/folder
Question: What is the total size of all files?
Answer: Result: 2.5 MB (2,621,440 bytes)
```

### **Web Interface**
Access the Streamlit app at `http://localhost:8501` for an interactive experience with:
- Drag-and-drop folder selection
- Real-time analysis progress
- Interactive question-answering
- Visual file system statistics

## 🔧 Technology Stack

- **Python**: Core programming language
- **OpenAI GPT**: AI-powered question answering
- **Streamlit**: Modern web interface framework
- **Pathlib**: File system operations
- **Requests**: HTTP client for API calls

## 🎓 Learning Value

This agent demonstrates:
- Advanced AI integration patterns
- Complex data processing workflows
- Natural language processing
- Web application development
- File system analysis techniques
- Modern UI/UX design principles

## 📁 File Structure

```
file_agent/
├── file_agent.py       # Core AI agent implementation
├── streamlit_app.py    # Web interface
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── flowchart.md       # System architecture diagram
└── interactive-flowchart.html  # Interactive visualization
```

## 🔗 Related Projects

- **Hello Agent**: Basic API integration demonstration
- **Root Project**: Combined system overview

## 🔒 Security Considerations

- **API Key Management**: Secure handling of OpenAI credentials
- **File System Access**: Controlled directory scanning with user consent
- **Data Privacy**: Local processing without external data transmission
- **Input Validation**: Sanitization of user inputs and file paths

## 🛠️ Advanced Features

### **Calculation Engine**
The agent can execute complex calculations using Python expressions:
- File size aggregations
- Statistical analysis
- Custom filtering operations
- Mathematical computations

### **Error Handling**
- Graceful API failure handling
- Permission error management
- Network timeout handling
- User-friendly error messages

### **Performance Optimization**
- Efficient file system traversal
- Memory-conscious data structures
- Progress indicators for large directories
- Optimized data processing

---

*This agent represents the advanced tier of AI agent development, combining sophisticated data analysis with natural language processing capabilities.* 