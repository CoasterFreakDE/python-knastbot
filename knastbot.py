import json
import os
import sys
import traceback
from asyncio import sleep
from os import listdir
from os.path import isfile, join

import discord
from discord.ext import commands


class KnastBot(commands.Bot):
    config_path = ''
    config = {}
    users = {}

    def __init__(self, config_path, config, users, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.config_path = config_path
        self.config = config
        self.users = users;

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.loop.create_task(self.status_task())

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        await self.process_commands(message)

    async def status_task(self):
        while True:
            await self.change_presence(activity=discord.Game('Melion.net | Dein meloniges Netzwerk'),
                                      status=discord.Status.online)
            await sleep(20)
            await self.change_presence(activity=discord.Game('MC Version » JAVA 1.15.2'), status=discord.Status.online)
            await sleep(20)
            await self.change_presence(activity=discord.Game('Discord » discord.gg/j6nAhV6'), status=discord.Status.online)
            await sleep(20)
            await self.change_presence(activity=discord.Game('Hilfe » .help'), status=discord.Status.online)
            await sleep(20)


def start(config_path, config, users):
    client = KnastBot(config_path=config_path, config=config, users=users, command_prefix=commands.when_mentioned_or('.'))

    if __name__ == '__main__':
        path = 'commands'
        extensions = [f for f in listdir(path) if isfile(join(path, f))]
        for extension in extensions:
            try:
                client.load_extension(f'commands.{extension[:-3]}')
            except Exception:
                print(f'Failed to load extension commands.{extension}.', file=sys.stderr)
                traceback.print_exc()

    client.run(config['token'])


def main():
    config_path = 'config'

    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    if not os.path.lexists(config_path):
        os.mkdir('config')

    if os.path.isfile(f'{config_path}/bots.json'):
        with open(f'{config_path}/bots.json', encoding='utf-8') as f:
            bots = json.load(f)
    else:
        bots = {"token": "BOT-1-Token", "knast_roleId": 11111, "blacklisted_roles": []}
        with open(f'{config_path}/bots.json', 'w') as f:
            json.dump(bots, f, indent=4)

    if os.path.isfile(f'{config_path}/users.json'):
        with open(f'{config_path}/users.json', encoding='utf-8') as f:
            users = json.load(f)
    else:
        users = {}
        with open(f'{config_path}/users.json', 'w') as f:
            json.dump(users, f, indent=4)

    start(config_path, bots, users)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Bot closed.')
