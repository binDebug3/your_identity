import openai
openai.api_key = "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" # replace with your API key

from random import choice
prompts = [
    "when <name> was <age> years old and the paparazzi confused <name> with <celeb>",
    "A <age>-year-old man named <name>, who looked eerily similar to <celeb>, found himself unexpectedly recruited to join a team of Hollywood actors in a high-stakes heist",
    "A <age>-year-old woman named <name>, who looked remarkably like <celeb>, finds herself stranded in a foreign country without her passport.",
    "A 25-year-old man named Max, who bears an uncanny resemblance to Chris Hemsworth, discovers he has superpowers after being struck by lightning.",
    "A 35-year-old man named Michael, who is often mistaken for Ryan Reynolds, must impersonate the actor at a fan convention when the real Reynolds falls ill.",
    "A 28-year-old woman named Sarah, who is frequently compared to Taylor Swift, tries to win back her ex-boyfriend by writing a hit song about their relationship.",
    "A 40-year-old man named David, who looks eerily similar to David Beckham, gets mistaken for the soccer star during a trip to London and ends up living out his wildest dreams.",
    "A 23-year-old woman named Emma, who bears a striking resemblance to Emma Watson, accidentally lands a leading role in a blockbuster movie franchise and struggles to cope with newfound fame.",
    "A 32-year-old man named Jake, who looks remarkably like Jake Gyllenhaal, becomes the subject of a viral internet meme and tries to use his newfound fame to jumpstart his acting career.",
    ""
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