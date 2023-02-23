import discord
import SQL,Tables
from Image_Manip import Composite, QueueText
#This list contains the name of every valid item in the Database, ***VERY VITAL***, make sure to keep it updated!
#The positions of items in this list also dictate their positions within the inventories of players when the inventory is being read into memory
Items = Tables.Items
#User should be the Player's ID
#Item should be the Name of the item, as defined in its relevant column in the database
#Amount is the amount of item the Player should have
#SetItemAmt Directly overwrites the amount of an item, AddItems/RemoveItems are just there to more easily add subtract from the value. Amount defaults to 0
def SetItemAmt(User,Item,Amount):
    SQL.WriteSQL(Item,"ID",Amount,User,"Inventory")

def AddItems(User,Item,Amount=0):
    AmountPresent = SQL.ReadSQL(User,Item,"ID","Inventory")
    Amount = AmountPresent+Amount
    SQL.WriteSQL(Item,"ID",Amount,User,"Inventory")

def RemoveItems(User,Item,Amount=0):
    AmountPresent = SQL.ReadSQL(User,Item,"ID","Inventory")
    Amount = AmountPresent-Amount
    SQL.WriteSQL(Item,"ID",Amount,User,"Inventory")

#Displays the Inventory info of a User, as a Discord Embed.
#TODO Make this generate an image instead, easier to work with that way
def DisplayInventory(User,ctx):
    #Read inventory from Save File
    Inventory=[]
    if ctx != 1:
        User=str(ctx.author.id)
    else:
        User=str(User)
    #Get list of all items in the players inventory, and their amounts
    for i in range(len(Items)):
        List=[]
        Item=Items[i-1]
        Data = SQL.ReadSQL(User,Item,"ID","Inventory")
        List.insert(0,Item)
        
        if i == 0:
            List.insert(1,Data)
        else:
            List.insert(i,Data)
        Inventory.insert(i-1,List)
    BGPATH="Images/Matte.png"
    for j in range(len(Inventory)):
        FP=f"Images/Items/{Inventory[j][0]}.png"
        Composite(FP,BGPATH,(j*0,j*50),"Images/Output.png")
        QueueText("Images/Output.png",0,0,0,"Fonts/Hack-Regular.ttf",[(150,j*50),(150,j*50),(150,j*50),(150,j*50)],[Inventory[j][1],Inventory[j][1],Inventory[j][1],Inventory[j][1]],[32,32,32,32])
        BGPATH="Images/Output.png"
        print(Inventory[j][0])

DisplayInventory(367685478226460704,1)