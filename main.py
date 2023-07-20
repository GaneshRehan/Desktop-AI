"""This is a Personal Desktop AI Assistant."""


print("Code began.")        # Indicates that code execution has started.

import speech_recognition as sr
import wikipedia
import openai
import pyttsx3
import webbrowser
import datetime
import os
import requests
from my_openai_apikey import my_apikey
import nltk

engine = pyttsx3.init()


def say(text):
    engine.say(text)
    engine.setProperty('rate',150)
    engine.runAndWait()


def lang_processing(query):
    pass


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source=source, duration=0.6)
        r.energy_threshold=300
        r.pause_threshold = 1
        audio = r.listen(source=source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio_data=audio, language="en-in")
            query = query.lower()
            print(f"User: {query}")
            return query
        except Exception:
            return "Some error occurred!!! Apologies from Jarvis "


def open_site(query):
    temp_query = query.split(" ")
    if any(i == temp_query.index('open') for i in [0, 1, 2]):
        site = temp_query[temp_query.index('open') + 1]
    url1=f"https://www.{site}.com"
    url2=f"https://www.{site}.in"
    if requests.head(url=url1).status_code == requests.codes.ok:
        say(text=f"Opening {site}")
        webbrowser.open(url=url1)
    elif requests.head(url=url2).status_code == requests.codes.ok:
        say(text=f"Opening {site}")
        webbrowser.open(url=url2)
    else:
        response = "That particular site does not exist."
        print(f"Jarvis: {response}")
        say(text=response)


def ai(prompt):
    openai.api_key = my_apikey

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    try:
        reply=response["choices"][0]["text"]
        print(f"Jarvis: {reply}")
        say(reply)
        # say(reply)
    except "UndefinedVariableError":
        print("Jarvis: Sorry! Couldn't find anything related to your request.")


chatStr=""


def chat(query):
    global chatStr
    # print(chatStr)
    openai.api_key=my_apikey
    chatStr += f"User: {query}\nJarvis"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(f"Jarvis: {response['choices'][0]['text']}")
    say(text=response['choices'][0]['text'])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def current_date_time(query):
    current_date = datetime.date.today()
    current_time = datetime.datetime.now().strftime("%H:%M")
    if "the date" in query:
        date_response = f"The current date is {current_date}"
        print(f"Jarvis: {date_response}")
        say(text=date_response)
    if "the time" in query:
        time_response = f"The current time is {current_time}"
        print(f"Jarvis: {time_response}")
        say(text=time_response)


if __name__ == "__main__":
    print("Jarvis: Hello! I am Jarvis, your personal desktop assistant. How may I help you?")
    # query = input("Jarvis: ")
    # say(text="Hello! I am Jarvis, your personal desktop assistant. How may I help you?")
    while True:
        print("Jarvis: Listening...", end=" ")
        query = takeCommand()
        # print("Jarvis: Listening")
        # query=input("User: ")

        if "open" in query:
            open_site(query=query)
            continue

        if "is date" in query or "is time" in query:
            current_date_time(query=query)
            continue

        if "shutdown" in query or "turn off" in query:
            response="Are you sure you want to shutdown the device? Please reply with a 'yes' or 'no'."
            print(f"Jarvis: {response}")
            say(text=response)
            reply = takeCommand()
            reply = reply.lower()
            if reply == "yes":
                os.system(command='shutdown /s /t 0')

        if "reboot" in query:
            response = "Are you sure you want to reboot the device? Please reply with a 'yes' or 'no'."
            print(f"Jarvis: {response}")
            say(text=response)
            reply = takeCommand()
            reply = reply.lower()
            if reply == "yes":
                os.system(command="shutdown /r /t 0")

        if "jarvis quit" in query or "bye jarvis" in query:
            response = "Are you sure you want to quit Jarvis? Please reply with a 'yes' or 'no'."
            print(f"Jarvis: {response}")
            say(text=response)
            reply = takeCommand()
            reply = reply.lower()
            if reply == "yes":
                break

        if query == "reset chat":
            chatStr=""
            continue

        # if "using artificial intelligence" in query or "using ai" in query:
        ai(prompt=query)

        # chat(query=query)

        # say(text=f"User: {query}")










    print("Code over.")


# Please note that to use this, you need an ACTIVE INTERNET CONNECTION. Else it won't work.