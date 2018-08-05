import asyncio
import time
from importlib import reload

import waifubot


def get_token(fp):
    with open(fp, 'r') as file:
        token = file.read()
    return token

def run_client(bot, *args, **kwargs):
    loop = asyncio.get_event_loop()
    while True:
        try: 
            loop.run_until_complete(waifubot.bot.start(*args, **kwargs))
            reload(waifubot)
        except Exception as e:
            print(e)
            print('bot restart')
            time.sleep(1)

def main():
    run_client(waifubot.bot, get_token('token.txt'))

if __name__ == '__main__':
    main()
