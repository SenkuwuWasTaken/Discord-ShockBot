import discord
from discord.ext import commands
from pishock import PiShockAPI
from discord import app_commands
import json
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

if not os.path.exists("settings.json"):
    default_settings = {
        "username": "",
        "api_key": "",
        "sharecode": "",
        "bot_token": "",
        "shockIntensityScale": 100,
        "myUserID": 0,
        "ShockBotAdmins": [],
        "bannedUserIDs": []
    }
    with open("settings.json", "w") as file:
        json.dump(default_settings, file, indent=4)
    print("settings.json created with empty values.")


with open('settings.json', 'r') as file:
    settingsData = json.load(file)

myUserID = int(settingsData['myUserID'])
ShockAdmins = [int(user_id) for user_id in settingsData['ShockBotAdmins']]
bannedUsers = [int(user_id) for user_id in settingsData['bannedUserIDs']]
username = settingsData['username']
api_key = settingsData['api_key']
sharecode = settingsData['sharecode']
bot_token = settingsData['bot_token']
shockIntensityScale = settingsData['shockIntensityScale']


api = PiShockAPI(username, api_key)
shocker = api.shocker(sharecode)
if not api.verify_credentials():
    exit("Incorrect Pishock Credentials")


def save_json(value):
    with open('data.json', 'w') as f:
        json.dump(value, f, indent=4)


def is_banned(interaction: discord.Interaction):
    if int(interaction.user.id) in bannedUsers:
        return True
    return False


# Event to indicate when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")


@bot.event
async def on_error(event, *args, **kwargs):
    import traceback
    print(f"An error occurred in event {event}:")
    traceback.print_exc()  # Print the full traceback to help debug


@bot.tree.command(name="set_intensity_scale")
@app_commands.describe(scale="scale all intensity relative to this value (1-100)")
async def set_intensity_scale(interaction: discord.Interaction, scale: int):
    global shockIntensityScale

    if int(interaction.user.id) != int(myUserID):
        await interaction.response.send_message(
            "You do not have permission to use this command.", ephemeral=True
        )
        return
    if scale < 1 or scale > 100:
        shockIntensityScale = scale
        settingsData['shockIntensityScale'] = shockIntensityScale
        save_json(settingsData)
    else:
        print("Invalid scaling value")
    return


@bot.tree.command(name="shock")
@app_commands.describe(duration="The duration in seconds (0.1-1.5)", intensity="The intensity level (1-100)")
async def shock(interaction: discord.Interaction, duration: int, intensity: int):
    user = interaction.user
    print(f"User {user.name} invoked 'shock' with duration={duration} and intensity={intensity}")
    if is_banned(interaction):
        await interaction.response.send_message(f"Command not sent, you are banned from using this bot.", ephemeral=True)
        print(f"Command not ran, {interaction.user.name} is banned")
        return

    if intensity < 1 or intensity > 100:
        await interaction.response.send_message(f"Invalid intensity.", ephemeral=True)
        print("Command not sent, invalid intensity.")
        return
    if duration < 0.1 or duration > 1.5:
        await interaction.response.send_message(f"Invalid duration.", ephemeral=True)
        print("Command not sent, invalid duration.")
        return

    shocker.shock(duration, intensity * shockIntensityScale)

    await interaction.response.send_message(
        f"{username} shocked by {user.name} at intensity {intensity} for {duration} seconds :3"
    )


@bot.tree.command(name="vibrate_shocker")
@app_commands.describe(duration="The duration in seconds (0.1-1.5)", intensity="The intensity level (1-100)")
async def vibrate(interaction: discord.Interaction, duration: int, intensity: int):
    user = interaction.user
    print(f"User {user.name} invoked 'vibrateshocker' with duration={duration} and intensity={intensity}")
    if is_banned(interaction):
        await interaction.response.send_message(f"Command not sent, you are banned from using this bot.", ephemeral=True)
        print(f"Command not ran, {interaction.user.name} is banned")
        return

    if intensity < 1 or intensity > 100:
        await interaction.response.send_message(f"Invalid intensity.", ephemeral=True)
        print("Command not sent, invalid intensity.")
        return
    if duration < 0.1 or duration > 1.5:
        await interaction.response.send_message(f"Invalid duration.", ephemeral=True)
        print("Command not sent, invalid duration.")
        return

    shocker.vibrate(duration, intensity * shockIntensityScale)

    await interaction.response.send_message(
        f"{username} shocked by {user.name} at intensity {intensity} for {duration} seconds :3"
    )


@bot.tree.command(name="pause_shocker")
async def pauseShocker(interaction: discord.Interaction):

    if interaction.user.id not in ShockAdmins :
        await interaction.response.send_message(
            "You do not have permission to run this command.", ephemeral=True
        )
        return

    shocker.pause(True)
    await interaction.response.send_message("Shocker paused")
    print(f"{interaction.user.name} paused the shocker.")


@bot.tree.command(name="unpause_shocker")
async def unpauseShocker(interaction: discord.Interaction):

    if interaction.user.id not in ShockAdmins:
        await interaction.response.send_message(
            "You do not have permission to run this command.", ephemeral=True
        )
        return

    shocker.pause(False)
    await interaction.response.send_message("Shocker paused")
    print(f"{interaction.user.name} paused the shocker.")


bot.run(bot_token)
