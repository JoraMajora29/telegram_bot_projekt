import aiohttp
from bs4 import BeautifulSoup


async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_boss_depending_on_game_mode(boss_game_mode):
    url = 'https://terraria.wiki.gg/wiki/Bosses'
    html_code = await fetch_html(url)
    soup = BeautifulSoup(html_code, 'html.parser')

    articles = soup.find('div', {'class': 'toc'})
    if articles:
        bosses = articles.find_all_next('li')
        for boss in bosses:
            if boss_game_mode in boss.get_text():
                boss_info = boss.get_text().split('\n')
                boss_info = [' '.join(info.split()[1:]) for info in boss_info if 'bosses' not in info and info]
                return boss_info


async def get_boss_information(boss_name):
    url = f'https://terraria.wiki.gg/wiki/{boss_name}'
    html_code = await fetch_html(url)
    soup = BeautifulSoup(html_code, 'html.parser')

    articles = soup.find_all("div", {"class": "infobox npc modesbox c-normal"})[0]
    item_data = {
        'name': boss_name,
        'img': f'https://terraria.wiki.gg{articles.img["src"]}'
    }

    for row in articles.find_all('tr'):
        header = row.find('th').text.strip()
        value = row.find('td').text.strip()
        if 'https://' not in value and header:
            item_data[header] = value

    return item_data
