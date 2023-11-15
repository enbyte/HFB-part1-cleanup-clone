# HFB
 


### Getting Started:

First off I would like to welcome everybody to the official Hypixel Flipper Bot repository and also go ahead and thank you for your contributions. Some quick notes before you get started: 
- The output functions as well as Discord MessageIds & Webhooks are hidden for obvious reasons.
- main.py is, as of now, three programs mashed into one, lowest(), volume(), & main() all started in a while loop at the bottom of main.py. This is because I can't afford multiple Virtual Machines.
- lowest() creates a dictionary of the auctions bins and sorts them from lowest to highest and stores them in lowest.txt, lbin_data.txt (all time lbins), & avg_lbin.txt.
- volume() self explanatory, stores the amount of items sold in volume.txt. volume_ignore.txt is used to know what auctions we've already stored "{AUC_ID:EPOCH}". Epcoh is stored in volume_ignore so we can remove the store after 60 seconds.
- main() This is where the main process happens. It will go through every AH/BZ, look at possible crafting profits, then create the embeds, and output the information.


### Benefits For Contributing:
All contruibers will get free premium as a thanks for their ongoing dedication to improving HFB. Additionally, depending on contributions, a commission can be arranged for those who feel they deserve it!

### FAQ
Q: What is the discord invite?
A: https://discord.gg/A88qYcdwyG

Q: I contributed how do I get my free premium?
A: Shoot me a DM on discord @ .yellowblood with a short description of your contributions as well as the pull requests.
