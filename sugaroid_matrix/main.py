#!/usr/bin/env python3

import asyncio
import json
import time

from aiohttp import ClientConnectionError, ServerDisconnectedError
from dotenv import load_dotenv
from nio import RoomMessageText
from nio import AsyncClient, LoginResponse
from sugaroid.sugaroid import Sugaroid
from .callbacks import Callbacks
from .config import Config


CONFIG_FILE = "credentials.json"


def write_details_to_disk(resp: LoginResponse, homeserver) -> None:
    """Writes the required login details to disk so we can log in later without
    using a password.

    Arguments:
        resp {LoginResponse} -- the successful client login response.
        homeserver -- URL of homeserver, e.g. "https://matrix.example.org"
    """
    # open the config file in write-mode
    with open(CONFIG_FILE, "w") as f:
        # write the login details to disk
        json.dump(
            {
                "homeserver": homeserver,  # e.g. "https://matrix.example.org"
                "user_id": resp.user_id,  # e.g. "@user:example.org"
                "device_id": resp.device_id,  # device ID, 10 uppercase letters
                "access_token": resp.access_token  # cryptogr. access token
            },
            f
        )


async def main(sugaroid: Sugaroid) -> None:
    config = Config.from_environment()
    client = AsyncClient(config['homeserver'])
    client.access_token = config['access_token']
    client.user_id = config['user_id']
    client.device_id = config['device_id']

    print("Status: sleeping for 30000")
    await client.sync(30000)
    print("Resuming:")
    cb = Callbacks(client, sugaroid=sugaroid)
    client.add_event_callback(cb.message, RoomMessageText)
    while True:
        try:
            await client.sync_forever(timeout=30000, full_state=True)
        except KeyboardInterrupt:
            break
        except (ClientConnectionError, ServerDisconnectedError):
            print("Unable to connect to homeserver, retrying in 15s")
            time.sleep(15)
        finally:
            await client.close()


def bootstrap():
    load_dotenv()
    sugaroid = Sugaroid()
    asyncio.get_event_loop().run_until_complete(main(sugaroid))


if __name__ == "__main__":
    bootstrap()
