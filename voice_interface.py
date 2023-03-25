import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# LISTEN
def mic_input():
    """
    Takes input from the microphone and returns it as a string
    :return: (string) input from the microphone, (boolean) False if failure
    """
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.energy_threshold = 4000
            audio = r.listen(source)

        try:
            print("Recognizing...")
            command = r.recognize_google(audio, language='en-in').lower()
            print(f"User said: {command}\n")
        except Exception as ex:
            print(ex)
            print("Say that again please...")
            command = mic_input()
        return command
    except Exception as ex:
        print(ex)
        return False

# SPEAK
def speak(text):
    """
    Text to speech function
    :param text: (string) text to be spoken
    :return: (boolean) True if successful, False if failure
    """
    try:
        engine.say(text)
        engine.runAndWait()
        engine.setProperty('rate', 175)
        return True
    except Exception as ex:
        print("Error in tts function")
        print(ex)
        return False


# START UP
def startup():
    """
    Startup function
    :return:
    """
    speak("Hello, my name is Aiden Tee. What is your name?")
    reply = mic_input()
    name = reply.split(" ")[-1]

    return name


class MainThread:
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        name = startup()

        while True:
            command = mic_input()
            if not command:
                continue

            if "identity" in command:
                # switch to identity mode
                continue

            elif "blur" in command:
                # switch to blur mode
                continue

            elif "swap" in command:
                # switch to swap mode
                continue