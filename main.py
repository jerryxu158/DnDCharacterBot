from queue import Empty
import pyodbc
import discord
#https://github.com/mkleehammer/pyodbc/wiki

cnxn = pyodbc.connect(CONNECTION STRING)
crsr = cnxn.cursor()

intents = discord.Intents.default()
intents.message_content = True

def splitByComma(message):
    message = message[message.find(' ') + 1:]
    message = message.split(', ')
    print(message)
    return message

def get_stats(user):
    crsr.execute("{CALL getStats (?)}", user)
    rows = crsr.fetchall()

    print(rows)
    if(rows[0][0] == 'does not exist'):
        return user + " does not exist"
    
    return rows

def add_feature(user, feature):
    params = (user, feature)
    crsr.execute("{CALL add_feature (?,?)}", params)
    cnxn.commit()
    
    return "feature successfully added"

def add_new_item(user, item, quantity, weight = None):
    params = (user, item, quantity, weight)
    crsr.execute("{CALL add_new_item (?,?,?,?)}", params)
    cnxn.commit()

    return 'added new item'

def add_spell(user, spell):
    params = (user, spell)
    crsr.execute("{CALL add_spell(?,?)}", params)
    cnxn.commit()

    return 'added spell'

def add_slots(user, level, quant):
    params = (user, level, quant)
    crsr.execute("{CALL add_SpellSlots(?,?,?)}", params)
    cnxn.commit()

    return 'added spell slots'

def use_item(user, item, quantity):
    params = (item, user, quantity)
    crsr.execute("{CALL decrement_item(?,?,?)}", params)
    
    out = crsr.fetchall()
    cnxn.commit()
    for rows in out:
        print(out)
    #out = list. out[0] = pyodbc row out[0][0] = first column of first row
    if(out[0][0] == 'insufficient quantity'):
        return 'insufficient quantity in inventory'
    elif(out[0][0] == 'does not exist'):
        return 'You do not have this item'
    else:
        return 'used ' + quantity + ' ' + item

def get_inventory(user):
    crsr.execute("{CALL get_items(?)}", user)
    rows = crsr.fetchall()
    cnxn.commit()
    return rows

def get_spells(user):
    crsr.execute("{CALL getPlayerSpells(?)}", user)
    rows = crsr.fetchall()
    cnxn.commit()
    return rows

def get_spellcasting(user):
    crsr.execute("{CALL getSpellCasting(?)}", user)
    rows = crsr.fetchall()
    cnxn.commit()
    return rows

def add_item(user, item, quantity):
    params = (item, user, quantity)
    crsr.execute("{CALL increment_item (?,?,?)}", params)
    cnxn.commit()
    return 'added item'

def new_char(character, person):
    params = (character, person)
    crsr.execute("{CALL newCharacter(?,?)}", params)
    rows = crsr.fetchall()
    cnxn.commit()
    if(rows[0][0] == 'success'):
        return character + ' added to database'
    else:
        return 'a character with that name already exists'

def set_char(user, quantity):
    params = (user, quantity)
    crsr.execute("{CALL set_chr(?,?)}", params)
    cnxn.commit()
    return 'charisma set to ' + quantity

def set_const(user, quantity):
    params = (user, quantity)
    crsr.execute("{CALL set_const(?,?)}", params)
    cnxn.commit()
    return 'constitution set to ' + quantity

def set_dex(user, quantity):
    params = (user, quantity)
    crsr.execute("{CALL set_dex(?,?)}", params)
    cnxn.commit()
    return 'Dexterity set to ' + quantity

def set_hp(user, quantity):
    params = (user, quantity)
    crsr.execute("{CALL set_hp(?,?)}", params)
    cnxn.commit()
    return 'Max hp set to ' + quantity

def set_int(user, quantity):
    params = (user, quantity)
    crsr.execute("{CALL set_int(?,?)}", params)
    cnxn.commit()
    return 'Inteligence set to ' + quantity

def set_str(user, quantity):
    params = (user, quantity)
    crsr.execute("{CALL set_str(?,?)}", params)
    cnxn.commit()
    return 'Strength set to ' + quantity

def set_wis(user, quantity):
    params = (user, quantity)
    crsr.execute("{CALL set_wis(?,?)}", params)
    cnxn.commit()
    return 'Wisdom set to ' + quantity

def set_spellSlots(user, level, quantity):
    params = (user, level, quantity)
    crsr.execute("{CALL setSpellSlots(?,?,?)}", params)
    cnxn.commit()
    return 'Added ' + quantity + ' spell slots of level ' + level

def use_spell(user, spell, level):
    params = (user, spell, level)
    crsr.execute("{CALl useSpell(?,?,?)}", params)
    cnxn.commit()
    return 'used ' + spell + ' at level ' + level

def long_rest(user):
    crsr.execute("{CALl longRest(?)}", user)
    cnxn.commit()

    rows = crsr.fetchall()

    if(rows[0][0] != 'success'):
        return 'something went wrong. Please check the spelling of the character'
    else:
        return 'long rest complete'

client = discord.Client(intents=intents)

@client.event 
async def on_ready():
    print('we have logged in as a {0.user}'.format(client))
@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return

    if msg.startswith('$hello'):
        output = splitByComma(msg)
        await message.channel.send(output)

    elif msg.startswith('$addFeature'):
        msg = splitByComma(msg)
        output = add_feature(msg[0], msg[1])
        await message.channel.send(output)

    elif msg.startswith('$newItem'):
        msg = splitByComma(msg)
        if(len(msg) == 4):
            output = add_new_item(msg[0],msg[1],msg[2],msg[3])
        else:
            output = add_new_item(msg[0], msg[1], msg[2])
        await message.channel.send(output)

    elif msg.startswith('$addSpell'):
        msg = splitByComma(msg)
        output = add_spell(msg[0], msg[1])
        await message.channel.send(output)

    elif msg.startswith('$addSlots'):
        msg = splitByComma(msg)
        output = add_slots(msg[0],msg[1],msg[2])
        await message.channel.send(output)

    elif msg.startswith('$useItem'):
        msg = splitByComma(msg)
        output = use_item(msg[0], msg[1], msg[2])
        await message.channel.send(output)
        
    elif msg.startswith('$getInventory'):
        msg = splitByComma(msg)
        output = get_inventory(msg[0])
        await message.channel.send(output)

    elif msg.startswith('$getSpells'):
        msg = splitByComma(msg)
        output = get_spells(msg[0])
        await message.channel.send(output)

    elif msg.startswith('$getSpellCasting'):
        msg = splitByComma(msg)
        output = get_spellcasting(msg[0])
        await message.channel.send(output)

    elif msg.startswith('$getStats'):
        msg = splitByComma(msg)
        output = get_stats(msg[0])
        await message.channel.send(output)

    elif msg.startswith('$addItem'):
        msg = splitByComma(msg)
        output = add_item(msg[0], msg[1], msg[2])
        await message.channel.send(output)
    
    elif msg.startswith('$newChar'):
        msg = splitByComma(msg)
        output = new_char(msg[0], msg[1])
        await message.channel.send(output)

    elif msg.startswith('$setChr'):
        msg = splitByComma(msg)
        output = set_char(msg[0], msg[1])
        await message.channel.send(output)

    elif msg.startswith('$setConst'):
        msg = splitByComma(msg)
        output = set_const(msg[0], msg[1])
        await message.channel.send(output)

    elif msg.startswith('$setDex'):
        msg = splitByComma(msg)
        output = set_dex(msg[0], msg[1])
        await message.channel.send(output)
    
    elif msg.startswith('$setHp'):
        msg = splitByComma(msg)
        output = set_hp(msg[0], msg[1])
        await message.channel.send(output)

    elif msg.startswith('$setInt'):
        msg = splitByComma(msg)
        output = set_int(msg[0], msg[1])
        await message.channel.send(output)

    elif msg.startswith('$setStr'):
        msg = splitByComma(msg)
        output = set_str(msg[0], msg[1])
        await message.channel.send(output)

    elif msg.startswith('$setWis'):
        msg = splitByComma(msg)
        output = set_wis(msg[0], msg[1])
        await message.channel.send(output)

    elif msg.startswith('$setSpellslots'):
        msg = splitByComma(msg)
        output = set_spellSlots(msg[0], msg[1], msg[2])
        await message.channel.send(output)

    elif msg.startswith('$useSpell'):
        msg = splitByComma(msg)
        output = use_spell(msg[0], msg[1], msg[2])
        await message.channel.send(output)
    
    elif msg.startswith('$longRest'):
        msg = splitByComma(msg)
        output = long_rest(msg[0])
        await message.channel.send(output)

client.run(TOKEN)