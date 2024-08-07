import asyncio
import logging

import deposit

if __name__ == "__main__":
    # Logging config
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] [%(name)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    import sys

    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(
        deposit.deposit_task(
            'UQBzseE936CmvgfrOTITCF6tzFZYym42fC4pO71WSgyMNPl3',
            'TonCenter_API_key'
        )
    )
