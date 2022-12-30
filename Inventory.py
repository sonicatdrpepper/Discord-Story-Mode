import SQL
import discord
#This list contains the name of every valid item in the Database, ***VERY VITAL***, make sure to keep it updated!
#The positions of items in this list also dictate their positions within the inventories of players when the inventory is being read into memory
Items=["Test_Item","Knife","BetterKnife"]
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
async def DisplayInventory(User,ctx):
    Inventory=[]
    User=str(ctx.author.id)
    for i in range(len(Items)):
        Item=Items[i-1]
        pass
        Data = SQL.ReadSQL(User,Item,"ID","Inventory")
        Inventory.append(Data)
    #Construct embed
    description=""
    Embed = discord.Embed(type="rich",title="Inventory",description=description)
    for j in range(len(Items)):
        if Inventory[j] == "0":
            pass
        else:
            Embed.add_field(name=Items[j-1],value=Inventory[j],inline=True)
    await ctx.send(embed=Embed)
#DisplayInventory(367685478226460704,1)