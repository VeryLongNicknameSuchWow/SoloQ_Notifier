# Solo Queue Notifier

This script is a simple tool to track League of Legends games of a specific player and send notifications
about their games to a Discord channel. It utilizes Riot Games API to fetch game data and uses webhooks to send messages
to Discord.

### Features

- Sends a Discord message whenever the player starts a new game
- Sends a Discord message whenever the player finishes a game

### Dependencies

This script was tested on Python 3.10 and requires the `requests` library. You can install it with pip:

```
pip3 install requests
```

### Configuration

Before running the script, a `config.ini` file needs to be created in the same directory as the script. The file should
contain a section `SOLOQ` with the following keys:

- `RIOT_API_KEY`: Your Riot Games API Key.
- `WEBHOOK_URL`: The Discord webhook URL you want to use to send notifications.
- `USERNAME`: The username of the player you want to track.
- `USER_REGION`: The specific region the player plays in, e.g., `na1` for North America.
- `WIDE_REGION`: The broad region the player is in, e.g., `americas` for North America.
- `DATA_FILE`: The name of the data file to store game and error information. This file should be unique for each
  username (when using multiple config files).

You can get your Riot Games API key [here](https://developer.riotgames.com/). User and wide regions should
match [Riot Games API routing values](https://developer.riotgames.com/docs/lol#routing-values). Information on how to
generate a Discord channel webhook is provided
in [this article](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

### Running the script

This script can be run with the following command:

```
python3 soloq.py
```

A path to a configuration file can optionally be passed as a command line argument:

```
python3 soloq.py other_config.ini
```

You can setup a [cron](https://en.wikipedia.org/wiki/Cron) job to run the script automatically every few minutes. To do
that run `crontab -e` to open the cron
table editor and add a new line at the bottom:

```
*/1 * * * * cd /path-to-your-script && python3 soloq.py
```

This will run the script once every minute.

### Note

This script makes between 3 and 7 requests to Riot API each time it's run.
Riot Games API has strict rate limits. If your application exceeds those limits, your IP may be temporarily blacklisted.
Always ensure you are within the API usage limits to prevent this from happening.

### Disclaimer

This script is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially
involved in producing or managing Riot Games properties. Riot Games, and all associated properties, are trademarks or
registered trademarks of Riot Games, Inc.

This script uses the Discord API but is not endorsed or certified by Discord. Discord, the Discord logo, and any
associated marks and logos are trademarks or registered trademarks of Discord, Inc., in the U.S. and other countries.