import os
from dotenv import load_dotenv
import tweepy
import random
import asyncio
import aiocron
import requests

load_dotenv()

auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_CLIENT_KEY"),
    os.getenv("TWITTER_CLIENT_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET"),
)

api = tweepy.API(auth)


session = requests.Session()
session.headers.update(Authorization=f"Bearer {os.getenv('MASTODON_ACCESS_TOKEN')}")


emojis = [
    "🏳️‍⚧️",
    "🦀",
    "🎈",
    "👗",
    "☕️",
    "🐶",
    "🎛",
    "💜",
    "🚃",
    "👩‍💻",
    "💕",
    "👾",
    "🤖",
    "🦞",
    "🔥",
    "✨",
    "💾",
    "📸",
    "♀️",
    "🏴‍☠️",
    "🌈",
    "🌆",
    "🎀",
    "🧋",
    "😈",
    "🎸",
    "💅",
]


@aiocron.crontab("*/1 * * * *")
async def replace_emoji():
    emoji = random.sample(emojis, 3)
    print(f"Replacing emoji with: {emoji}")

    name = "bronke" if random.random() > 0.95 else "brooke"
    pronouns = "she/they" if random.random() > 0.95 else "she/her"

    display_name = name + " chalmers ⊃ " + "\u200b".join(emoji)

    api.update_profile(
        name=display_name,
        location=pronouns + ", @breq@tacobelllabs.net",
    )

    session.patch(
        "https://tacobelllabs.net/api/v1/accounts/update_credentials",
        data={
            "display_name": display_name,
            "note": f'19. 🏳️‍⚧️. {pronouns}. tinkering with code, chips, math, music. do it all. "the cutest fucking person here" -some girl at a rave. blåhaj.  boston & maine. quartz 💕',
        },
    ).raise_for_status()


asyncio.get_event_loop().run_forever()
