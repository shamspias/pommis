# Pommis A Music bot using Python and discord.py

# Install

## Create a Virtual Environment

Windows First, make sure you have python installed on your pcopen cmd or PowerShell
	
	python -m venv  yourvenv
		
Linux and others Open terminal
	
        sudo apt-get install python3-pip
        pip3 install virtualenv
	
After installing virtualenv just type

        virtualenv yourvenv

## Activate Virtual Environment.

Windows
	
	yourvenv/Scripts/activate
		
If show any error then open Powershell in admin
then type

        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
	and press "A" then Enter.

Linux

        . yourvenv/bin/activate

## Install the requirement .txt to virtualenv

Windows
	
	pip install -r requirement .txt

Linux
	
        pip3 install -r requirement .txt

## Set config.tomal
Normally it will auto set config.toml file after 1st running 
but better to create a config.toml file then put info for token and prefix 

Example:

        "token"="Your Discord Token" # the bot's token
        "prefix"="." # prefix used to denote commands
        
        [music]
        # Options for the music commands
        "max_volume"=250 # Max audio volume. Set to -1 for unlimited.
        "vote_skip"=true # whether vote-skipping is enabled
        "vote_skip_ratio"=0.5 # the minimum ratio of votes needed to skip a song
        [tips]
        "github_url"="https://github.com/shamspias/pommis"
        

## Running the bot

use 

        python music/__main__.py

-------------------------------
# Comments

use `help` to get more info

`join` or `j` to join in same voice channel

`play` or `p` then YouTube link or song name to 
play or add to queue

`skip` or `s` to skip

`stop` to stop

`leave` or `dc` to disconnect from channel

`clear` `number` to delete text and chatting from channel(Admin only)

`queue ` or `q` to show list of music in queue

`clear_queue` or `cq` to clear current queue

`resume`  `pus` `pouse`  `pause` to Pause the song and resume the song,

`volume` or `vol` or `v` to change volume

`jump_queue` or `jq`  or `change_queue` to change/shift queue song positions 
example: want to bring song number 10 to number 1 in queue just use .jump_queue 10 1

-------------------
# Deploy Using PM2

## Ubuntu server

Do the virtualenv process
then

Install Nodejs and npm then install pm2

        sudo apt install nodejs
        sudo apt install npm
        sudo npm install -g pm2
Then run the comment

        pm2 start music/__main__.py --name=pommis --interpreter=your_env_name/bin/python3

can see logs just use
        
        pm2 logs pommis(apps name)

---------------------------------



Thanks to `py-music-bot`
https://github.com/joek13/py-music-bot
