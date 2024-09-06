import discord
import os
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI

def main():
    load_dotenv()
    class MyClient(discord.Client):
        async def on_ready(self):
            print('Logged on as {0}!'.format(self.user))
        async def on_message(self, message):
            message.content = message.content.lower()
            if message.author == self.user:
                return
            elif message.content.startswith('help'):
                await message.channel.send('commands: hello, chatgpt, weather. ex. chatgpt how are you?')
                return
            elif message.content.startswith('hello'):
                await message.channel.send('Hello World')
            elif message.content.startswith('chatgpt'):

                client = OpenAI()
                chatGPTInput = [{"role": "system", "content": "You are a intelligent assistant."},
                                 {"role": "user", "content": message.content}]

                completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=chatGPTInput)

                await message.channel.send(completion.choices[0].message)

                return

            elif message.content.startswith('weather'):
                await message.channel.send('weather')
                return
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(os.getenv("discordAPIKey"))

if __name__ == "__main__":
    main()


