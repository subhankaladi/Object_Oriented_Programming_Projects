import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

# Load environment variables from .env file
load_dotenv()


# 💡 Encapsulation: All model setup logic is wrapped inside a class
class ModelProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.provider = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai"
        )

    def get_model(self):
        return OpenAIChatCompletionsModel(
            model="gemini-2.0-flash",
            openai_client=self.provider
        )


# 💡 Abstraction: User interacts with this class instead of handling low-level agent setup
class GreetingAgentApp:
    def __init__(self, model):
        self.agent = Agent(
            name="Greeting Agent",
            instructions=(
                "You are a Greeting Agent. Your task is to greet the user with a friendly message. "
                "When someone says hi, you reply back with 'Salam from Subhan Kaladi'. "
                "If someone says bye, then say 'Allah Hafiz from Subhan Kaladi'. "
                "If someone asks something else, then say 'Subhan is here just for greeting, I can't answer anything else, sorry.'"
            ),
            model=model
        )

    # 💡 Polymorphism: You can later add more types of agents by overriding this method
    def get_response(self, user_input: str) -> str:
        result = Runner.run_sync(self.agent, user_input)
        return result.final_output


# Main Application Runner
def main():
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    model_provider = ModelProvider(gemini_api_key)
    model = model_provider.get_model()

    app = GreetingAgentApp(model)

    user_question = input("Please enter your question: ")
    response = app.get_response(user_question)

    print(response)


if __name__ == "__main__":
    main()
