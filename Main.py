import discord,random,configparser
from SQL import CheckSQLUser, ReadSQL, GetAllData, WriteSQL
from time import sleep
from cutscenes import *
from Image_Manip import Download, CreateStatCard,CreateLevelCard
import Inventory

TOKEN="MTA0MzczNDY5NDQ4MDU4MDcyOQ.GXD-am.WUDQN3kwofDBDWE-HwZ320xSEkLoAcLADyAOgA"
client=discord.Bot()

@client.event
async def on_ready():
    print("Successfully Connected to Discord")

@client.slash_command(name="test-cutscene")
async def test_cutscene(ctx):
    #await cutscene(ctx,"cutscene1")
    await Inventory.DisplayInventory(ctx.author.id,ctx)
    
@client.slash_command(name="view_stats")
async def stats(ctx):
    ID1=str(ctx.author.id)
    if CheckSQLUser(ctx.author.id) == 0:
        await ctx.respond("That user is not in the database")
        return
    else:
        pass
        #Read Data
        HP=ReadSQL(ID1,"HP","ID","UserData")
        Level=ReadSQL(ID1,"LEVEL","ID","UserData")
        Class=ReadSQL(ID1,"CLASS","ID","UserData")
        EXP=ReadSQL(ID1,"CEXP","ID","UserData")
        DEF = ReadSQL(ID1,"DEF","ID","UserData")
        ATK = ReadSQL(ID1,"ATK","ID","UserData")
        CRT = ReadSQL(ID1,"CRT","ID","UserData")
        DDG = ReadSQL(ID1,"DDG","ID","UserData")
        URL=ctx.author.avatar.url
        Download(URL,"Images/Avatar.png")
        CreateStatCard(ATK,DEF,CRT,DDG,HP,Class,ctx.author)
        f = discord.File("Images/Usercard.png")
        await ctx.respond(file = f)

#Main Fight Function
#Opponent1 is the NPC
#Opponent2 is the Player
async def Fight_NPC_Complex(ctx,Opponent1,Opponent2):
    #Read Fighter Data
    Opponent1_Name=Opponent1
    Opponent1_HP=ReadSQL(Opponent1_Name,"HP","NAME","NPCData")
    Opponent1_Level=ReadSQL(Opponent1_Name,"LEVEL","NAME","NPCData")
    Opponent1_Class=ReadSQL(Opponent1_Name,"CLASS","NAME","NPCData")
    Opponent1_Battle_Intro=ReadSQL(Opponent1_Name,"INTRO","NAME","NPCData")
    Opponent1_EXP_Drop=ReadSQL(Opponent1_Name,"EXP","NAME","NPCData")
    
    ID1=str(Opponent2.id)
    ReadSQL(ID1,)
    Opponent2_HP=ReadSQL(ID1,"HP","ID","UserData")
    Opponent2_Level=ReadSQL(ID1,"LEVEL","ID","UserData")
    Opponent2_Class=ReadSQL(ID1,"CLASS","ID","UserData")
    Opponent2_Battle_Intro=ReadSQL(ID1,"INTRO","ID","UserData")
    Opponent2_EXP=ReadSQL(ID1,"EXP","ID","UserData")
    Opponent2_CEXP=ReadSQL(ID1,"CEXP","ID","UserData")
    
    #Leveling Formula
    ToNextLevel=Opponent2_Level*100
    turn_no = 1
    
    #Initial Message for UI
    await ctx.respond(f"**{Opponent2.name}** Lvl:`{Opponent2_Level}` Challenges **{Opponent1_Name}** Lvl:`{Opponent1_Level}`")
    #message = await ctx.send(f"**{Opponent2.name}** HP:`{Opponent2_HP}`\n**{Opponent1_Name}** HP:`{Opponent1_HP}`\nBattle Start! \nTurn: {turn_no}")
    description = f"**{Opponent2.name}** HP:`{Opponent2_HP}`\n**{Opponent1_Name}** HP:`{Opponent1_HP}`\nBattle Start! \nTurn: {turn_no}"
    embed = discord.Embed(title="Battle",type="rich",description=description)
    message = await ctx.send(embed=embed)
    while True:
        #Check for loop break condition
        if Opponent1_HP <= 0:
            await ctx.send(f"{Opponent2.name} Won and earned {Opponent1_EXP_Drop} EXP Points")
            WriteSQL("EXP","ID",Opponent2_EXP+Opponent1_EXP_Drop,ID1,"UserData")
            #Check if leveled up
            if Opponent2_CEXP+Opponent1_EXP_Drop>=ToNextLevel:
                WriteSQL("LEVEL","ID",Opponent2_Level+1,ID1,"UserData")
                WriteSQL("CEXP","ID",0,ID1,"UserData")
                #Stat growths
                Stats = increase_stats(ID1)
                #Tell user that they leveled up
                URL=ctx.author.avatar.url
                Download(URL,"Images/Avatar.png")
                CreateLevelCard(Stats[0],Stats[1],Stats[2],Stats[3],Stats[4],Opponent2_Class,Opponent2)
                f = discord.file("Images/Usercard.png")
                await ctx.respond(File = f)
            else:
                WriteSQL("CEXP","ID",Opponent2_CEXP+Opponent1_EXP_Drop,ID1,"UserData")
            break
        if Opponent2_HP <= 0:
            await ctx.test("Opponent1_Name Won")
        
        #Do damage calculations
        Data=Execute_Turn(Opponent1_Name,Opponent2)
        #Extract Data from Execute_Turn
        NPC_ATTACK_RNG=Data[0]
        PLAYER_ATTACK_RNG=Data[1]
        MessageContents=Data[2]
        #Update UI
        MessageContents=f"**{Opponent2.name}** HP:`{Opponent2_HP}`\n**{Opponent1_Name}** HP:`{Opponent1_HP}`\n{MessageContents} \nTurn: `{turn_no}`"
        embed=discord.Embed(title="Battle",type="rich",description=MessageContents)
        await message.edit(embed=embed)
        #Update HP values
        Opponent1_HP=Opponent1_HP-PLAYER_ATTACK_RNG
        Opponent2_HP=Opponent2_HP-NPC_ATTACK_RNG
        #Increment Turn
        turn_no=turn_no+1
        sleep(1)

#Stat growths function
def increase_stats(userID):
    userID=str(userID)
    Def = ReadSQL(userID,"DEF","ID","UserData")
    Atk = ReadSQL(userID,"ATK","ID","UserData")
    Crt = ReadSQL(userID,"CRT","ID","UserData")
    Ddg = ReadSQL(userID,"DDG","ID","UserData")
    HP = ReadSQL(userID,"HP","ID","UserData")
    LVL = ReadSQL(userID,"LEVEL","ID","UserData")
    #Class will affect growth rates and starting stats
    Class = ReadSQL(userID,"CLASS","ID","UserData")
    Data=[]
    RNG0 = random.randint(0,3)
    RNG1 = random.randint(0,3)
    RNG2 = random.randint(0,3)
    RNG3 = random.randint(0,3)
    RNG4 = random.randint(1,LVL*2)
    Def = Def+RNG0
    Atk = Atk+RNG1
    Crt = Crt+RNG2
    Ddg = Ddg+RNG3
    HP = HP+RNG4
    WriteSQL("ATK","ID",Atk,userID,"UserData")
    WriteSQL("DEF","ID",Def,userID,"UserData")
    WriteSQL("CRT","ID",Crt,userID,"UserData")
    WriteSQL("DDG","ID",Ddg,userID,"UserData")
    WriteSQL("HP","ID",HP,userID,"UserData")
    #Check which stats increased
    if RNG0 == 0:
        Def = [Def,0]
    else:
        Def = [Def,1]
    
    if RNG1 == 0:
        Atk = [Atk,0]
    else:
        Atk = [Atk,1]
        
    if RNG2 == 0:
        Crt = [Crt,0]
    else:
        Crt = [Crt,0]
    
    if RNG3 == 0:
        Ddg = [Ddg,0]
    else:
        Ddg = [Ddg,1]
    
    Data.append(Def)
    Data.append(Atk)
    Data.append(Crt)
    Data.append(Ddg)
    Data.append(HP)
    return Data

def Execute_Turn(Opponent1_ID,Opponent2):
    #Get Stats from DB
    Def1=ReadSQL(Opponent1_ID,"DEF","NAME","NPCData")
    Atk1=ReadSQL(Opponent1_ID,"ATK","NAME","NPCData")
    Ddg1=ReadSQL(Opponent1_ID,"DDG","NAME","NPCData")
    Crt1=ReadSQL(Opponent1_ID,"CRT","NAME","NPCData")
    
    ID1=str(Opponent2.id)
    Def2=ReadSQL(ID1,"DEF","ID","UserData")
    Atk2=ReadSQL(ID1,"ATK","ID","UserData")
    Ddg2=ReadSQL(ID1,"DDG","ID","UserData")
    Crt2=ReadSQL(ID1,"CRT","ID","UserData")
    
    
    #Crit RNG            
    NPC_CRIT=random.randint(0,100)
    PLAYER_CRIT=random.randint(0,100)
    #Dodge RNG
    NPC_DODGE=random.randint(0,100)
    PLAYER_DODGE=random.randint(0,100)
    #Attack RNG
    Player_ATK_RNG = random.randint(0+Atk2,10+Atk2)-Def1
    NPC_ATK_RNG = random.randint(0+Atk1,10+Atk1)-Def2
    if Player_ATK_RNG <= 0:
        Player_ATK_RNG = 0
    if NPC_ATK_RNG <= 0:
        NPC_ATK_RNG = 0
    
    #Damage Checks
    Data=[]
    if PLAYER_DODGE <= Ddg2:
            NPC_ATK_RNG = 0
            if PLAYER_CRIT <= Crt2:
                Player_ATK_RNG=Player_ATK_RNG*3
                message=f"**{Opponent2.name}** dodged **{Opponent1_ID}'s** Attack, and landed a critical hit dealing `{Player_ATK_RNG}` Damage!\n"
                Data.append(NPC_ATK_RNG)
                Data.append(Player_ATK_RNG)
                Data.append(message)
                return Data
            
            message=f"**{Opponent2.name}** dodged **{Opponent1_ID}'s** Attack, and landed a hit dealing `{Player_ATK_RNG}` Damage!\n"
            Data.append(NPC_ATK_RNG)
            Data.append(Player_ATK_RNG)
            Data.append(message)
            return Data
        
    if NPC_DODGE <= Ddg1:
        Player_ATK_RNG = 0
        if NPC_CRIT <= Crt1:
            NPC_ATK_RNG=NPC_ATK_RNG*3
            message=f"**{Opponent1_ID}** dodged **{Opponent2.name}'s** Attack, and landed a critical hit dealing `{NPC_ATK_RNG}` Damage!\n"
            Data.append(NPC_ATK_RNG,)
            Data.append(Player_ATK_RNG)
            Data.append(message)
            return Data
        
        message=f"**{Opponent1_ID}** dodged **{Opponent2.name}'s** Attack, and landed a hit dealing `{NPC_ATK_RNG}` Damage!\n"
        Data.append(NPC_ATK_RNG,)
        Data.append(Player_ATK_RNG)
        Data.append(message)
        return Data
        
    if NPC_CRIT <= Crt1:
        NPC_ATK_RNG = NPC_ATK_RNG*3
        message=f"**{Opponent1_ID}** Landed a critical hit dealing `{NPC_ATK_RNG}` Damage!\n**{Opponent2.name}** Landed a hit dealing `{Player_ATK_RNG}` Damage."
        if PLAYER_CRIT <= Crt2:
            Player_ATK_RNG = Player_ATK_RNG*3
            message=f"**{Opponent1_ID}** Landed a critical hit dealing `{NPC_ATK_RNG}` Damage!\n**{Opponent2.name}** Landed a critical hit dealing `{Player_ATK_RNG}` Damage!"
        Data.append(NPC_ATK_RNG,)
        Data.append(Player_ATK_RNG)
        Data.append(message)
        return Data
            
    if PLAYER_CRIT <= Crt2:
        Player_ATK_RNG = Player_ATK_RNG*3
        message=f"**{Opponent2.name}** Landed a critical hit dealing `{Player_ATK_RNG}` Damage!\n**{Opponent1_ID}** Landed a hit dealing `{NPC_ATK_RNG}` Damage."
        if NPC_CRIT <= Crt1:
            NPC_ATK_RNG = NPC_ATK_RNG*3
            message=f"**{Opponent2.name}** Landed a critical hit dealing `{Player_ATK_RNG}` Damage!\n**{Opponent1_ID}** Landed a critical hit dealing `{NPC_ATK_RNG}` Damage!"
        Data.append(NPC_ATK_RNG,)
        Data.append(Player_ATK_RNG)
        Data.append(message)
        return Data
    else:
        message=f"**{Opponent2.name}** Landed a hit dealing `{Player_ATK_RNG}` Damage.\n**{Opponent1_ID}** Landed a hit dealing `{NPC_ATK_RNG}` Damage."
        Data.append(NPC_ATK_RNG,)
        Data.append(Player_ATK_RNG)
        Data.append(message)
        return Data

#Plays a cutscene from a cutscene file
async def cutscene(ctx,cutsceneID):
    #Read Cutscene File
    Player = ctx.author
    tmp = await ctx.respond("_")
    # time.sleep(0.1)
    # tmp.delete()
    # time.sleep(.5)
    Event = await Play_Cutscene(ctx,cutsceneID)
    #Handle BATTLE event
    if Event[0] == "{BATTLE}":
        print("Executing Battle")
        await Fight_NPC_Complex(ctx,Event[1],Player)
        return
    #Handle ITEM event
    elif Event[0] == "{ITEM}":
        #TODO implement a Inventory system for this event to work
        Amount = Event[2]
        Item = Event[1]
        if Amount > 0:
            Inventory.AddItems(str(Player.id),Item,Amount)
            await ctx.send(f"You gained {Amount} of {Item}")
        elif Amount < 0:
            Inventory.RemoveItems(str(Player.id),Item,Amount)
            await ctx.send(f"You lost {Amount} of {Item}")

#Adds Player to the database, and sets up all relevant values
def Init():
    pass

client.run(TOKEN)