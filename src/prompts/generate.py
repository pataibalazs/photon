import logging
import os

import openai
import json

openai.api_key = os.getenv('OPENAI_SK', '')


def generate_prompts(in_sequence: str) -> list[str]:
    functions = [
        {
            "name": "write_post",
            "description": "Generates professional grade food photography using Stable Diffusion XL, with variations "
                           "given by the function arguments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt1": {
                        "type": "string",
                        "description":  "A description emphasizing the simplicity and purity of the food "
                                        "item. Focus on showcasing its natural colors, textures, and form without the "
                                        "addition of any extra ingredients or adornments. The styling should be "
                                        "hyperrealistic, emphasizing the food item in its most authentic state."
                    },
                    "prompt2": {
                        "type": "string",
                        "description":  "A description that highlights the artisanal or homemade aspect of the "
                                        "food item. Attention should be on the textures, natural imperfections, "
                                        "and authentic qualities of the food. Hyperrealistic styling should be "
                                        "employed to bring out the true essence of the food item without any "
                                        "additional elements."
                    },
                    "prompt3": {
                        "type": "string",
                        "description":  "A description that brings out the inherent beauty and simplicity of "
                                        "the food item. Focus on the color contrasts, natural shine, and shape of the "
                                        "food. Employ hyperrealistic styling to portray the food item in a simplistic "
                                        "yet captivating manner."

                    },
                }
            }
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.9,
        messages=[
            {
                "role": "user",
                "content": f"Given a food with additional features, generate prompts of 2-3 sentences for a "
                           f"state-of-the-art Diffusion"
                           f"model to generate glamorous food photography that can be used by restaurant chains to "
                           f"display it on their website. All of the prompts should emphasize that the picture is "
                           f"taken from above. The prompts should avoid adding elements that aren't in the initial "
                           f"description of the food. Avoid displaying people, complex backgrounds and image "
                           f"settings.An example:  Overhead shot of a bruschetta with chard, spinach, poached egg and "
                           f"dukkah plate, shot on Sony Alpha A7R IV, food photography style, macro lens, "
                           f"close up shot, 50mm lens f/ 1.4"
            },
            {
                "role": "user",
                "content": f"Food: {in_sequence}"
            }
        ],
        functions=functions,
        function_call={
            "name": functions[0]["name"]
        }
    )

    reply = response.choices[0].message['function_call']['arguments']

    logging.info(f'{reply=}')

    json_obj = json.loads(reply)

    prompts = list(json_obj.values())

    return prompts
