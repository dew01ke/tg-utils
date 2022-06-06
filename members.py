import asyncio
import sys
from telethon import TelegramClient, events

api_id =
api_hash = ''
target_filename = 'members_{}.txt'

async def readline(prompt):
    print(prompt, end='', flush=True)
    return (await asyncio.get_running_loop().run_in_executor(None, sys.stdin.readline)).rstrip()

async def get_chats(client):
    sources = []
    chats = await client.get_dialogs()

    for index, chat in enumerate(chats):
        print('#{}: {}'.format(index, chat.name))

    return chats

async def get_members(client, chat):
    members = await client.get_participants(chat)

    return members

def transform_members(members):
    output = []

    for member in members:
        if not member.bot:
            output.append('{} {}'.format(member.id, member.username if member.username else ''))

    return '\r\n'.join(output)

def save_to_file(filename, content):
    with open(filename, 'w', encoding = 'utf-8') as f:
        f.write(content)

async def main():
    client = TelegramClient('tgutils', api_id, api_hash)

    await client.start()

    chats = await get_chats(client)

    index = await readline('Chat index to fetch: ')
    chat = chats[int(index)]

    members = await get_members(client, chat)
    filename = target_filename.format(chat.name)
    save_to_file(filename, transform_members(members))

asyncio.run(main())