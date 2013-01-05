TazBot 2.0
==========

TazBot is a Q & A Bot written to serve the users in the official SliTaz IRC channel on freenode.
It's simple to use and it's answers database can be expanded on the fly using it's learning system.
TazBot has two commands, 'help' and 'topics', that tell the user how to use TazBot and which questions the bot able to answer. The bot can answer questions in the channel when questions include it's nickname as well as answer questions in private with a user.

This code is released under the Creative Commons Zero license, which places it in the Public Domain while obsolving me of any responsibility or liablity that may result from the use or misuse of this code. Basically put, you have the full right to do whatever you want with the code without any restrictions including selling it as your own. The only thing you cannot do is sue me if things go wrong. Read LICENSE for more information on this.


How do I use it?
----------------
Just edit tazbot.conf to what you want and type ./tazbot to connect.

`help` will display the basic usage of the bot:  
`Tazbot: help`

`topics` will bring up the topics the bot can answer questions about:  
`TazBot: topics`

Use the `!learn` or `!teach` commands with the trigger and responses seperated by a `|` to teach the bot responses. Spaces don't matter, but the length is limited to the standard IRC message line (around 500 characters). Multiple lined responses is also supported and will be each be shown on their own line. If there is more than the set amount of lines (set in the conf file), the responses will be forwarded to the user.
Triggers are searched by closest matches so single words or short triggers work better, but words can be searched within longer triggers:  
`!learn This is a trigger | And this is a response!`  
`!teach Trigger | Line 1 | Line 2 | Oh My`

It's possible to user nickname substituion by using `#nick` within the response or you can make the bot respond with actions by prefixing the response with a `+` (plus sign). You can also use `#botnick` to represent the bot's nick within responses:  
`!learm How do I have sex? | Stop asking lame questions #nick! | +kicks #nick`  
`!teach Awesomeness | Yes, #botnick is awesome!`

The `!relearn` or `!reteach` commands can be used to overwrite the current trigger/response pairs with the new ones.
`!relearn Replaced Trigger | And here's a new response!`  
`!reteach Trigger | Line4 | LineX | LineAwesome`

To see how many triggers match a phrase, use the `!find` command followed by the phrase:  
`!find Joe`  
`!find Trixar_za is God`

To make TazBot forget a learned response use, the `!forget` command followed by the phrase:  
`!forget Joe`  
`!forget Trixar_za is dumb`

To see how many responses TazBot has learned so far you can use the `!responses` command:  
`!responses`

Otherwise there is other simple commands to control the bot:  
`!nick newnick` - Makes the bot change it's nickname to newnick  
`!join #chan` - Makes the bot join #chan  
`!part #chan` - Makes the bot part #chan  
`!quit` - Makes the bot quit

The Bot also features a few easter eggs so try asking the bot about the number `42`, where all the `girls` are, if it's a kind robot `overlord` or what it thinks about `Windows 8`. ;)