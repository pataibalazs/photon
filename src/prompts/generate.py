import os

import openai
import json

openai.api_key = os.getenv('OPENAI_SK', '')


def generate_prompts(in_sequence: str):
    functions = [
        {
            "name": "write_post",
            "description": "Shows the prompt1, prompt2, prompt3, prompt4, prompt5, prompt6, prompt7, prompt8, "
                           "prompt9, prompt10, prompt11, prompt12, prompt13, prompt14, prompt15 of some the input "
                           "food: " + "input",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt1": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt2": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt3": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt4": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt5": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt6": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt7": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt8": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt9": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt10": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt11": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt12": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt13": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt14": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    },
                    "prompt15": {
                        "type": "string",
                        "description": "One prompt of the given food, maximum 20 characters."
                    }
                }
            }
        }
    ]

    # multiple user interactions with different prompt each
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "system",
                "content": "You are a useful assistant."
            },
            {
                "role": "user",
                "content": f"Here is a food: {in_sequence}. Generate prompts 20 that will be used for an image model to generate a professional realistic image of the given food. For example ideal prompts would be: professional photograpghy, professional lighting, amazing camera, 4K, ultrarealistic, realistic, sharp detail.. etc. You can also generate prompts about the food origin or anything that could produce unique prompts which is connected to the food"
            }
        ],
        functions=functions,
        function_call={
            "name": functions[0]["name"]
        }
    )

    reply = response.choices[0].message['function_call']['arguments']
    json_obj = json.loads(reply)

    values = list(json_obj.values())

    return ', '.join(values)
