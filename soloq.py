import configparser
import shelve

import requests

config = configparser.ConfigParser()
if not config.read('config.ini'):
    print("Could not load config.ini file")
    exit(1)

try:
    config_section = config['SOLOQ']
except KeyError as e:
    print("Config file must contain a [SOLOQ] section")
    exit(1)

try:
    RIOT_API_KEY = config_section['RIOT_API_KEY']
    WEBHOOK_URL = config_section['WEBHOOK_URL']
    USERNAME = config_section['USERNAME']
    USER_REGION = config_section['USER_REGION']
    WIDE_REGION = config_section['WIDE_REGION']
    DATA_FILE = config_section['DATA_FILE']
except KeyError as e:
    print(e, "must be specified in config [SOLOQ] section")
    exit(1)


def get_summoner_dto():
    summoner_by_name_url = f"https://{USER_REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{USERNAME}"
    response = requests.get(summoner_by_name_url, params={'api_key': RIOT_API_KEY})
    summoner_dto = response.json()
    if not response.ok:
        raise Exception("Could not get summoner", summoner_dto)
    return summoner_dto


def notify_game_result(summoner_dto, data):
    puuid = summoner_dto['puuid']
    last_match = data['last_match']

    matches_by_puuid_url = f"https://{WIDE_REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    response = requests.get(matches_by_puuid_url, params={'api_key': RIOT_API_KEY, 'count': 1})
    matches_dto = response.json()
    if not response.ok:
        raise Exception("Could not get match history", matches_dto)
    if not matches_dto:
        print("Match history is empty")
        return

    match = matches_dto[0]
    if match == last_match:
        return

    match_by_id_url = f"https://{WIDE_REGION}.api.riotgames.com/lol/match/v5/matches/{match}"
    response = requests.get(match_by_id_url, params={'api_key': RIOT_API_KEY})
    match_dto = response.json()
    if not response.ok:
        raise Exception("Could not get match details", match_dto)

    rank_message = ""
    queue_id = match_dto['info']['queueId']
    if queue_id == 420 or queue_id == 440:
        queue_str = "SOLO/DUO" if queue_id == 420 else "FLEX"
        queue_type = 'RANKED_SOLO_5x5' if queue_id == 420 else 'RANKED_FLEX_SR'
        league_entries_url = f"https://{USER_REGION}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_dto['id']}"
        response = requests.get(league_entries_url, params={'api_key': RIOT_API_KEY})
        league_entries = response.json()
        if not response.ok:
            raise Exception("Could not get league entries", league_entries)

        for entry in league_entries:
            if entry['queueType'] == queue_type:
                rank_str = f"{entry['tier']} {entry['rank']} {entry['leaguePoints']}LP"
                wins = entry['wins']
                losses = entry['losses']
                total = 100 * wins / (wins + losses)
                wr_str = f"{wins}W {losses}L {total:.2f}% WR"
                rank_message = f"\n\n{queue_str}\n{rank_str}\n{wr_str}"

    participants = match_dto['info']['participants']
    numeric_id = match.split("_")[1]

    if match_dto['info']['gameDuration'] <= 5 * 60 * 1000:
        # game lasted less than 5 minutes - likely a remake
        response = requests.post(WEBHOOK_URL, json={'embeds': [
            {
                "title": USERNAME,
                "description": f"remake...",
                "color": 8421504,
                "footer": {
                    "text": f"ID: {numeric_id}"
                },
            },
        ]})
        if not response.ok:
            raise Exception("Could not post to Discord")
    else:
        for p in participants:
            if p['puuid'] == puuid:
                emoji = ":trophy:" if p['win'] else ":cold_face:"
                result = "won" if p['win'] else "lost"
                color = 6591981 if p['win'] else 16737095
                print(f"game {result} (ID: {numeric_id})")
                response = requests.post(WEBHOOK_URL, json={'embeds': [
                    {
                        "title": USERNAME,
                        "description": f"game {result} {emoji}{rank_message}",
                        "color": color,
                        "footer": {
                            "text": f"ID: {numeric_id}"
                        },
                    },
                ]})
                if not response.ok:
                    raise Exception("Could not post to Discord")
                break

    data['last_match'] = str(matches_dto[0])


def notify_in_game(summoner_dto, data):
    summoner_eid = summoner_dto['id']

    active_games_url = f"https://{USER_REGION}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_eid}"
    response = requests.get(active_games_url, params={'api_key': RIOT_API_KEY})
    current_game_info = response.json()
    if not response.status_code == 404 and not response.ok:
        raise Exception("Could not get active game", current_game_info)

    if 'status' in current_game_info:
        print("Currently not in game")
        return

    current_game = str(current_game_info['gameId'])
    previous_game = data['in_game']

    if previous_game == current_game:
        print(f"In the same game (ID: {current_game})")
        return

    message = f"{USERNAME} started a new game (ID: {current_game})"
    print(message)
    response = requests.post(WEBHOOK_URL, json={'embeds': [
        {
            "title": USERNAME,
            "description": f"started a new game :sparkles:",
            "color": 16738740,
            "footer": {
                "text": f"ID: {current_game}"
            },
        },
    ]})
    if not response.ok:
        raise Exception("Could not post to discord")

    data['in_game'] = str(current_game)


if __name__ == '__main__':
    with shelve.open(DATA_FILE) as data:
        for key in ['in_game', 'last_match', 'error']:
            if key not in data:
                data[key] = ''

        try:
            summoner = get_summoner_dto()
            notify_game_result(summoner, data)
            notify_in_game(summoner, data)
            data['error'] = False
            print("Ran successfully!")
        except Exception as e:
            if not data['error']:
                requests.post(WEBHOOK_URL, json={'content': str(e)})
            data['error'] = True
            raise e
