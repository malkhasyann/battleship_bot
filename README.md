# TELEGRAM Battleship Game Bot

Play Battleship game with your friends via Telegram Bot.

***

1. Register a bot and save the bot token in ``.env`` file like: <br>``BOT_TOKEN = 0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA``
2. Create a virtual environment and install the requirements(py 3.10+):<br>
``python3 -m venv venv``<br>
``source venv/bin/activate``<br>
``pip3 install -r requirements.txt``
3. Start the bot: ``python3 bot.py`` 
4. ``/new_game`` creates a new game session and generates a key<br>for connecting to the game session (e.g. ``xBpkMfHA``).
5. ``/connect`` connects to a game session with the given key(e.g. ``/connect xBpkMfHA``).
