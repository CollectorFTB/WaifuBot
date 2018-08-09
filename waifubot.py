import asyncio
import string
import time
from functools import wraps

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from meme_collections import (add_to_collection, delete_from_collection,
                              get_from_collection, handle_collections)
from misc import get_messages, load_file, split_word_by_step, turn_into_emoji

# global vars
bot = Bot(command_prefix='~')

# data vars
CONFIG = load_file('data/config.json')
SPECIAL_IDS = load_file('data/ids.json')
SUPER_MODERATOR = SPECIAL_IDS[0]
last_message = ''


def needs_permission(bot, hidden=False):
    """Decorator to make a command that forces the user to have sufficient permissions to use the command
    
    Arguments:
        bot {Bot} -- the global scope bot to send error messages
    
    Keyword Arguments:
        hidden {bool} -- if true, the command will not appear in the built in help command (default: {False})
    
    """

    def decorator(func, hidden=hidden):
        @bot.command(pass_context=True ,hidden=hidden)
        @wraps(func)
        async def wrapped(ctx, *args, **kwargs):
            if ctx.message.author.id == SUPER_MODERATOR or any(role.name == 'Moderator' for role in ctx.message.author.roles):
                return await func(ctx, *args, **kwargs)
            await bot.say("You don't have the permissions to run this command!")
        return wrapped
    return decorator

@bot.event
async def on_ready():
    """event that gets triggered whenever the bot is started
    """

    print(bot.user.name, 'ready for action!')
    print('------')

@bot.event
async def on_message(message):
    """Event that happens whenever a message is sent
    
    Arguments:
        message {Message} -- the sent message (acts like)
    """

    if message.content[:2] == '..':
        await bot.send_message(content=handle_collections(message), destination=message.channel)
    elif message.content[::-len(message.content)-1] == '::':
        await turn_into_emoji(message)
    else:
        await bot.process_commands(message)


@bot.command(pass_context=True, alias='muni')
async def mooni(ctx, *args):
    """Command to send mp3 file containing mooni sample
    
    Arguments:
        ctx {[type]} -- [description]
    """

    if len(args) == 1:
        await bot.send_file(fp=f'files/{args[0]}.mp3', destination=ctx.message.channel)


"""
>>> ~prune 5
"""
@bot.command(pass_context=True)
async def prune(ctx, amount_to_prune, *args):
    """Command to delete messages from a channel
    
    Arguments:
        ctx {[Context]} -- deletes messages from ctx.channel
    """
    messages = await get_messages(bot, ctx, amount_to_prune)
    await bot.delete_messages(messages)
    await bot.say('Pruned **' + str(amount_to_prune) + '** message(s)!')
  

"""
>>> ~polako
https://i.imgur.com/3CQ040d.png
"""
@bot.command()
async def polako(*args):
    """polako meme
    """

    await bot.say('https://i.imgur.com/3CQ040d.png')

@bot.command(pass_context=True)
async def fizzbuzz(ctx, *args):
    """Command to play fizzbuzz with user
    """
    threshold = CONFIG['threshold']
    from misc import fizzbuzz as fb


    values = [3, 5, 7, 13]
    responses = ['fizz', 'buzz', 'bizz', 'fuzz']
    names = ['Easy', 'Normal', 'Hard', 'Expert']
    difficulties = {name.lower():{value:response for response, value in zip(responses[:i+1], values[:i+1])} for i, name in enumerate(names)}
    difficulties_string = ', '.join(names)
    name_responses = [name.lower() for name in names]

    def valid_difficulty_response(message):
        name_responses = [name.lower() for name in names]
        return message.content.lower() in name_responses
    def valid_number_response(message):
        return int(message.content) if message.content.isdigit() else False
    def valid_fizzbuzz_response(message):
        if message.content.isdigit():
            return True
        responses = ['fizz', 'buzz', 'bizz', 'fuzz']
        fizzbuzz_split = split_word_by_step(message.content, 4)
        i = -1
        for word in fizzbuzz_split:
            if word in responses:
                j = responses.index(word)
                if j > i:
                    i = j
                else:
                    return False
            else:
                return False
        return message

    try:
        await bot.say('Choose difficulty: ' + difficulties_string)
        response = await wait_for_response(ctx, valid_difficulty_response, threshold)
        await bot.say('Lets Go!')

        difficulty = difficulties[response.lower()]
        current = 1
        while True:
            current_fizzbuzz = fb(current, difficulty)
            current += 1
            await bot.say(current_fizzbuzz)
            
            response = await wait_for_response(ctx, valid_fizzbuzz_response, threshold)
            current_fizzbuzz = fb(current, difficulty)
            response = int(response) if response.isdigit() else response
            if response == current_fizzbuzz:
                current += 1
            else:
                raise BadResponseError("Wrong answer, I Win!")
    except BadResponseError as e:
        await bot.say(e.value)


async def wait_for_response(ctx, response_func, time_threshold):
    """Command to allow interative talk with user
    
    Arguments:
        response_func {function} -- Function to check each message to see if its valid
        time_threshold {int} -- Time to wait before raising an exception
    """

    timer = time.time()
    user_response = ''
    global last_message
    while time.time() - timer < time_threshold:
        user_responses = [message for message in reversed(await get_messages(bot, ctx, 2)) if message.author == ctx.message.author and response_func(message) and message.content != last_message]
        if user_responses:
            user_response = user_responses[0].content
            last_message = user_response            
            break
    else:
        raise BadResponseError('Error: No response in given time')
    return user_response


"""
>>> ~meme a1
:regional_indicator_a::one:
>>> ~meme 2 plus 2
:two::regional_indicator_p::regional_indicator_l::regional_indicator_u::regional_indicator_s::two:
"""
@bot.command(pass_context=True)
async def meme(ctx, *args):
    """
    Turn the message into alphanumeric emojis 
    """
    raw_message = "".join(args)
    message = ''
    num2words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    for char in raw_message:
        if char in string.digits:
            message += f":{num2words[int(char)]}:"
        else:
            message += f":regional_indicator_{char}:" if char != 'b' else ':b:'
    await bot.say(message)

"""
>>> ~flag_meme canada 
:flag_ca::flag_na:da
>>> ~flag_meme 123
123
"""
@bot.command()
async def flag_meme(*args):
    """Turn the message into a flag meme
    """
    with open('data/flags.txt') as file:
        flags = file.read()
    flags = flags.split()

    message= ''
    for word in args:
        split_word = split_word_by_step(word, 2)
        for i, pair in enumerate(split_word):
            if pair.upper() in flags:
                split_word[i] = f':flag_{pair.lower()}:'
        message += "".join(split_word) + " "
    if message:
        await bot.say(message)   

"""
>>> ~echo 123 test
123 test
"""
@needs_permission(bot, hidden=True)
async def echo(ctx, *args):
    """Repeat a message in chat
    """

    for arg in args:
        await bot.say(arg)

@needs_permission(bot, hidden=True)
async def reload(ctx, *args):
    """Signal to main function that it doesn't need to restart
    """
    with open('rerun.txt', 'w') as file:
        file.write('y')
    await bot.say('`~~~ Reloading bot ~~~`')
    await bot.close()
        
@needs_permission(bot, hidden=True)
async def shutdown(ctx, *args):
    """Signal to main function that it needs to reload the bot
    """
    with open('data/rerun.txt', 'w') as file:
        file.write('n')
    await bot.say('`~~~ SHUTTING DOWN ~~~`')
    await bot.close()

@bot.command(pass_context=True, hidden=True)
async def secret(ctx, *args):
    """monkaS
    """
    if ctx.message.author.id in SPECIAL_IDS:
        with open('data/secret.txt', 'r') as file:
            secret_message = file.read()
        await bot.send_message(destination=ctx.message.author, content=secret_message)


"""
>>> ~id Collector
406768116808128
(fake id)
"""
@needs_permission(bot, hidden=True)
async def id(ctx, *args):
    """Send the user a message with each id of the users he specified
    """
    if len(args) == 0:
        await bot.say('No such user(s).')
    for username in args:
        for user in ctx.message.server.members:
            if user.name == username:
                await bot.send_message(content=f'{user.name} : {user.id}', destination=ctx.message.author)


class BadResponseError(Exception):
    """Exception class that gets raised whenever a user response doesn't fit the conditions

    Attributes:
        value (str): Holds the error message for the exception
    """
    def __init__(self, value):
        """Constructor for the BadResponseError class
        
        Arguments:
            value {str} -- Error message
        """

        self.value = value
    def __str__(self):
        """
        Function to return string representation of the exception

        Returns:
            str: A string to represent the exception value
        """
        return repr(self.value)
