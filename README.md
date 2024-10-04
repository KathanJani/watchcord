
# WatchCord

**WatchCord** is a Discord bot project **under development**, designed to track product prices through web scraping and platform-specific/third-party APIs. Users can set target prices and receive automated pings by username or role when deals are found. Key features include real-time access to product details, scheduled tracking, search and filter commands, data logging for bot enhancement, automation scripts, and a GUI-based admin panel for ease of use.


## Screenshots

<!-- ![App Screenshot](./Screenshots/ss.jpg) -->
<p float="left" align="middle">
  <img align="top" src="./Screenshots/SS1.png" width="400" alt="Landing Page"  />
  <img align="top" src="./Screenshots/SS2.png" width="400" alt="Home Page"  />
</p>
<img width="10" />
<p float="left" align="middle">
  <img align="top" src="./Screenshots/SS3.png" width="400" alt="Login Page"  />
  <img align="top" src="./Screenshots/SS4.png" width="400" alt="Help Page"  />
</p>


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`APP_ID`

`DISCORD_TOKEN`

`PUBLIC_KEY`


## Run Locally

Clone the project

```bash
git clone https://github.com/KathanJani/watchcord.git
```

Go to the project directory

```bash
cd watchcord
```

Create & activate a virtual environment

```bash
pip install venv

python -m venv .venv
  
.venv\Scripts\activate.bat
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start the bot by running the script

```bash
bot.py
```


## Tech Stack

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="30" alt="python logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" height="30" alt="fastapi logo"  />
  <img width="12" />
  <img src="https://cdn3.emoji.gg/emojis/9355-discordpy.png" height="30" alt="discord.py logo"  />
  <img width="12" />
  <img src="https://cdn2.hubspot.net/hubfs/4367560/Imported_Blog_Media/scrapy.png" height="30" alt="scrapy logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" height="30" alt="pandas logo"  />
  <img width="12" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Celery_logo.png" height="30" alt="celery logo"  />
  <img width="12" />
  <img src="https://cdn.simpleicons.org/selenium/43B02A" height="30" alt="selenium logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg" height="30" alt="mongodb logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg" height="30" alt="redis logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" height="30" alt="html5 logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" height="30" alt="css3 logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-original-wordmark.svg" height="30" alt="tailwindcss logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" height="30" alt="javascript logo"  />
</div>

###