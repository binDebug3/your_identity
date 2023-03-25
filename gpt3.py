import openai
openai.api_key = "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" # replace with your API key

from random import choice
prompts = [
    "<name> was <age> years old and the paparazzi confused <name> with <celeb>",
    "A <age>-year-old <gender> named <name>, who looked eerily similar to <celeb>, found himself unexpectedly recruited to join a team of Hollywood actors in a high-stakes heist",
    "A <age>-year-old <gender> named <name>, who looked remarkably like <celeb>, finds themself stranded in a foreign country without their passport.",
    "A <age>-year-old <gender> named <name>, who bears an uncanny resemblance to <celeb>, discovers he has superpowers after being struck by lightning.",
    "A <age>-year-old <gender> named <name>, who is often mistaken for <celeb>, must impersonate the actor at a fan convention when the real <celeb> falls ill.",
    "A <age>-year-old <gender> named <name>, who is frequently compared to <celeb>, tries to win back their ex by writing a hit song about their relationship.",
    "A <age>-year-old <gender> named <name>, who looks eerily similar to <celeb>, gets mistaken for the soccer star during a trip to London and ends up living out their wildest dreams.",
    "A <age>-year-old <gender> named <name>, who bears a striking resemblance to <celeb>, accidentally lands a leading role in a blockbuster movie franctheire and struggles to cope with newfound fame.",
    "A <age>-year-old <gender> named <name>, who looks remarkably like <celeb>, becomes the subject of a viral internet meme and tries to use their newfound fame to jumpstart their acting career.",
    ""
]

def generate_prompt(name, gender, age, celeb):
    prompt = choice(prompts)
    
    prompt = (
        prompt.replace("<name>", name)
        .replace("<age>", age)
        .replace("<celeb>", celeb)
        .replace("<gender>", gender)
    )
    
    return prompt

def makeString(name = "", gender = "", age = "", celeb = ""):
    return generate_prompt(name, gender, age, celeb)

def generate_paragraph(input_string):
    prompt = f"Please write a 100 word funny story about the time when {input_string}."
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
    input_string = makeString(name = "jeff", gender = 'male', age = "24", celeb = "Ryan Golesing")
    print(generate_paragraph(input_string))