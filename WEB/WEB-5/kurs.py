import argparse
import aiohttp
import asyncio
import platform
import logging
from datetime import datetime, timedelta

options = argparse.ArgumentParser(description="Number of days")
options.add_argument("day", help="the number of days for which the exchange rate is required", default=1, type=int)

args = vars(options.parse_args())
number_days = args['day']
print(number_days)

async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    logging.info(f"Error status: {resp.status} for {url}")
        except aiohttp.ClientConnectorError as err:
            logging.info(f'Connection error: {url}', str(err))


async def main():
    number = 0
    exchange = []
    text = {}
    while number_days != number:
        now = datetime.today().date()
        date = now - timedelta(days=number)
        try:
            result = await request(f"https://api.privatbank.ua/p24api/exchange_rates?date={date.strftime('%d.%m.%Y')}")
            for item in result['exchangeRate']:
                if item['currency'] in ('USD', 'EUR'):
                    text[item['currency']] = {'sale': item['saleRate'], 'purchase': item['purchaseRate']}
            exchange.append({result['date']: text})
        except aiohttp.ClientConnectorError as e:
            logging.error(f"Connection error {url}: {e}")
        number +=1
    return exchange


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)
