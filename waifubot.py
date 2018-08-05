import asyncio
import string
import time
from collections import namedtuple
from functools import wraps

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from meme_collections import (add_to_collection, delete_from_collection,
                              get_from_collection)
from misc import get_messages

bot = Bot(command_prefix='~')

SUPER_MODERATOR = '168080614405177344'
def needs_permission(bot):
    def decorator(func):
        @bot.command(pass_context=True)
        @wraps(func)
        async def wrapped(ctx, *args, **kwargs):
            if ctx.message.author.id == SUPER_MODERATOR or any(role.name == 'Moderator' for role in ctx.message.author.roles):
                return await func(ctx, *args, **kwargs)
            await bot.say("You don't have the permissions to run this command!")
        return wrapped
    return decorator
       
@bot.event
async def on_ready():
    print(bot.user.name, 'ready for action!')
    print('------')


# add new item to collection - .. <collection> <item>
# get item from collection  - ... <collection> - ... <collection>
# remove item from collection - .... <collection> <item>
async def handle_collections(message):
    split_message = message.content.split()
    prefix = split_message[0]
    ADD, GET, DELETE = '..',  '...', '....'

    if prefix == DELETE:
        reply = delete_from_collection(split_message[1], " ".join(split_message[2:]))
    if prefix == ADD:
        reply = add_to_collection(split_message[1], " ".join(split_message[2:]))
    if prefix == GET and len(split_message) == 2:
        reply = get_from_collection(split_message[1])
    
    await bot.send_message(destination=message.channel, content=reply)

@bot.event
async def on_message(message):
    if message.content.lower() == "right?" and message.author.id == '168080614405177344':
        await bot.send_message(message.channel, "yeah :thumbsup:")
    elif message.content[:2] == '..':
        await handle_collections(message)
    else:
        await bot.process_commands(message)

@bot.command(pass_context=True, alias='muni')
async def mooni(ctx, *args):
    if len(args) == 1:
        await bot.send_file(fp=f'files/{args[0]}.mp3', destination=ctx.message.channel)

@bot.command(pass_context=True)
async def prune(ctx, *args):
    if len(args) == 1:
        amount_to_prune = int(args[0])
        messages = await get_messages(bot, amount_to_prune)
        await bot.delete_messages(messages)
        await bot.send_message(content='Pruned **' + str(amount_to_prune) + '** message(s)!', destination=ctx.message.channel)
  

@bot.command
async def polako(*args):
    await bot.say('https://i.imgur.com/3CQ040d.png')

@bot.command(pass_context=True)
async def fizzbuzz(ctx, *args):
    # returns fizzbuzz reply for number
    with open('data/config.json', 'r') as file:
        config = json.load(file)
    threshold = config['threshold']
    user = ctx.user
    from misc import fizzbuz as fb


    values = [3, 5, 7, 13]
    responses = ['fizz', 'buzz', 'bizz', 'fuzz']
    names = ['Easy', 'Normal', 'Hard', 'Expert']
    difficulties = {name:{r:v for r,v in zip(responses[:i+1], values[:i+1])} for i, name in enumerate(names)}
    difficulties_string = ', '.join(names)

    user_response = str()
    possible_responses = [name.lower() for name in names]
    await bot.say('Choose difficulty: ' + difficulties_string)
    try:
        timer = time.time()
        while time.time() - timer < threshhold:
            messages = await get_messages(bot, 6)
            for message in messages:
                if message.content.lower() in possible_responses:
                    user_response = message.content.lower()
                    break
            if user_response != '':
                break
        else:
            if user_response == '':
                raise NoResponseError()
        
        await bot.say('poggers ' + user_response)

    except NoResponseError as e:
        await bot.send_message(destination=ctx.channel, content=e)
        


@bot.command(pass_context=True)
async def meme(ctx, *args):
    raw_message = "".join(args)
    message = ''
    num2words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    for char in raw_message:
        if char in string.digits:
            message += f":{num2words[int(char)]}:"
        else:
            message += f":regional_indicator_{char}:" if char != 'b' else ':b:'
    await bot.send_message(content=message, destination=ctx.message.channel)

@bot.command
async def flag_meme(*args):
    with open('files/flags.txt') as file:
        flags = file.read()
    flags = flags.split()

    def split_word_by_step(word, step):
        return [word[i:i+step] for i in range(0, len(word), step)]
            
    message= ''
    for word in args:
        split_word = split_word_by_step(word, 2)
        for i, pair in enumerate(split_word):
            if pair.upper() in flags:
                split_word[i] = f':flag_{pair.lower()}:'
        message += "".join(split_word) + " "
    if message:
        await bot.say(message)   

@needs_permission(bot)
async def echo(ctx, *args):
    for arg in args:
        await bot.say(arg)

@needs_permission(bot)
async def reload(ctx, *args):
    with open('rerun.txt', 'w') as file:
        file.write('y')
    await bot.say('`~~~ Reloading bot ~~~`')
    await bot.close()
        
@needs_permission(bot)
async def shutdown(ctx, *args):
    with open('rerun.txt', 'w') as file:
        file.write('n')
    await bot.say('`~~~ SHUTTING DOWN ~~~`')
    await bot.close()

class NoResponseError(Exception):
    def __init__(self):
        self.value = 'No response in given time limit'
    def __str__(self):
        return repr(self.value)
