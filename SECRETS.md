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

### In Between:
1. Create a file called `secrets.json` in `bot_config`. (NOTE: This file should not be gitignored, so you should not post this version to github if you use this method.)
2. You will need to put your secrets like this. **Pro Tip** (Try to keep the variable name the same, because otherwise it'll be a bunch of unwanted hassle.)
    - Find out how to get a MongoDB Connection str [here](https://docs.mongodb.com/manual/reference/connection-string/) or [here](https://www.youtube.com/watch?v=R2VReXO_1j0). For the second link, watch from 00:28-2:09 and 7:50-8:02. 

{

    "token": "YourActualToken(InStr)",
    "mongo": "YourMongoDBConnectionStr(RememberToReplaceThe<password>)",
    "news api": "YourNewsApiKey(InStr)",
    "api_key": "YourActualApiKey(InStr)"

}

NOTE: You probably shouldn't put this one on Github, just for safety reasons, unless you are an absolute god at using  `.gitignore` files. :)