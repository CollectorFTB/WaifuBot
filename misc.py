import asyncio


def fizzbuzz(number, divisors):
    output = ''
    for divisor in divisors:
        output = output+divisors[divisor] if number%divisor==0 else output
    return output if output != '' else number

async def get_messages(bot, count):
    messages = bot.logs_from(ctx.message.channel, limit=amount_to_prune+1)
    messages = [message async for message in messages]
    return messages
