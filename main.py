from queue import Empty
import pyodbc
import discord
#https://github.com/mkleehammer/pyodbc/wiki

cnxn = pyodbc.connect(CONNECTION STRING)
crsr = cnxn.cursor()

intents = discord.Intents.default()
intents.message_content = True

def get_stats(user):
    crsr.execute("{CALL getStats (?)}", user)
    if(len(crsr.fetchall()) == 0):
        return user
    
    return crsr.fetchall()

def add_feature(user, feature):
    params = (user, feature)
    crsr.execute("{CALL add_feature (?,?)}", params)
    cnxn.commit()
    
    return "feature successfully added"

def add_new_item(user, item, quantity, weight = None):
    params = (user, item, quantity, weight)
    crsr.execute("{CALL add_new_item (?,?,?,?)}", params)
    cnxn.commit()

    return 'added item'

def add_spell(user, spell):
    params = (user, spell)
    crsr.execute("{call add_spell(?,?)}", params)
    cnxn.commit()
    return 'added spell'
def add_slots(user, level, quant):
    params = (user, level, quant)
    crsr.execute("{call add_SpellSlots(?,?,?)}", params)
    cnxn.commit()
    return 'added spell slots'


client = discord.Client(intents=intents)

@client.event 
async def on_ready():
    print('we have logged in as a {0.user}'.format(client))
@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return

    if msg.startswith('$getStats'):
        msg = message.content[9:]
        output = get_stats(msg)
        await message.channel.send(output)
    elif msg.startswith('$addFeature'):
        msg = msg[12:]
        msg = msg.split(',')
        output = add_feature(msg[0], msg[1])
        await message.channel.send(output)
    elif msg.startswith('$addItem'):
        msg = msg[9:]
        msg = msg.split(',')
        if(len(msg) == 4):
            output = add_new_item(msg[0],msg[1],msg[2],msg[3])
        else:
            output = add_new_item(msg[0], msg[1], msg[2])
        await message.channel.send(output)
    elif msg.startswith('$addSpell'):
        msg = msg[10:]
        msg = msg.split(',')
        output = add_spell(msg[0], msg[1])
        await message.channel.send(output)
    elif msg.startswith('$addSlots'):
        msg = msg[10:]
        msg = msg.split(',')
        output = add_slots(msg[0],msg[1],msg[2])
        await message.channel.send(output)
    elif msg.startswith('$useItem'):
        msg = msg[9:]

client.run(DISCORD TOKEN)