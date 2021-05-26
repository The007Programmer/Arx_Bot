# Cafe_Bot

![Cafe Bot-logos](https://user-images.githubusercontent.com/83626443/118020079-91aed400-b30e-11eb-83ed-f88fa81dc51c.png)

## Motivation

Our motivation to make this bot came from a small build-up of frustration at other discord bots. They only did specific things, and you had to add multiple of them to make a good server with good bots. A friend and I both shared this belief. We decided that we should make our own discord bot, to cure other people of this frustration. So, that's what we've done! This is a combination of many attributes of many popular bots. Now, half your server-space doesn't get taken up by bots! You just have to add 1!

## Features

This is an all-around Discord Bot, with many features, such as:
* AI-Chat System¹
* Currency System¹
* Error Handler³
* Giveaway System³
* Custom Help Command (Not the ugly orginal bot-rendered one.)³
* A Calculator³
* Moderation Commands³
* A Polling System³
* Eval & Stat Commands²
* A Leveling System³
* and much more!

[Invite The Bot to Your Server!](https://discord.com/oauth2/authorize?client_id=832409595791409242&permissions=8&scope=bot)

Inviting it would mean a ton to me, the main developer of this bot, to see it in a public server, so please add it! 😁

## Prerequisites

Mainly a bunch of pip installs, for the project to work.

Python 3.6+

A working Text Editor or IDE.

[The Pip Installs](PIP_INSTALLS.md)

## Usage

Many of you that have come across this page, probably want to use this code for yourself. ⚡ NEWS FLASH ⚡, many people that just take things from a person's github and use it for themselves and they DON'T GIVE CREDIT! If you want to us it properly, then you have to give credit to this github page, and all the contributors.

Well, anyway, to use it, there will be certain things you will have to replace in your code, as well as required prerequisites (mentioned above), in order for the code to work properly.

First things first: You will need to create a bot from your discord developer portal:
![bot-token1](https://user-images.githubusercontent.com/83626443/118029530-1bfc3580-b319-11eb-8452-48cf12541420.gif)

Then, you need an API Key from [PGamerX](https://api-info.pgamerx.com/register.html). (Steps should be self explanatory.)

Now, after these steps, this step can go 2 ways from here.

### If you're using Replit:
1. You will need to go to the sidebar on your project to a section called Environment Variables, and add your Token and API_Key in the Key section, and the actual values in the Value section.
![environmentvars](https://user-images.githubusercontent.com/83626443/118030800-9da09300-b31a-11eb-9fd0-ef9a2eff14b2.gif)
2. Only then, will the certain parts of the code (in main.py and cogs/mod.py) will work correctly. Everything else will work.
3. I like using Replit, because it is easier in terms of hosting the bot 24/7.

### If you're using a Local Text Editor:
1. Make sure you have set the current language to Python 3.6+. 
2. If you know that the code you're making will never reach the public, then in main.py and cogs/mod.py, you will have to replace the `os.getenviron['API_Key']` and `os.getenviron['Token']`. All instances of `os.getenviron['API_Key']` will be replaced with your actual api key, in str format! All instances of `os.getenviron['Token']` will need to be replaced with your actual bot token, also in str format. This is important. Remember, your token and api key will not appear magically! You have to remember to do these steps.
3. But if you plan on publishing it to a Github (only do this if you know how to connect to a github repo from a local text editor, commit, push and pull), then you will **NOT** want to put the api_key and token as is (in str). You may get flagged by discord and they will stop your bot, and make you regernerate your token. As for your api_key, if other people see that, they can also use it! To prevent having your bot stopped or your api_key used, follow these steps. (If you don't get these steps, there is an example below.) 
   - First make a new file called `.env`. 
   - Then put the contents of the variables that you want to get rid of in there. 
   - Then add `*.env` into a new file called `.gitignore`. (Btw, in the example below, it only shows main.py, because I was lazy to create a new directory for an example.)
![vscode2](https://user-images.githubusercontent.com/83626443/118033835-1ead5980-b31e-11eb-829d-b1f14be94982.gif)

* And that should be it for prerequisites and installations.

## Current Build Status
- @MilkshakeTheCoder - (Possible Dashboard???)
- @Andrewthederp - (Currency System Upgrades, Overall better feel.)

## Main Technologies Used
* Python 3.8+
* Discord
* Discord.py
* Github
* Replit
* UpTimeRobot

## After that...
* You should be free to run the code and have a fully functioning bot! If there are problems with our explanation and/code, please be sure to let us know in the discussion below! Also, be sure to join our server!

[Join our Discord Server!](https://discord.gg/CtNTUX4znA)

## Credits and Acknowledgments
Code With Swastik¹ ⠀⍿ ⠀[Github](https://github.com/CodeWithSwastik) · [Youtube](https://www.youtube.com/c/CodeWithSwastik/featured)

MenuDocs² ⠀⍿ ⠀[Github](https://github.com/MenuDocs) · [Youtube](https://www.youtube.com/channel/UCpGGFqJP9vYvzFudqnQ-6IA)

## Fellow Coders and Contributors³

@MilkshakeTheCoder ⠀⍿ ⠀[Github](https://github.com/MilkshakeTheCoder)

@Andreawthederp ⠀⍿ ⠀[Github](https://github.com/andrewthederp)

Also check out our [Code of Conduct](https://github.com/MilkshakeTheCoder/Cafe_Bot/blob/main/CODE_OF_CONDUCT.md).