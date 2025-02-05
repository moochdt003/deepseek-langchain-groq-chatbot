from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.callbacks.manager import get_openai_callback
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper
import os
import json
from datetime import datetime
import argparse
import logging
from typing import Optional

class ChatBot:
    def __init__(self, model_name: str = "deepseek-r1-distill-llama-70b", temperature: float = 0.6):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='chatbot.log'
        )
        self.logger = logging.getLogger(__name__)

        # Load environment variables
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        # Initialize the chat model
        try:
            self.chat = ChatGroq(
                api_key=api_key,
                model_name=model_name,
                temperature=temperature,
                max_tokens=4096
            )
            
            # Initialize tools
            search = DuckDuckGoSearchRun()
            wikipedia = WikipediaAPIWrapper()

            self.tools = [
                Tool(
                    name="Search",
                    func=search.run,
                    description="Useful for searching the internet for current information and news."
                ),
                Tool(
                    name="Wikipedia",
                    func=wikipedia.run,
                    description="Useful for getting detailed information from Wikipedia."
                )
            ]

            # Initialize agent with tools
            self.agent = initialize_agent(
                tools=self.tools,
                llm=self.chat,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                handle_parsing_errors=True
            )

            # Initialize conversation with memory
            self.conversation = ConversationChain(
                llm=self.chat,
                memory=ConversationBufferMemory(),
                verbose=True
            )
        except Exception as e:
            self.logger.error(f"Error initializing chat model: {str(e)}")
            raise

    def save_conversation(self, filename: Optional[str] = None) -> None:
        """Save the conversation history to a JSON file"""
        if filename is None:
            filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            history = self.conversation.memory.chat_memory.messages
            conversation_data = {
                "timestamp": datetime.now().isoformat(),
                "messages": [
                    {
                        "role": "system" if isinstance(msg, SystemMessage) else "human" if isinstance(msg, HumanMessage) else "ai",
                        "content": msg.content
                    }
                    for msg in history
                ]
            }
            
            with open(filename, 'w') as f:
                json.dump(conversation_data, f, indent=2)
            print(f"\nConversation saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving conversation: {str(e)}")
            print(f"\nError saving conversation: {str(e)}")

    def process_input(self, user_input: str) -> str:
        """Process user input and determine whether to use agent or regular conversation"""
        # Keywords that suggest the need for current information
        search_keywords = ['search', 'find', 'look up', 'what is', 'who is', 'current', 
                         'latest', 'news', 'how to', 'weather', 'price', 'when']
        
        # Check if input suggests the need for search
        needs_search = any(keyword in user_input.lower() for keyword in search_keywords)
        
        try:
            if needs_search:
                # Use agent with tools for searches
                response = self.agent.run(user_input)
            else:
                # Use regular conversation for chat
                response = self.conversation.predict(input=user_input)
            return response
        except Exception as e:
            self.logger.error(f"Error processing input: {str(e)}")
            return f"I encountered an error: {str(e)}"

    def run(self):
        """Run the chat loop"""
        print("\nWelcome to the Enhanced LangChain-Groq Chatbot!")
        print("This bot can search the internet and access Wikipedia!")
        print("Type 'exit' to end the conversation")
        print("Type 'save' to save the conversation")
        print("Type 'clear' to clear the conversation history")
        print("-" * 50)

        try:
            while True:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() == 'exit':
                    self.save_conversation()
                    break
                elif user_input.lower() == 'save':
                    self.save_conversation()
                    continue
                elif user_input.lower() == 'clear':
                    self.conversation.memory.clear()
                    print("\nConversation history cleared!")
                    continue
                elif not user_input:
                    continue

                try:
                    with get_openai_callback() as cb:
                        response = self.process_input(user_input)
                        print(f"\nBot: {response}")
                        print(f"\nTokens used: {cb.total_tokens}")
                except Exception as e:
                    self.logger.error(f"Error getting response: {str(e)}")
                    print(f"\nError getting response: {str(e)}")

        except KeyboardInterrupt:
            print("\nExiting gracefully...")
            self.save_conversation()

def main():
    parser = argparse.ArgumentParser(description='Enhanced LangChain-Groq Chatbot')
    parser.add_argument('--model', type=str, default="deepseek-r1-distill-llama-70b",
                      help='Model name to use')
    parser.add_argument('--temperature', type=float, default=0.6,
                      help='Temperature for response generation')
    
    args = parser.parse_args()
    
    try:
        chatbot = ChatBot(model_name=args.model, temperature=args.temperature)
        chatbot.run()
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()