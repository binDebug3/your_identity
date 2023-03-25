import openai
openai.api_key = "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" # replace with your API key

from random import choice
prompts = [
    "when <name> was <age> years old and the paparazzi confused <name> with <celeb>",
    "A <age>-year-old man named <name>, who looked eerily similar to <celeb>, found himself unexpectedly recruited to join a team of Hollywood actors in a high-stakes heist",
    "A <age>-year-old woman named <name>, who looked remarkably like <celeb>, finds herself stranded in a foreign country without her passport.",
    "A <age>-year-old man named <name>, who bears an uncanny resemblance to <celeb>, discovers he has superpowers after being struck by lightning.",
    "A <age>-year-old man named <name>, who is often mistaken for <celeb>, must impersonate the actor at a fan convention when the real <celeb> falls ill.",
    "A <age>-year-old woman named <name>, who is frequently compared to <celeb>, tries to win back her ex-boyfriend by writing a hit song about their relationship.",
    "A <age>-year-old man named <name>, who looks eerily similar to <celeb>, gets mistaken for the soccer star during a trip to London and ends up living out his wildest dreams.",
    "A <age>-year-old woman named <name>, who bears a striking resemblance to <celeb>, accidentally lands a leading role in a blockbuster movie franchise and struggles to cope with newfound fame.",
    "A <age>-year-old man named <name>, who looks remarkably like <celeb>, becomes the subject of a viral internet meme and tries to use his newfound fame to jumpstart his acting career.",
    "A <age>-year-old woman named <name>, who is frequently mistaken for <celeb>, inadvertently becomes embroiled in a celebrity scandal after a case of mistaken identity."
]

def generate_prompt(name, age, celeb):
    prompt = choice(prompts)
    
    prompt = prompt.replace("<name>", name).replace("<age>", age).replace("<celeb>", celeb)
    
    return prompt

good_bye = [
    "Goodbye is the hardest thing to say to someone who means the world to you, especially when goodbye is not what you want." - Unknown

"Don't cry because it's over, smile because it happened." - Dr. Seuss

"How lucky I am to have something that makes saying goodbye so hard." - A.A. Milne

"Saying goodbye doesn't mean anything. It's the time we spent together that matters, not how we left it." - Trey Parker

"Goodbyes are not forever, are not the end; it simply means I'll miss you until we meet again." - Unknown

"It's time to say goodbye, but I think goodbyes are sad and I'd much rather say hello. Hello to a new adventure." - Ernie Harwell

"The story of life is quicker than the wink of an eye, the story of love is hello and goodbye...until we meet again." - Jimi Hendrix

"We started with a simple hello, but ended with a complicated goodbye." - Unknown

"How lucky I am to have known someone who was so hard to say goodbye to." - Unknown

"Farewell! God knows when we shall meet again." - William Shakespeare

"The pain of parting is nothing to the joy of meeting again." - Charles Dickens

"Goodbyes are not forever. Goodbyes are not the end. They simply mean I'll miss you until we meet again." - Unknown

"It's not the goodbye that hurts, but the flashbacks that follow." - Unknown

"We'll meet again, don't know where, don't know when, but I know we'll meet again some sunny day." - Vera Lynn

"The only way to make sense out of change is to plunge into it, move with it, and join the dance." - Alan Watts

"If you're brave enough to say goodbye, life will reward you with a new hello." - Paulo Coelho

"The two hardest things to say in life are hello for the first time and goodbye for the last." - Moira Rogers

"It's time to say goodbye, but I think goodbyes are sad and I'd much rather say hello. Hello to a new adventure." - Ernie Harwell

"The pain of parting is nothing to the joy of meeting again." - Charles Dickens

"I'll miss you until you come back but I hope you'll make it back safely to me." - Unknown

"Don't be dismayed at goodbyes. A farewell is necessary before you can meet again." - Richard Bach

"Goodbyes make you think. They make you realize what you've had, what you've lost, and what you've taken for granted." - Ritu Ghatourey

"I never say goodbye to anyone. I always prefer to say see you later." - Unknown

"It's not the goodbye that hurts, but the flashbacks that follow." - Unknown

"Remember me and smile, for it's better to forget than to remember me and cry." - Dr. Seuss

"Goodbye always makes my throat hurt." - Charlie Brown

"Goodbye is not a word, it's a feeling." - Unknown

"Every goodbye makes the next hello closer." - Unknown"
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