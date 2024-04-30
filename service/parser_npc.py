import aiohttp
from bs4 import BeautifulSoup

nps_types = {
    'Town NPCs': ['Pre-Hardmode', 'Hardmode'],
    'Town pets': ['Town pets'],
    'Town Slimes': ['Town Slimes']
}


async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_npc_depending_on_type(npc_type):
    url = 'https://terraria.wiki.gg/wiki/NPCs'
    html_code = await fetch_html(url)
    soup = BeautifulSoup(html_code, 'html.parser')

    articles = soup.find(string=npc_type).find_next('tbody').find_all("td", {"class": "il1c"})

    return articles


async def get_npc_information(npc_name):
    url = f'https://terraria.wiki.gg/wiki/{npc_name}'
    html_code = await fetch_html(url)
    soup = BeautifulSoup(html_code, 'html.parser')

    articles = soup.find_all("div", {"class": "infobox npc modesbox c-normal"})[0]

    item_data = {
        'name': npc_name,
        'img': f'https://terraria.wiki.gg{articles.img["src"]}'
    }

    for row in articles.find_all('tr'):
        header = row.find('th').text.strip()
        value = row.find('td').text.strip()
        if 'https://' not in value and header:
            item_data[header] = value

    return item_data
