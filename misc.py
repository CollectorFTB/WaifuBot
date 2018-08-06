import asyncio
import json


def load_config():
    with open('data/config.json', 'r') as file:
        data = json.load(file)
    config = data
    return config

def fizzbuzz(number, divisors):
    output = ''
    for divisor in divisors:
        output = output+divisors[divisor] if number%divisor==0 else output
    return output if output != '' else number

async def get_messages(bot, ctx, count):
    messages = bot.logs_from(ctx.message.channel, limit=count+1)
    messages = [message async for message in messages]
    return messages
