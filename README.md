# Unlimited Filter Bot


<p align="center">
  <a href="https://www.python.org">
    <img src="http://ForTheBadge.com/images/badges/made-with-python.svg">

  </a>
</p>
<p align="center">
  <a href="https://github.com/TroJanzHEX/Unlimited-Filter-Bot/stargazers">
    <img src="https://img.shields.io/github/stars/TroJanzHEX/Unlimited-Filter-Bot?style=social">

  </a>
  
  <a href="https://github.com/TroJanzHEX/Unlimited-Filter-Bot/fork">
    <img src="https://img.shields.io/github/forks/TroJanzHEX/Unlimited-Filter-Bot?label=Fork&style=social">

  </a>  
</p>

[![TroJanz](https://img.shields.io/badge/TroJanzHEX-Channel-orange?style=for-the-badge&logo=telegram)](https://telegram.dog/TroJanzHEX)  
ㅤㅤㅤㅤㅤㅤㅤ  
[![TroJanz](https://img.shields.io/badge/TroJanzHEX-Support-red?style=flat&logo=telegram)](https://telegram.dog/TroJanzSupport)  [![TroJanz](https://img.shields.io/badge/TroJanzHEX-Website-red?style=flat&logo=CodersRank)](https://TroJanzHEX.me)  
ㅤㅤㅤㅤㅤㅤㅤ  
[![MIT license](https://img.shields.io/badge/License-MIT-blue?style=flat)](https://github.com/TroJanzHEX/Unlimited-Filter-Bot/blob/main/LICENSE)  [![Open Source](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/TroJanzHEX/Unlimited-Filter-Bot)


## An advanced Filter Bot with nearly unlimitted filters!


### Features
* Nearly unlimited filters
* Supports all type of filters(Including Alert Button Filter).
* Can save button filters directly (Rose Bot Feature)
* Supports multiple PM connections
* And all other features of a Filter Bot :D


#### Deploy the bot and start adding your filters :)


## How to use the bot
* Add bot to your group with admin rights.

* Add your filters :)


## Bot Commands

(You need to be an admin or Auth User in order to use these commands)

> Filter Commands
* `/add <filtername> <filtercontent>`  -  To add your filter. You can also reply to your content with /add command.

* `/del <filtername>`  -  Delete your filter.

* `/delall`  -  Delete all filters from group. (Group Owner Only!)

* `/viewfilters`  -  List all filters in chat.

> Connection Commands
* `/connect groupid`  -  Connects your group to PM. You can also simply use, `/connect` in groups.

* `/connections`  -  Manage your connections. (only in PM)

> Extras
* `/status`  -  Shows current status of your bot (Auth User Only)

* `/id`  -  Shows ID information

* `/info <userid>`  -  Shows User Information. Also use `/info` as reply to some message for their details!


## You can check the video tutorial on how to deploy

[Click here to see tutorial video](https://youtu.be/hkmc3e7U7R4)

Thanks to [InfotelGroup](https://telegram.dog/InFoTel_Group) and [Erich Daniken](https://telegram.dog/ErichDaniken) for the video


## Any bugs or errors or suggestions, report at [TroJanzSupport](https://telegram.dog/TroJanzSupport)


## Installation

### Deploy to Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/TroJanzHEX/Unlimited-Filter-Bot)

### Deploy in your vps
```sh
git clone https://github.com/TroJanzHEX/Unlimited-Filter-Bot
cd Unlimited-Filter-Bot
pip3 install -r requirements.txt
# <Create config.py appropriately>
python3 bot.py
```


## Configs

* TG_BOT_TOKEN  - Get bot token from @BotFather

* API_ID        - From my.telegram.org (or @UseTGXBot)

* API_HASH      - From my.telegram.org (or @UseTGXBot)

* AUTH_USERS  - ID of users that can use the bot commands. Get from [MissRose Bot](https://telegram.dog/MissRose_bot) by using /id command

* DATABASE_URI  - Mongo Database URL from https://cloud.mongodb.com/

* DATABASE_NAME  - Your database name from mongoDB. Default will be 'Cluster0'

* SAVE_USER  -  Give yes or no . Usefull for getting userinfo and total user counts. May reduce filter capacity :( .

* HEROKU_API_KEY  -  To check dyno status. Go to https://dashboard.heroku.com/account , scroll down and press Reveal API


### Optional - To set alternate Bot Commmands!
( *Add required field as heroku var and give desired command as value. You can edit it in sample_config.py also!*)

* ADD_FILTER_CMD  -  default will be 'add'

* DELETE_FILTER_CMD  -  default will be 'del'

* DELETE_ALL_CMD  -  default will be 'delall'

* CONNECT_COMMAND  -  default will be 'connect'

* DISCONNECT_COMMAND  -  default will be 'disconnect'

EG;  
![Vars Eg](https://telegra.ph/file/1f956f3491f2f20a9c1ec.jpg)

## Credits

<p align="left">
  <a href="https://github.com/pyrogram/pyrogram">
    <img alt="Pyrogram" src ="https://i.imgur.com/BOgY9ai.png" width="104.75" height="32"/>
  </a>
</p>

<p align="left">
  <a href="https://docs.mongodb.com">
    <img alt="MongoDB" src ="https://img.shields.io/badge/MongoDB-%234ea94b.svg?&style=for-the-badge&logo=mongodb&logoColor=white"/>
  </a>
</p>
