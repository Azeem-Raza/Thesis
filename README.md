# Mobile Retail Customer Support AI

An AI-powered customer support agent for a mobile retail store using LangChain/LangGraph, Groq API, and Streamlit.

## Features

- **Product Availability Checking:** Accurately retrieves and provides information about mobile phones in inventory
- **Order Status Tracking:** Checks order status by order number and provides tracking information
- **Smart Contextual Responses:** Uses AI to generate natural, helpful responses
- **Dark-Mode UI:** Clean, modern dark-themed interface
- **No If-Else Logic:** Fully AI-driven decision making through LangGraph workflows

## Project Structure

- `agent.py`: Backend implementation using LangChain and LangGraph
- `app.py`: Streamlit frontend with dark theme UI
- `data.py`: Product and order inventory data
- `.env`: Environment variables for API keys
- `requirements.txt`: Project dependencies

## Setup Instructions

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/mobile-retail-support-ai.git
   cd mobile-retail-support-ai
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Get a Groq API key from [Groq Console](https://console.groq.com/)

5. Create a `.env` file with your API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

6. Run the application:
   ```
   streamlit run app.py
   ```

## How It Works

The customer support AI uses a LangGraph-based workflow:

1. The agent analyzes user queries to determine intent (product or order query)
2. For product queries, it extracts product names and checks inventory
3. For order queries, it extracts order numbers and retrieves status
4. The agent generates natural responses based on the available data
5. All decisions are made by the AI model - no hardcoded decision logic

## Sample Queries

- "Do you have the iPhone 15 Pro in stock?"
- "What's the price of the Samsung Galaxy S24 Ultra?"
- "Tell me about the Google Pixel 8 Pro features"
- "What's the status of my order ORD10001?"
- "When will my order ORD10003 arrive?"

## Technologies Used

- **LangChain & LangGraph**: For building the agent workflow
- **Groq API**: Fast, efficient LLM API using Llama 3 70B
- **Streamlit**: For creating the web interface
- **Python**: Core programming language

## License

MIT

## Contributing

Contributions, issues, and feature requests are welcome! 