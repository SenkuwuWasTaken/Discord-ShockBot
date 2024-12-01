WARNING: this is currently untested on the PiShock side, as I don't have mine yet.

1. Install requirements.txt and run the python file <br />
This can be done manually, or with `install requirements.bat` <br />
2. Settings.json template will appear for you to fill out, explanations below.
3. Then run `run bot.bat` or run `ShockBot.py manually` <br />


```
"username": ""                
--this is your PiShock account username

"api_key": ""                 
--this is you PiShock API key

"sharecodes": [""]            
--PiShock sharecodes for your shockers. 
for multiple, format it as ["code1", "code2", "code3] etc

"bot_token": ""               
--Discord bot token

"shockIntensityScale": 100    
--All shocks and vibrations will be scaled with this number as the maximum intensity, 
this can be changed through discord commands, or manually (1-100)

"myUserID": 0                 
--Copy Paste your discord UserID here so only you can use certain commands.

"ShockBotAdmins": []          
--Same as above, but you can add many UserIDs to control certain commands. 
for multiple, format it as [123, 456, 789] etc

"bannedUserIDs": []           
--Manual banning of UserIDs from using this bot. same as above for multiple IDs
```
