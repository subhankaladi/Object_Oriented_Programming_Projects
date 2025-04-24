import os
import requests
from typing import Optional, Dict
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.tool import function_tool
import chainlit as cl

load_dotenv()

# 🎯 OOP Class for API Setup (Encapsulation)


class GeminiProvider:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/openai"

    def get_provider(self):
        return AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

# Instantiate GeminiProvider and create model
provider_instance = GeminiProvider()  # 🧱 Object
provider = provider_instance.get_provider()
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)



# (Abstraction + Static)

class SubhanDataFetcher:
    @staticmethod
    @function_tool("get_subhan_data")
    def get_subhan_data() -> str:
        try:
            response = requests.get("https://www.youtube.com/@subhankaladi")
            if response.status_code == 200:
                return  response.text
            else :
                return f"Error: {response.status_code}"
            
        except Exception as e:
            return f"Error: {str(e)}"
        
class SubhanAgentFactory:
    @staticmethod
    def create_agent():
        return Agent(
            name="Greeting Agent",
            instructions="""
                You are a Greeting Agent designed to provide friendly interactions and information about Subhan Kaladi.

                Your responsibilities:
                1. Greet users warmly when they say hello (respond with 'Salam from Subhan Kaladi')
                2. Say goodbye appropriately when users leave (respond with 'Allah Hafiz from Subhan Kaladi')
                3. When users request information about Subhan Kaladi, use the get_subhan_data tool to retrieve and share his profile information
                4. For any questions not related to greetings or Subhan Kaladi, politely explain: 'I'm only able to provide greetings and information about Subhan Kaladi. I can't answer other questions at this time.'

                Always maintain a friendly, professional tone and ensure responses are helpful within your defined scope.
            """,
            model=model,
            tools=[SubhanDataFetcher.get_subhan_data]
        )

# Create agent from factory
agent = SubhanAgentFactory.create_agent()


@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    return default_user



@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="Hello! How can I help you today?"
    ).send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    
    result = await cl.make_async(Runner.run_sync)(agent, input=history)
    response_text = result.final_output

    await cl.Message(content=response_text).send()

    history.append({"role": "assistant", "content": response_text})
    cl.user_session.set("history", history)