# Enhanced LangChain-Groq Chatbot

An advanced AI chatbot implementation that combines the power of Groq's LLM with LangChain's tools for internet access, web searching, and conversation memory. This chatbot can search the internet, access Wikipedia, and maintain conversation context while providing informative responses.

## Features

- 🌐 Internet search capabilities using DuckDuckGo
- 📚 Wikipedia integration for detailed information
- 💭 Conversation memory with history saving
- 🔍 Smart input processing to determine when to use search vs chat
- 📊 Token usage tracking
- 🛠️ Command-line configuration options
- 📝 Conversation history saving in JSON format
- 🔄 Clear conversation functionality
- 🚀 Auto-save on exit
- 📋 Detailed logging system

## Features in Detail

### Internet Search
The chatbot automatically detects when a query might benefit from current information and uses DuckDuckGo to search the internet.

### Wikipedia Integration
Access to Wikipedia articles for detailed information about various topics.

### Conversation Memory
The chatbot maintains context throughout the conversation and can save conversation history to JSON files.

### Smart Processing
Automatically determines whether to use internet search or regular conversation based on the query type.

## Logging

The application maintains detailed logs in `chatbot.log`, including:
- Initialization information
- Error messages
- API interactions
- User interactions

## Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com))

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/langchain-groq-chatbot.git
cd langchain-groq-chatbot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Groq API key:

```bash
GROQ_API_KEY=<your_groq_api_key>
```

## Usage

### Basic Usage

Run the chatbot with default settings:

```bash
python app.py
```


### Advanced Usage

Run with custom parameters:

```bash
python app.py --model <model_name> --temperature <temperature>
```


### Available Commands

While the chatbot is running:
- Type `exit` to end the conversation (auto-saves)
- Type `save` to save the current conversation
- Type `clear` to clear the conversation history
- Use natural language to interact with the bot

### Example Queries

- "Search for the latest news about AI"
- "What is the current weather in New York?"
- "Look up information about quantum computing"
- "Find recent developments in renewable energy"
- "Tell me about the history of the Internet"

## Project Structure

enhanced-langchain-groq-chatbot/
├── app.py # Main application file
├── requirements.txt # Project dependencies
├── .env # Environment variables (create this)
├── .gitignore # Git ignore file
├── README.md # This file
└── chatbot.log # Log file (created when running)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [LangChain](https://github.com/hwchase17/langchain) for the amazing tools and framework
- [Groq](https://groq.com/) for the powerful LLM API
- DuckDuckGo for search capabilities
- Wikipedia API for knowledge access

## Support

For support, please open an issue in the GitHub repository.

## Disclaimer

This project is not affiliated with Groq, LangChain, or DuckDuckGo. All trademarks are the property of their respective owners.

