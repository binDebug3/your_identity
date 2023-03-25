import openai
openai.api_key = "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" # replace with your API key

from random import choice
prompts = [
    "when <name> was <age> years old and the paparazzi confused <name> with <celeb>"
]

def generate_prompt(name, age, celeb):
    prompt = choice(prompts)
    
    prompt = prompt.replace("<name>", name).replace("<age>", age).replace("<celeb>", celeb)
    
    return prompt

def makeString(name = "", age = "", celeb = ""):
    return generate_prompt(name, age, celeb)

def generate_paragraph(input_string):
    prompt = f"Please write a funny story about the time {input_string}."
    model_engine = "text-davinci-002" # replace with the GPT-3 model engine you want to use
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    paragraph = response.choices[0].text.strip()
    return paragraph

if __name__ == "__main__":
    input_string = makeString(name = "jeff", age = "24", celeb = "Ryan Golesing")
    print(generate_paragraph(input_string))