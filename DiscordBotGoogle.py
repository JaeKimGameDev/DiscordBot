import discord
import os
import google.generativeai as genai
from dotenv import load_dotenv

def main():
    load_dotenv()
    os.environ['API_KEY'] = os.getenv("GOOGLEAI_API_KEY")

    genai.configure(api_key=os.environ['API_KEY'])

    class MyClient(discord.Client):
        async def on_ready(self):
            print('Logged on as {0}!'.format(self.user))
        async def on_message(self, message):
            message.content = message.content.lower()
            model = genai.GenerativeModel('gemini-1.5-flash')
            if message.author == self.user:
                return
            elif message.content.startswith('help'):
                await message.channel.send('commands: gemini. ex. gemini how are you?')
                return
            elif message.content.startswith('gemini'):
                user_input = message.content[6:]
                response = model.generate_content(user_input)
                print(response.text)
                if (len(response.text) > 2000):
                    counter=0
                    while (counter < len(response.text)):
                        counter += 2000
                        await message.channel.send(response.text[counter-2000:counter])
                else:
                    await message.channel.send(response.text)
                return

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(os.getenv("discordAPIKey"))

if __name__ == "__main__":
    main()