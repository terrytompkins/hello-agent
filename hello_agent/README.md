# Hello Agent - Basic Agent Demo

A minimal "hello world" agent that demonstrates the fundamental agent pattern: **Input → API Call → Process → Output**.

## 🎯 Purpose

This agent serves as a simple introduction to AI agents, showing the basic pattern without complexity. Perfect for presentations and learning the fundamentals of agent architecture.

## 🏗️ Architecture

```
User Input → Hello Agent → Weather API → Process Data → Formatted Output
```

### **Simple Agent Pattern**
1. **Input**: User provides city name
2. **API Call**: HTTP request to OpenWeatherMap API
3. **Processing**: Parse JSON response and format data
4. **Output**: Display formatted weather information

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the agent:**
   ```bash
   python hello_agent.py
   ```

## 📋 Features

- **Weather API Integration**: Fetches real-time weather data
- **Error Handling**: Graceful degradation with user-friendly messages
- **Interactive CLI**: Command-line interface with demo and interactive modes
- **JSON Processing**: Parses and formats API responses
- **User-Friendly Output**: Emoji-enhanced weather display

## 💻 Usage

### Demo Mode
The agent automatically runs demo queries for London, New York, and Tokyo.

### Interactive Mode
Enter any city name to get current weather information.

### Example Output
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

## 🔧 Technology Stack

- **Python**: Core programming language
- **Requests**: HTTP client for API calls
- **JSON**: Data format for API responses
- **OpenWeatherMap API**: Free weather data service

## 🎓 Learning Value

This agent demonstrates:
- Basic API integration patterns
- Error handling best practices
- Simple data processing workflows
- User interface design principles
- Agent architecture fundamentals

## 📁 File Structure

```
hello_agent/
├── hello_agent.py      # Main agent implementation
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── flowchart.md       # System architecture diagram
└── interactive-flowchart.html  # Interactive visualization
```

## 🔗 Related Projects

- **File System Agent**: Advanced AI-powered file analysis
- **Streamlit Interface**: Web-based UI for file system agent

---

*This agent is part of a larger demonstration of AI agent evolution, from simple API integration to sophisticated AI-powered analysis.* 