#Tables for easier access than SQL, good for Immutable Data

#Item Stats
#Each one is stored as a List, with the structure being outlined in the file Inv Strucutre
Items=["Knife","BetterKnife","Test","Gun"]
Knife=["WEAPON","5","100",("L_HAND","R_HAND"),4]
BetterKnife=["WEAPON","10","200",("L_HAND","R_HAND"),8]

#Valid Commands/Keywords #Might add a sort of aliasing system, e.g grab and pickup mean the same thing
Commands=["inv","move","attack","kill","pickup","talk","equip"]

#Classes
#Index 0 is the name of the class, the next 5 indexes in the list are for stat growth bonuses/penalties
#1 = DEF,2 = ATK, 3 = CRT, 4 = DDG, 5 = HP
Class0=["Commoner",1,1,1,1,1]
Classes=[Class0]

#Battle Intro's