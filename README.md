Create unique* human-friendly system names from raw ED system names (like Wregoe CJ-X c28-22 or HIP 99188).

Command line usage: 

python ProceduralSystemRename.py "HIP 99188"

This prints the humanised name, and resulting pairs of [<raw_name>, <humanised_name>] are added to pair_database.lst.
pair_database.lst is queried first to find a pre-existing match.
Since either a humanised or raw name can be fed to the routine, pair_database.lst permits finding the original raw name for a previously humanised name.

*Technically, two different raw system names can result in the same humanised same, but it is highly unlikely to encounter this in ad hoc usage. 
