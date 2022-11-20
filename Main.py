import discord
from SQL import CheckSQLUser, ReadSQL, GetAllData
import random
import configparser
from time import sleep

TOKEN="MTA0MzczNDY5NDQ4MDU4MDcyOQ.GXD-am.WUDQN3kwofDBDWE-HwZ320xSEkLoAcLADyAOgA"
client=discord.Bot()

#Read INI Config File
config = configparser.ConfigParser()
config.read("Config.ini")
Better_Fight_AI = config.get('Settings','AdvancedFightLogic')

@client.event
async def on_ready():
    print("Successfully Connected to Discord")

@client.slash_command(name="test-battle")
async def test(ctx):
    await Fight_NPC_Complex(ctx,"TEST_NPC",ctx.author)

@client.slash_command(name="test-cutscene")
async def cutscene_test(ctx):
    await cutscene(ctx,"cutscenes/test_cutscene.cutscene")

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
    
    ID1=str(Opponent2.id)
    Opponent2_HP=ReadSQL(ID1,"HP","ID","UserData")
    Opponent2_Level=ReadSQL(ID1,"LEVEL","ID","UserData")
    Opponent2_Class=ReadSQL(ID1,"CLASS","ID","UserData")
    Opponent2_Battle_Intro=ReadSQL(ID1,"INTRO","ID","UserData")
    
    turn_no = 1
    #Initial Message for
    await ctx.respond(f"**{Opponent2.name}** Lvl:`{Opponent2_Level}` Challenges **{Opponent1_Name}** Lvl:`{Opponent1_Level}`\n**{Opponent2.name}:** {Opponent2_Battle_Intro}\n**{Opponent1_Name}:** {Opponent1_Battle_Intro}\n")
    message = await ctx.send(f"**{Opponent2.name}** HP:`{Opponent2_HP}`\n**{Opponent1_Name}** HP:`{Opponent1_HP}`\nBattle Start! \nTurn: {turn_no}")
    while True:
        #Check for loop break condition
        if Opponent1_HP <= 0:
            await ctx.send(f"{Opponent2.name} Won")
            break
        if Opponent2_HP <= 0:
            await ctx.send("Opponent1_Name Won")
        
        #Do damage calculations
        Data=Execute_Turn(Opponent1_Name,Opponent2)
        #Extract Data from Execute_Turn
        NPC_ATTACK_RNG=Data[0]
        PLAYER_ATTACK_RNG=Data[1]
        MessageContents=Data[2]
        #Update UI
        MessageContents=f"**{Opponent2.name}** HP:`{Opponent2_HP}`\n**{Opponent1_Name}** HP:`{Opponent1_HP}`\n{MessageContents} \nTurn: `{turn_no}`"
        await message.edit(content=MessageContents)
        #Update HP values
        Opponent1_HP=Opponent1_HP-PLAYER_ATTACK_RNG
        Opponent2_HP=Opponent2_HP-NPC_ATTACK_RNG
        #Increment Turn
        turn_no=turn_no+1
        sleep(1)


def generate_stats(userID):
    userID=str(userID)
    Level=ReadSQL(userID,"level","ID","data")
    Data=[]
    Def = 0
    Atk = 0
    Crt = 0
    Ddg = 0
    for i in range(int(Level)):
        RNG0 = random.randint(0,3)
        RNG1 = random.randint(0,3)
        RNG2 = random.randint(0,3)
        RNG3 = random.randint(0,3)
        Def = Def+RNG0
        Atk = Atk+RNG1
        Crt = Crt+RNG2
        Ddg = Ddg+RNG3
    Data.append(Def)
    Data.append(Atk)
    Data.append(Crt)
    Data.append(Ddg)
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
def cutscene(ctx,cutsceneID):
    #Read Cutscene File
    CutsceneData= open(cutsceneID,'r')
    Lines = CutsceneData.readlines()
    count=0
    #Read actual cutscene data
    for line in Lines:
        count+=1
        #Read Metadata from first line
        if count==1:
            Metadata=line.split(',')
            Cutscene_Name=Metadata[0]
            Cutscene_Name=Cutscene_Name.rstrip()
            NPCs = []
            #Construct list of NPC's that are present in the cutscene
            for i in range(len(Metadata)):
                if i == 1:
                    pass
                else:
                    NPCs.append(Metadata[i])
        #Start Reading past line 1
        else:
            pass
            #print(line.rstrip())
cutscene(0,"cutscenes/test_cutscene.cutscene")
#client.run(TOKEN)