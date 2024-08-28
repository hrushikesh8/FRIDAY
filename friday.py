import pyttsx3
import speech_recognition as sr
from datetime import datetime
from num2words import num2words
import webbrowser
import time
import os
from AppOpener import open, close
import pyautogui
import getpass
from dotenv import load_dotenv
from openai import OpenAI

# OpenAI code

# Load variables from the .env file into the environment
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# App continuation code
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
  engine.say(audio)
  engine.runAndWait()
  engine.setProperty('rate', 190)


def greetMe():
  hour = int(datetime.now().hour)
  if 0 <= hour < 12:
    speak("Good Morning!")
  elif 12 <= hour < 18:
    speak("Good Afternoon!")
  else:
    speak("Good Evening!")
  speak("This is Friday, your assistant.")


def takeCommand():
  # It takes microphone input from the user and returns string output
  r = sr.Recognizer()     
  with sr.Microphone() as source:
    speak("Listening")
    print("Listening...")
    r.pause_threshold = 1
    audio = r.listen(source)

  try:
    print("Recognizing...")
    query = r.recognize_google(audio, language='en-in')
    print(f"User said: {query}\n")
  except Exception as e:
    print(e)
    speak("Say it again please")
    print("Say that again please...")
    return "None"

  return query


def get_completion(prompt, model="gpt-3.5-turbo-1106"):
  messages = [{"role": "user", "content": prompt}]
  response = client.chat.completions.create(model=model,
                                            messages=messages,
                                            temperature=0)
  output_of_api = response.choices[0].message.content
  return output_of_api


def handle_user_input():
  user_input = takeCommand().lower()

  prompt = f"""
    You are going to act as a voice assistant named FRIDAY giving friendly and a bit sarcastic replies as a chatbot,
    If the user input is like a query or expecting an answer, clarifying something or want to know about, just give out the answer,
    or else if the user input is not like asking a question, if you cannot give any accurate response, just give out the response what you can in a friendly manner.
    Give friendly responses and results which are very short and sweet so that any age of human can understand,
    give a reply in less than 3 or 4 lines mostly,
    but give out more than that depending on the input delimited by triple backticks.
    Also process the language of User input and respond in the same language as reply if you know, if not reply in English only
    Your main task is to differ between asking a query, if asking a query give the answer and give out the string "system_task" if it is like asking about the time, take notes, 
    access keyboard or mouse, searching for in web, news, play music, open apps, want to close session, shutdown or sleep the system and any of kind similar to what system tasks are - like which you cannot perform.

    User input: ```{user_input}```
    """
  try:
    response = get_completion(prompt)
  except:
    response = "Can you say it again!!"

  return response, user_input


def namaste():
  greetMe()
  while True:
    speak("How can I assist you today?")
    main_query, query = handle_user_input()
    # response = get_completion(handle_user_input())
    print(main_query)
    # time.sleep(4)

    if main_query != "system_task":
      speak(main_query)
      time.sleep(1)
    else:
      #take notes
      if 'note' in query or 'take notes' in query:
        open("notepad", match_closest=True, output=False)
        speak("What do you want to type")
        sentence = takeCommand().lower()
        time.sleep(5)
        pyautogui.typewrite(sentence, interval=0.1)
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)
        pyautogui.press('enter')

      # condition to open installed applications
      if 'open' in query:
        try:
          query_to_arr = query.split(" ")
          if "the" in query:
            query_to_arr.remove("the")
          app_name = query_to_arr[query_to_arr.index("open") + 1]
          open_result = open(f"${app_name}", match_closest=True, output=False)
          if open_result:
            speak(f"Opened {app_name}")
          else:
            pass
        except Exception as e:
          speak("Could not find the app you are looking for.")

      if "close" in query:
        query_to_arr = query.split(" ")
        if "the" in query:
          query_to_arr.remove("the")
        app_name = query_to_arr[query_to_arr.index("close") + 1]
        close(app_name, match_closest=True, output=False)
        speak("Closed the app")

      if 'keyboard' in query:
        keys_info = takeCommand().lower()
        while keys_info:
          if 'type' in keys_info:
            pyautogui.typewrite(sentence, interval=0.1)
          if 'hotkey' in keys_info or 'hot ki' in keys_info:
            speak("What is the hot key you want to")
            hot_key_command = takeCommand().lower().split(" ")
            for i in hot_key_command:
              pyautogui.hotkey(i, end=" ")
          else:
            keys_info = False

      if 'news' in query:
        webbrowser.open(
            "https://news.google.com/foryou?hl=en-IN&gl=IN&ceid=IN:en")

      if 'search' in query:
        web_search = query.replace(" ", "+")
        webbrowser.open(f"https://www.google.com/search?q={web_search}")
        pyautogui.press("browsersearch")

      if 'time' in query:
        current_time = datetime.now().time()
        time_in_words = f"{num2words(current_time.hour)} {num2words(current_time.minute)}"
        speak(f"Sir, the time is {time_in_words}")

      if 'my name' in query:
        username = getpass.getuser()
        speak(f"Hello {username} what can I do for you")

      if 'who are you' in query or 'what can you do' in query:
        speak(
            'I am your personal assistant. I am programmed to minor tasks like opening youtube, google chrome and give search results'
        )

      if "who made you" in query or "who created you" in query or "who discovered you" in query:
        speak("I was built by TFI")

      if 'friday' in query or 'hello' in query:
        speak("This is Friday, I am ready to take your command sir")

      if 'bye' in query or 'exit' in query or 'bye-bye' in query:
        speak("Goodbye!, Take care")
        exit()

      if 'shutdown' in query or 'shut down' in query:
        # pyautogui.hotkey('alt','f4')
        shutdown_key = takeCommand().lower()
        if 'yes' in shutdown_key or 'go on' in shutdown_key:
          os.system("shutdown /s /t 2")
          speak("Are you sure to Shutdown the system, say Yes to proceed")
        else:
          speak("Okay! Your PC will not shut down.")


if __name__ == "__main__":
  namaste()
