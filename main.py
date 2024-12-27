import discord
import largest
import price
import asyncio
import os
import subprocess
import student

from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
from dotenv import load_dotenv


# Load the .env file
load_dotenv()

# Retrieve the token
TOKEN = os.getenv("DISCORD_TOKEN")

# Define the bot client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Command Tree for slash commands
tree = app_commands.CommandTree(client)

# Event: Bot is ready
@client.event
async def on_ready():
    asyncio.create_task(fetchData())
    
    try:
        synced = await tree.sync()
    except Exception as e:
        print(f"Error syncing commands: {e}")

async def fetchData():
    while True:
        await asyncio.sleep(86400)
        subprocess.run(["python", "api.py"])


# Slash command to check if the bot is online and responding
@tree.command(name="awake", description="Check if the bot is online.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Awake")




# Slash commads that will display sorted data from Vinmonopolet
@tree.command(name="student", description="Gives a list of the current cheapest raw alcohol products from Vinmonopolet in NOK")
async def ping(interaction: discord.Interaction):
    view = student.StudentView()
    embed = student.rawAlcoholEmbed(1)
    await interaction.response.send_message(embed=embed, view=view)


@tree.command(name="largest", description="Gives a list of the current largest alcohol products from Vinmonopolet buy volume")
async def ping(interaction: discord.Interaction):
    view = largest.LargestView()
    embed = largest.largestEmbed(1)
    await interaction.response.send_message(embed=embed, view=view)

@tree.command(name="price", description="Gives a list of the current cheapest items")
async def ping(interaction: discord.Interaction):
    view = price.PriceView()
    embed = price.priceEmbed(1)
    await interaction.response.send_message(embed=embed, view=view)




# Run the bot
client.run(TOKEN)

