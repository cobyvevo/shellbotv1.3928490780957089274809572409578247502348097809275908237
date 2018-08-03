import discord
from discord.ext import commands
import urllib.request
import lxml.html
import random
client = commands.Bot(command_prefix = ".")

def getcat():
    tree = lxml.html.parse("http://random.cat/view")
    images = tree.xpath("//img/@src")
    return images[0]

def extractphoto(oof,base,keyword,ignore):
    s = ""
    query = (base+oof)
    imgrees = []
    tree = lxml.html.parse(s.join(query))
    images = tree.xpath("//img/@src")
   
    for img in images:
        if img.find(keyword) == 0:
            if img.find(ignore) != 0:
                imgrees.append(img)

            
    return imgrees

def gethentai(tag,page):
    s = ""
    query = ("http://konachan.com/post?page="+str(page)+"&tags=" , tag)
    newimages = []
    tree = lxml.html.parse(s.join(query))
    images = tree.xpath("//a/@href")
    for img in images:
        if img.find("/post/show/") == 0:
            newimages.append(extractphoto(img,"http://konachan.com","https://konachan.com/","https://konachan.com/data/avatars"))
    
    return newimages

def gethentaithumb(tag,page):
    s = ""
    query = ("http://konachan.com/post?page="+str(page)+"&tags=" , tag)
    newimages = []
    tree = lxml.html.parse(s.join(query))
    images = tree.xpath("//img/@src")
    for img in images:
        if img.find("https://konachan.com/") == 0:
            newimages.append(img)
    
    return newimages

def gethentailink(tag,page):
    s = ""
    query = ("http://konachan.com/post?page="+str(page)+"&tags=" , tag)
    newimages = []
    tree = lxml.html.parse(s.join(query))
    images = tree.xpath("//a/@href")
    for img in images:
        if img.find("/post/show/") == 0:
            newimages.append(img)
    
    return newimages


def randomhentai(tag):
    allhents = []
    page = 1
    items = 100
    while items > 0 and page < 6:
        hentais = gethentailink(tag,page)
        for im in hentais:
            allhents.append(im)
        page = page + 1
        items = len(hentais)
        
    if len(allhents) > 0:
        chosen = random.choice(allhents)
        return extractphoto(chosen,"http://konachan.com","https://konachan.com/","https://konachan.com/data/avatars")[0]
    else:
        return "No results found"

    
info_dir = "info/"
picture_dir = "images/"

nsfw_saves = "nsfws.txt"
talk_saves = "talks.txt"

token = "NDc0NjczNDA0NDQ5MTI4NDY4.DkUByQ.eytEmR0dn9rpyvAJCFMYlTMAaP8"

nsfw_channel_names = {}
talk_messages = {}

def savedictionary(filename,arra):
    with open(info_dir+filename,"w") as f:
        for key, value in arra.items():
            f.write(str(key)+"="+str(value)+"\n")
            
def loaddictionary(filename):
    lamo = {}  
    file = open(info_dir+filename)
    for line in file:
        line = line.rstrip() 
        x = line.split("=")
        a = x[0]
        b = x[1]
        lamo[a] = b
        
    return lamo
            
def loadnsfws():
    global nsfw_channel_names
    nsfw_channel_names = loaddictionary(nsfw_saves)
    print(nsfw_channel_names)
    
def savensfws():
    savedictionary(nsfw_saves,nsfw_channel_names)

def loadtalks():
    global talk_messages
    talk_messages = loaddictionary(talk_saves)
    print(talk_messages)
    
def savetalks():
    savedictionary(talk_saves,talk_messages)

def isowner(msg):
    if msg.server.owner.id == msg.author.id:
        return True
    else:
        return False

passedmessage = []
passeduser = []

olofissad = ["olof is the best","olof is good","olof is cool","is olof cool","is olof the best","is olof amazing","olof is amazing"]

loadnsfws()
loadtalks()

@client.event
async def on_ready():
    print("im ready")
    loadnsfws()
    loadtalks()

@client.event
async def on_message(msg):
    global passedmessage
    global passeduser
    
    if msg.author.id == client.user.id:
        return

    if msg.content in olofissad:
        await client.send_message(msg.channel, "olof is sad")
        
    
    if msg.content == "ur gay bot":
        await client.send_message(msg.channel, "no u")
    if msg.content == "gib info pls bot":
        userid = msg.author.id
        await client.send_message(msg.channel, "ur gay <@{}>".format(userid))
    if msg.content == "gib gun pls bot":
        userid = msg.author.id
        await client.send_file(msg.channel, picture_dir+"inter.png")
    if msg.content == "gib cat pls bot thx":
        await client.send_message(msg.channel, getcat())
    msgcontent = msg.content.lower()
    
    if msgcontent[0] != "." :
        passedmessage.append(msg.content)
        passeduser.append(msg.author.id)
        
    global talk_messages
    
    past = len(passedmessage)-2
    print(past)
    
    try:
        passedmessagel = passedmessage[past].lower()
    except IndexError:
        print("nope")
        
    msgcontent.replace("=", ":")

    await client.change_presence(game=discord.Game(name="nothing"))
    if msgcontent[0] != "." :
        if passedmessagel[0] != ".":
            if msg.author.id != passeduser[past]:
                if len(msg.mentions) == 0:
                    if msg.mention_everyone == False:
                        talk_messages[passedmessagel] = msgcontent
                        await client.change_presence(game=discord.Game(name="learning"))
                        savetalks()

        
       
    await client.process_commands(msg)
    
@client.command(pass_context=True)
async def hents(msg,tag=""):
    global nsfw_channel_names
    
    server = msg.message.server.id
    if server in nsfw_channel_names:
        print("found")
    else:
        nsfw_channel_names[server] = "nsfw"
        
    nsfwchannelname = nsfw_channel_names[server]

    if str(msg.message.channel.name) != nsfwchannelname:
        await client.say("this channel isnt nsfw")
    else:
        await client.say("Searching for " + tag + " hentai")
        await client.say(randomhentai(tag))
        
@client.command(pass_context=True)      
async def setnsfw(msg,name):
    if isowner(msg.message):
        global nsfw_channel_names
        server = msg.message.server.id
        nsfw_channel_names[server] = name
        await client.say("NSFW channel set to " + name)
        savensfws()
    else:
        await client.say("u arent owner u gey")
        
@client.command(pass_context=True)      
async def cb(msg):
    message = msg.message.content.lower()
    message = message.replace(".cb ", "")
    if message in talk_messages:
        await client.say(talk_messages[message])
        
@client.command(pass_context=True)     
async def cat():
    await client.say(getcat())
    
@client.command()     
async def refresh():
    loadnsfws()
    loadtalks()
    


    
               
        
client.run(token)
