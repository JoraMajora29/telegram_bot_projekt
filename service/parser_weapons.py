import aiohttp
from bs4 import BeautifulSoup

weapons_types_and_subtypes = {
    'Melee weapons': {
        'Swords': ['Pre-Hardmode Swords', 'Hardmode Swords'],
        'Yoyos': ['Pre-Hardmode Yoyos', 'Hardmode Yoyos'],
        'Spears': ['Pre-Hardmode Spears', 'Hardmode Spears'],
        'Boomerangs': ['Pre-Hardmode Boomerangs', 'Hardmode Boomerangs'],
        'Flails': ['Pre-Hardmode Flails', 'Hardmode Flails'],
        'Other': ['Pre-Hardmode Other', 'Hardmode Other'],
    },
    'Ranged weapons': {
        'Bows and Repeaters': ['Pre-Hardmode Bows', 'Hardmode Bows and Repeaters'],
        'Guns': ['Pre-Hardmode Guns', 'Hardmode Guns'],
        'Launchers': ['Launchers'],
        'Consumables': ['Consumables'],
        'Grenades': ['Grenades'],
        'Others': ['Pre-Hardmode Others', 'Hardmode Others']
    },
    'Magic weapons': {
        'Wands': ['Pre-Hardmode Wands', 'Hardmode Wands'],
        'Magic guns': ['Pre-Hardmode Magic Guns', 'Hardmode Magic Guns'],
        'Spell books': ['Pre-Hardmode Spell books', 'Hardmode Spell books'],
        'Others': ['Pre-Hardmode Other', 'Hardmode Other']
    },
    'Summoning weapons': {
        'Minion-summoning weapons': ['Pre-Hardmode Minion-Summoning weapons', 'Hardmode Minion-Summoning weapons'],
        'Sentry-summoning weapons': ['Sentry-summoning weapons', 'Hardmode Sentry-Summoning weapons'],
        'Whips': ['Pre-Hardmode Whips', 'Hardmode Whips']
    },
    'Other weapons': {
        'Placeable weapons': ['Pre-Hardmode Placeable Weapons', 'Hardmode Placeable Weapons'],
        'Explosives': ['Explosives'],
        'Other weapons': ['Other weapons']
    }
}


async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_weapons_depending_on_type(weapon_subtype_mode):
    url = 'https://terraria.wiki.gg/wiki/Weapons'
    html_code = await fetch_html(url)
    soup = BeautifulSoup(html_code, 'html.parser')
    weapon_subtype = weapon_subtype_mode[0]
    weapon_mode = weapon_subtype_mode[1]
    if weapon_subtype == 'Flails':
        articles = soup.find(string=weapon_mode).find_next('ul')
        res_1 = articles.select('li')
        res_2 = articles.find_next('ul').select('li')
        res_1.extend(res_2)
        return res_1
    if weapon_subtype == weapon_mode:
        articles = soup.find('span', class_='mw-headline', string=weapon_mode).find_next('ul').select('li')
        return articles
    articles = soup.find(string=weapon_mode).find_next('div').select('li')
    return articles


async def get_weapon_information(weapon_name):
    url = f'https://terraria.wiki.gg/wiki/{weapon_name}'
    html_code = await fetch_html(url)
    soup = BeautifulSoup(html_code, 'html.parser')

    articles = soup.find_all("div", {"class": "infobox item"})[0]

    item_data = {
        'name': weapon_name,
        'img': f'https://terraria.wiki.gg{articles.img["src"]}'
    }

    for row in articles.find_all('tr'):
        header = row.find('th').text.strip()
        value = row.find('td').text.strip()
        if 'https://' not in value and header:
            item_data[header] = value

    return item_data
