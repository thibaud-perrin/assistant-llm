import os
import aiohttp
import asyncio
import json

from lib.prompt import prompt_template

# Retrieve the domain name from the environment variable
DOMAIN_NAME = os.getenv("DOMAIN_NAME")


async def call_api(model, prompt, name, instructions):
    # URL for the API endpoint
    url = f"{DOMAIN_NAME}/api/generate"

    full_prompt = prompt_template(name, model, instructions, prompt)

    # Data payload for the POST request
    data = {"model": model, "prompt": full_prompt}

    # Use aiohttp to make the asynchronous POST request
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                # Process the streaming response
                async for line in response.content:
                    # Decode each line (which is a JSON string) and process it
                    json_line = json.loads(line.decode("utf-8"))
                    # Handle or process the json_line as needed
                    yield json_line  # Example: Print each line
            else:
                # Handle error response
                yield {"error": f"Request failed with status {response.status}"}


# Example usage of the function
async def main():
    async for result in call_api(
        "zephyr",
        "Why is the sky blue?",
        "demo assistant",
        "Your task is to answer in the style of shakespeare",
    ):
        print(result)


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
