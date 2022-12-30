from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from SQL import ReadSQL
import requests
import shutil
#Crops a given image down to 128x128

def SquareCrop(FP):
    img=Image.open(FP)
    img.thumbnail((128,128),Image.Resampling.LANCZOS)
    w,h=img.size
    left = (w - 127)/2
    top = (h - 127)/2
    right = (w + 127)/2
    bottom = (h + 127)/2

    # Crop the center of the image
    img = img.crop((left, top, right, bottom))
    img.save(FP)

#Pastes a image onto a background, background is controlled by FP (file path)
def LevelCardComposite(FP,BGPATH,offset):
    img=Image.open(FP)
    img_w, img_h = img.size
    #BGPATH=ReadSQL(str(User),"Background","data")
    background = Image.open(BGPATH)
    bg_w, bg_h = background.size
    if has_transparency(FP)==False:
        img.convert("RGBA")
        img.putalpha(255)
    background.paste(img,offset,img)
    background.convert("RGBA")
    background.save('Images/Usercard.png')

#Draws text on top of a image, in path FP, RGB arguments control color
def DrawText(FP,Offset,Text,size,R,G,B,Font):
    img=Image.open(FP)
    Drawer=ImageDraw.Draw(img)
    CustomFont=ImageFont.truetype(Font, size)
    Drawer.text(Offset,Text,font=CustomFont,fill=(R,G,B))
    img.save(FP)

def QueueText(FP,R,G,B,Font,Offset=[(0,0)],Text=["Sample Text"],size=[1]):
    img=Image.open(FP)
    Drawer=ImageDraw.Draw(img)
    #CustomFont=ImageFont.truetype(Font,size)
    for i in range(len(Text)):
        CustomFont=ImageFont.truetype(Font,size[i])
        Drawer.text(Offset[i],Text[i],font=CustomFont,fill=(R,G,B))
    img.save(FP)

#Modifies the brightness of an image
def ModBrightness(FP,Factor):
    img2=ImageEnhance.Brightness(Image.open(FP))
    img2_output=img2.enhance(Factor)
    img2_output.save(FP)

#Checks if an image has alpha mask
def has_transparency(FP):
    img = Image.open(FP).convert("RGBA")
    alpha_range = img.getextrema()[-1]
    #if true image is not transparent
    if alpha_range == (255,255):
        return False
    else:
        return True

def CreateStatCard(ATK,DEF,CRT,DDG,HP,Class,Player):
    SquareCrop("Images/Avatar.png")
    L=ReadSQL(str(Player.id),"LEVEL","ID","UserData")
    LevelCardComposite("Images/Avatar.png","Images/Background.png",(0,0))
    QueueText("Images/Usercard.png",0,0,0,"Fonts/CyberpunkWaifus.ttf",[(288,32),(288,81),(461,80),(461,31)],[f"{ATK} ATK",f"{DEF} DEF",f"{DDG} DDG",f"{CRT} CRT"],[32,32,32,32])
    DrawText("Images/Usercard.png",(0,260),f"Level {L} {Class}",32,0,0,0,"Fonts/CyberpunkWaifus.ttf")
    DrawText("Images/Usercard.png",(288,130),f"{HP} HP",32,0,0,0,"Fonts/CyberpunkWaifus.ttf")
    #DrawText("Images/Usercard.png",(0,130),f"{Class}",32,0,0,0,"Fonts/CyberpunkWaifus.ttf")
        
def CreateLevelCard(ATK,DEF,CRT,DDG,HP,Class,Player):
    SquareCrop("Images/Avatar.png")
    L=ReadSQL(str(Player.id),"LEVEL","ID","UserData")
    LevelCardComposite("Images/Avatar.png","Images/Background.png",(0,0))
    if ATK[1]==1:
        LevelCardComposite("Images/Arrow-Scaled.png","Images/Usercard.png",(250,31))
    if DEF[1]==1:
        LevelCardComposite("Images/Arrow-Scaled.png","Images/Usercard.png",(250,81))
    if CRT[1]==1:
        LevelCardComposite("Images/Arrow-Scaled.png","Images/Usercard.png",(430,31))
    if DDG[1]==1:
        LevelCardComposite("Images/Arrow-Scaled.png","Images/Usercard.png",(430,81))
    QueueText("Images/Usercard.png",0,0,0,"Fonts/Hack-Regular.ttf",[(288,32),(288,81),(461,81),(461,32)],[f"{ATK[0]} ATK",f"{DEF[0]} DEF",f"{DDG[0]} DDG",f"{CRT[0]} CRT"],[32,32,32,32])
    DrawText("Images/Usercard.png",(0,260),f"{Player.name} Leveled Up to Level {L}!",32,0,0,0,"Fonts/Hack-Regular.ttf")
    DrawText("Images/Usercard.png",(288,130),f"{HP} HP",32,0,0,0,"Fonts/Hack-Regular.ttf")
    LevelCardComposite("Images/Arrow-Scaled.png","Images/Usercard.png",(250,130))

#Futureproofing incase the amount of item types goes over the limit for embed fields.
def InventoryDisplay(Items=[]):
    #Place item images on image
    pass
    #Place Text on Images
    for i in range(len(Items)):
        DrawText("Images/Matte.png",(0,0),Items[i],5,0,0,0,"Hack-Regular.ttf")

def Download(URL,FP):
    Avatar = requests.get(URL, stream = True)
    if Avatar.status_code == 200:
        try:
            with open(FP,'wb') as f:
                shutil.copyfileobj(Avatar.raw, f)
        except:
            print("Failed to Download file, probably invalid file path")