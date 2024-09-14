import asyncio
import logging
from typing import List, Dict
import google.generativeai as genai
from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

class GeminiChatCompletion:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def get_chat_message_content(self, chat_history: ChatHistory, kernel: Kernel):
        messages = [{"role": "user" if msg.origin == "user" else "model", "parts": [msg.content]} 
                    for msg in chat_history.messages]
        
        response = await asyncio.to_thread(
            self.model.generate_content,
            messages
        )
        
        return response.text

class LightsPlugin:
    @kernel_function
    def turn_on(self) -> str:
        return "Lights turned on."

    @kernel_function
    def turn_off(self) -> str:
        return "Lights turned off."

async def main():
    # Initialize the kernel
    kernel = Kernel()

    # Add Gemini chat completion
    chat_completion = GeminiChatCompletion(api_key="llm_api_key")
    
    # Set the logging level for semantic_kernel.kernel to DEBUG.
    setup_logging()
    logging.getLogger("kernel").setLevel(logging.DEBUG)

    # Add a plugin
    kernel.add_plugin(
        LightsPlugin(),
        plugin_name="Lights",
    )

    # Create a history of the conversation
    history = ChatHistory()

    # Initiate a back-and-forth chat
    while True:
        # Collect user input
        user_input = input("User > ")
        
        # Terminate the loop if the user says "exit"
        if user_input.lower() == "exit":
            break

        # Add user input to the history
        history.add_user_message(user_input)

        # Get the response from Gemini
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            kernel=kernel,
        )

        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the assistant to the chat history
        history.add_assistant_message(result)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())