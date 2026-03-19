# Modified for L E G I O N, Twow guild in Ambershire
# Forked from https://github.com/wierdthing/shootyepgp-ret (RET, Tel'abim)

## Roll commands for L E G I O N

- /ret roll (mainspec roll)
- /ret sr (soft-reserve roll)
- /ret dsr (double soft-reserve roll)
- /retcsr (cumulative soft-reserve roll)
- /ret ep (check your EP if you are a PUG)

With the cumulative roll, you can provide it the number of weeks you have SR'ed an item
ie "/retcsr 3" will roll with +60 for 3 weeks of SR

## EP/GP export to file

Added by L E G I O N (Ambershire). Use `/shootyexport` in chat to dump the current EP/GP standings to a SavedVariable.
Then type `/quit` to let WoW write it to disk. The file will be saved at:
```
WTF/Account/<ACCOUNTNAME>/SavedVariables/shootyepgp.lua
```

Then run `epgp_export.py` (included in this repo) to convert it to `CSV` and `JSON`.
The script will find the file automatically, or ask you for your WoW folder path if it can't.

---

# shootyepgp

Guild Helper addon for EPGP loot system in WoW (1.12)

## setup

shootyepgp requires some modifications to guild permissions for officer notes by the guild leader.

### Version 3.x (current)

- officer notes must be set to visible by all and editable **only** by the EPGP admins (eg. officer rank+)
- public notes are not in use by the addon

#### _Version 2.x (deprecated)_

- _public and officer notes must be set to visible by all._
- _both public and officer notes **must** be editable **only** by the EPGP admins (eg. officer rank+)_

## tips

Create a new chatframe (right-click > create new window on chat tab) and name it `debug` (capitalization doesn't matter)  
Most of the information messages will now print on that frame and not clutter your default chatframe.

## usage

Right-click on minimap or FuBar shootyepgp icon will show all available settings.  
Left-click shows the standings window with everyone's EP, GP and PR values.  
The standings window can also be toggled with **/shooty show** chat command.

## features

- EPGP standings list (all)
- Simple chatlink click to bid on items (all)
- Item Bids list (admin/ML)
- Item GP prices on item tooltips (all)
- Export standings to csv (all)
- **Export standings to file via `/shootyexport` + `epgp_export.py` — added by L E G I O N (Ambershire)**
- Configurable EPGP Decay (admin)
- Configurable Offspec discount (admin)
- Guild Progression multiplier (admin)
- Reserves - *standby list EP* - with alts support (admin and all)

Addon has been designed so that basic member functionality is usable even without the addon.

- `/w <masterlooter name> +` (for main spec) or `/w <masterlooter name> -` (for off spec) after the loot officer links a piece of loot and asks for bids in raid chat.
- Type `/x +` (where x is the number of the custom channel) or `/x +MainName` if on an alt to respond to a standby list afk check.

Having the addon makes everything more convenient, but is not mandatory.

## epgp basics and help

[shootyepgp wiki](https://github.com/Road-block/shootyepgp/wiki)

## download

- Release version: Download shootyepgp-x.y-11200.zip file from [latest](https://github.com/Road-block/shootyepgp/releases/latest) and extract to AddOns folder.
- *Alpha version: Download shootyepgp-master.zip from [here](https://github.com/Road-block/shootyepgp/archive/master.zip) extract to AddOns folder and **remove** the -master suffix from the folder so it's just `shootyepgp`.*
