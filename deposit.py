import asyncio
import logging

import aiohttp

API_BASE = 'https://toncenter.com/'


async def create_get(endpoint: str, data: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(API_BASE + endpoint, params=data) as resp:
            return await resp.json()


# Task for checking wallet for new transactions and process deposits
async def deposit_task(address: str, api_key: str, filename: str = 'deposit.txt') -> None:
    # Check api key
    if api_key == '':
        logging.error('TonCenter API key is missing, deposit task is quitting!')
        return

    # Log if task was started
    logging.info('Deposit task was started successfully')

    try:
        # Try to load last saved logical time from file
        with open(filename, 'r') as f:
            lt_cache = int(f.read())
    except FileNotFoundError:
        # If file not found, set logical time to 0
        lt_cache = 0

    # Pre-defined request params
    data = {
        'address': address,
        'limit': 20,
        'archival': 'true',
        'api_key': api_key
    }

    while True:
        # Delay between checks
        await asyncio.sleep(3)

        # API call to Toncenter that returns last transactions of wallet
        resp = await create_get('api/v2/getTransactions', data)

        # If call was not successful, try again
        if not resp['ok']:
            continue

        # Iterating over transactions
        for tx in resp['result']:
            # Logical time of transaction
            lt = int(tx['transaction_id']['lt'])

            # Skip transaction, if this logical time is lower than cached
            if lt <= lt_cache:
                continue

            # Transaction data
            msg = tx['in_msg']['message']
            value = int(tx['in_msg']['value'])
            source = tx['in_msg']['source']

            # Log deposit data
            logging.info(f'Deposit income: {round(value / 1_000_000_000, 3)} TON, addr: {source}')

            # Call deposit processing function
            await __deposit(msg, source, value)

            # Update and write cached logical time
            lt_cache = lt
            with open(filename, 'w') as f:
                f.write(str(lt_cache))


async def __deposit(message: str, source: str, amount: int) -> None:
    # some logic can be processed here
    pass
