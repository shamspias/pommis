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

        python -m music

-------------------------------




Thanks to `py-music-bot`
https://github.com/joek13/py-music-bot
