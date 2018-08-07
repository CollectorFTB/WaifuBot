import asyncio
import time
from importlib import reload

import waifubot


# get the bot token 
def get_token(fp):
    with open(fp, 'r') as file:
        token = file.read()
    return token

# loop that handles reloading/shutting down the bot
def run_client(bot, *args, **kwargs):
    loop = asyncio.get_event_loop()
    line = 'y'
    while line == 'y':
        try: 
            loop.run_until_complete(waifubot.bot.start(*args, **kwargs))
            reload(waifubot)
        except Exception as e:
            print(e)
            print('bot restart')
            time.sleep(1)
        with open('rerun.txt') as file:
            line = file.read()

def main():
    run_client(waifubot.bot, get_token('token.txt'))

if __name__ == '__main__':
    main()
