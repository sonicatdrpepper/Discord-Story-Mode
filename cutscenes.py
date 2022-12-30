import SQL, time

#Cutscene Metadata
Name="Test Cutscene"
#List of NPCs presetn in cutscene by id
NPCs=["TEST_NPC","TEST_NPC_2"]
Events = ["{END}", "{BATTLE}", "{ITEM}", "{DIALOGUE_RESPONSE}","{WAIT}"]

global WaitTriggered
WaitTriggered = 0
ItemTriggered = 0
#Read in Data of NPCs that are present in the cutscene
NPC1_Name=SQL.ReadSQL(NPCs[0],"PRETTY_NAME","NAME","NPCData")
NPC1_Class=SQL.ReadSQL(NPCs[0],"CLASS","NAME","NPCData")
NPC2_Name=SQL.ReadSQL(NPCs[1],"PRETTY_NAME","NAME","NPCData")
NPC2_Class=SQL.ReadSQL(NPCs[1],"CLASS","NAME","NPCData")

async def Play_Cutscene(ctx,ID):
    Meta = open(f"cutscenes/{ID}.md","r")
    Data = open(f"cutscenes/{ID}.cut","r")
    #Read cutscene metadata
    MLines = Meta.readlines()
    Cutscene_Name = MLines[0].strip()
    Friendly_NPC = MLines[1].split(',')
    Enemy_NPC = MLines[2].split(',')
    #NPC Variables
    
    #Player Variables
    Player_Name = ctx.author.name
    Player_Class = SQL.ReadSQL(str(ctx.author.id),"CLASS","ID","UserData")
    
    #Read cutscene actual data, and process events
    DLines = Data.readlines()
    for line in DLines:
        line = line.strip()
        Data_Return = []
        if line.startswith("//") == True:
            pass
        elif line in Events:
            #Handle {END} Event
            if line == Events[0]:
                return
            #Handle {BATTLE} Event
            elif line == Events[1]:
                Data_Return.append(Events[1])
                Data_Return.append(Enemy_NPC[0])
                print("Battle Triggered")
                return Data_Return
            #Handle {ITEM} Event
            elif line == Events[2]:
                Data_Return.append(Events[2])
                
                return Data_Return
            #Handle {DIALOGUE_RESPONSE} Event
            elif line == Events[3]:
                Data_Return.append(Events[3])
                return Data_Return
            #Handle {WAIT} Event
            elif line == Events[4]:
                global WaitTriggered
                WaitTriggered = 1
        
        #Actually execute WAIT event
        elif WaitTriggered == 1:
            try:
                time.sleep(float(line))
            except:
                print("Exception thrown during WAIT event, most likely specified time was not an integer/float, or the string conversion failed")
            WaitTriggered = 0
        elif ItemTriggered == 1:
            Items = line.split(',')
            Item = Items[0]
            Amount = Items[1]
            try:
                #Add Item and Amount to Data_Return to make the event function
                Data_Return.append(Events[2])
                Data_Return.append(Item)
                Data_Return.append(Amount)
                return Data_Return
            except:
                print("Exception thrown while processing ITEM event")
        #Run if line does not contain an event
        else:
            line = line.replace("Player_Name", Player_Name)
            line = line.replace("Player_Class", Player_Class)
            print(line)
            await ctx.send(line)