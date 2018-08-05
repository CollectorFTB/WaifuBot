import asyncio
import time
from importlib import reload

import WaifuBot


def get_token(fp):
    with open(fp, 'r') as file:
        token = file.read()
    return token

def run_client(bot, *args, **kwargs):
    loop = asyncio.get_event_loop()
    while True:
        try: 
            loop.run_until_complete(WaifuBot.bot.start(*args, **kwargs))
            print('here')
            WaifuBot.bot.close()
            WaifuBot.create_bot()
            print('here')
            reload(WaifuBot)
        except Exception as e:
            print(e)
            print('bot restart')
            time.sleep(1)

def main():
    run_client(WaifuBot.bot, get_token('token.txt'))
    # WaifuBot.bot.run(get_token('token.txt'))
    """
    WaifuBot.bot.run(get_token('token.txt'))
    
        if line == 'y':
            reload(WaifuBot)
            WaifuBot.create_bot()
            WaifuBot.bot.run(get_token('token.txt'))
    """
if __name__ == '__main__':
    main()
