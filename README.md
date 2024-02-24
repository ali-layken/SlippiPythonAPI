# SlippiPython
API for interacting with standardized slippi replay data (.slp) from smash.gg sets. The smash.gg API descrription has been updated and (.slp) has changed alot in the last 7 years. This project is no longer being supported I wrote it in highschool. To work with slippi data in python please refer to this community effort: https://pypi.org/project/py-slippi/

## How to use:

-run DownloadStats.py and follow the directions

# Ouput:
kill.txt & stats.txt are examples of what the output will look like.

## How to develop:
-make a pickle and open the pickle created by DownloadStats.py

everything that you need to extract new stats like maybe stage win% or somthing will be conatianed in the pickle.



### The pickle is a list with 2 things:

-ALL of the set data as a dict

-a dict with info about every game so u dont have to loop over and grab it before doing whaetever stat
