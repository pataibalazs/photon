import openai

openai.api_key = ""

def callGPT(input):
    messages = [
        {"role": "user",
        "content": f"""Given the input, which includes a primary food item and possibly additional descriptors, your task is to generate keywords representing the visible ingredients of the specified food. The ingredients you list should be those that would typically be visible in high-quality, stunning photographs of the food, taken using top-tier professional equipment. These photographs emphasize the allure and visual appeal of the food. Consider both the main food item and any accompanying descriptors when listing the visible ingredients. Do not have any new lines, or numbers, just comas Input: '{input}'."""
        }

    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = completion.choices[0].message.content
    return reply