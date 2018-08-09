import asyncio
import time
from importlib import reload

import waifubot


def get_token(fp):
    """Gets the bot token from the token file
    
    Arguments:
        fp {str} -- file path to the token
    
    Returns:
        [str] -- bot token
    """

    with open(fp, 'r') as file:
        return file.read()


def run_client(*args, **kwargs):
    """loop that handles reloading/shutting down the bot
    """

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
        with open('data/rerun.txt') as file:
            line = file.read()

def main():
    run_client(get_token('data/token.txt'))

if __name__ == '__main__':
    main()
