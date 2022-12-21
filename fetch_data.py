import aiohttp
import asyncio
import os
import time
import re
import json
import string
import time
import urllib
import queue
import threading
import concurrent.futures
import urllib.parse
import urllib.request
from urllib.request import urlopen
from datetime import datetime
from collections import Counter
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from logger import Logger
from tqdm.auto import tqdm

link_file = 'intermediates/links.json'
output_file = 'intermediates/data.json'
links = []
output = {}


def write_output():
    global output
    with open(output_file, 'w+') as convert_file:
        convert_file.write(json.dumps(output))
    Logger.write_info("Data written to the JSON file")


def get_links():
    global links
    global link_file
    try:
        with open(link_file, "r") as file:
            links = json.load(file)
        Logger.write_info("Links read from file.")
    except Exception as e:
        Logger.write_error(e)


async def get_page(session, url):
    global output
    if not links:
        Logger.write_warning("Links not read!")
    try:
        async with session.get(url) as r:
            if r.status == 200:
                text = await r.text()
                text_content = []
                soup = BeautifulSoup(text, 'html.parser')
                content = soup.findAll('p')
                article = ''
                for i in content:
                    article = article + ' ' + i.text
                text_content.append(article)
                Logger.write_debug("URL read -" + url)
                output[url] = text_content
            elif r.status == 400:
                Logger.write_error("Timeout - " + url)
            else:
                Logger.write_info(await r.status)
    except:
        Logger.write_error("Error while reading webpage")
        (aiohttp.ClientError, asyncio.TimeoutError)


async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def get_all_links(urls):
    timeout = aiohttp.ClientTimeout(sock_read=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        data = await get_all(session, urls)
        return data


def fetch_data():
    global output
    get_links()
    start_time = time.time()
    urls = links
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    results = asyncio.run(get_all_links(urls))
    Logger.write_info("Number of pages read - " + str(len(results)))
    Logger.write_info("Time taken to read all the pages - " +
                      str(time.time() - start_time) + " secs")
    write_output()


if __name__ == "__main__":
    fetch_data()
