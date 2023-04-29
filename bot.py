import discord
import responses
from dotenv import load_dotenv

import os

# Send messages
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    #async def on_message(self, message):
    #    print(f'Message from {message.author}: {message.content}')
    
    async def on_message(self, message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == self.user:
            return

        # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        # If the user message contains a '?' in front of the text, it becomes a private message
        if user_message[0] == '?':
            user_message = user_message[1:]  # [1:] Removes the '?'
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)



def run_discord_bot():
    load_dotenv()
    TOKEN = os.environ.get("TOKEN")
    print("TOKEN", TOKEN)


    intents = discord.Intents.default()
    intents.message_content = True
    
    client = MyClient(intents=intents)
    client.run(TOKEN)

