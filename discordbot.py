# This example requires the 'message_content' intent.

import discord
import openai
import json
import re

openai.api_key = "OPENAI API KEY HERE"

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
client = discord.Client(intents=intents)


savepath = "mode.txt"


def strip_special_chars(str, message):
    message = message.replace(str, '')
    message = message.strip()
    return message

def get_chat(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1.0,
        messages=message
    )
    return response

def make_message(systemmsg, message):
    message_chat = []
    message_chat.append({"role": "system", "content": systemmsg})
    message_chat.append({"role": "user", "content": message})
    return message_chat

@client.event
async def on_ready():
    print(f'Logged in!')

@client.event
async def on_reaction_add(reaction,user):
    initial_message = reaction.message.content
    f = open("mode.txt", "r")
    mode_text = f.read()
    f.close()
    if (reaction.emoji.name == 'responsesnark'):
        response = get_chat(make_message("I want you to reply to this user with a sarcastic tone at their awkward statement. "+mode_text, initial_message))
        await reaction.message.reply(response["choices"][0]["message"]["content"])
    if (reaction.emoji.name == 'responselove'):
        response = get_chat(make_message("I want you to reply to this user with a loving and friendly tone at their lovely statement. "+mode_text, initial_message))
        await reaction.message.reply(response["choices"][0]["message"]["content"])
    if (reaction.emoji.name == 'responseangry'):
        response = get_chat(make_message("I want you to reply to this user with a angry and hostile tone at their stupid statement. "+mode_text, initial_message))
        await reaction.message.reply(response["choices"][0]["message"]["content"])
    if (reaction.emoji.name == 'responseapathetic'):
        response = get_chat(make_message("I want you to reply to this user with a apathetic, depressed and bored tone at their boring statement. "+mode_text, initial_message))
        await reaction.message.reply(response["choices"][0]["message"]["content"])

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!chatmode"):
        f = open("mode.txt", "w")
        initial_message = strip_special_chars('!chatmode', message.content)
        f.write(initial_message)
        f.close()
    if message.content.startswith("!currentmode"):
        f = open("mode.txt", "r")
        mode_text = f.read()
        f.close()
        await message.reply("The current chatmode is set to: "+mode_text)        
    if 'responsebot' in message.content.casefold():
        f = open("mode.txt", "r")
        mode_text = f.read()
        f.close()
        initial_message = re.sub('responsebot',  '',  message.content, flags=re.I)
        message_chat = []
        message_chat.append({"role": "system", "content": "Pretend you are not an AI. Do not mention you are a language AI model, pretend you are human. Reply to this user as if you were a normal person on a chat application and not an AI.  Pretend to have your own opinion and be able to respond to subjective questions. " + mode_text})
        message_chat.append({"role": "user", "content": initial_message})
        response = get_chat(message_chat)
        await message.reply(response["choices"][0]["message"]["content"])        



client.run('DISCORD API KEY HERE')