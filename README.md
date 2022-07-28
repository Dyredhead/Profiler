# Profiler
A small python script for replicating Google Chrome's icon maker for new profiles

### Prologue:
Not too long ago I was still using Chrome as my main web browser. When I switched to Firefox I was dismayed to find that it did not have such great support for multipule profiles. When you made a new profile on Chrome, it prompted you to make a cusotm icon for that profile using your pfp. The icon would consist of a fullscale Chrome logo and then a small verison of your pfp in the top right corner. This made it extremly easy to know at a glance which icon coresponded to which profile. Becuase of this I decided to code up this python script to automatically generate a Chrome style icon for any application.

### How to use: 
```
python Profiler.py path/to/image/of/app path/to/image/of/pfp path/to/output/image
```
if no output path is provided, the script defaults to $HOME/Pictures/

### Examples:
if I had this firefox icon (courtesy of the [BeautyLine](https://www.gnome-look.org/p/1425426/) icon set): 

![firefox](/assets/firefox.png)

and this profile picture:

![pfp](/assets/PFP (School).png)

Then running ```python Profiler.py firefox.png pfp.png``` would give me an output of:

![firefox+pfp](/assets/firefox+pfp.png)
