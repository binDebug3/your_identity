import openai
openai.api_key = "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" # replace with your API key

def makeString(name = "", age = "", celeb = ""):
    return f"when {name} was {age} years old and the paparazzi confused {name} with {celeb}"

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