import os, sys, time, colorama, random, pickle, re
colorama.init()

from constants import *
from console_commands import *
from bot_commands import *

import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    return

    while True:
        query = input("\n> ")
        parts = query.split(' ')
        if (parts[0] in commands):
            command = commands[parts.pop(0)]
        else:
            command = cmd_dir

        if command == cmd_quit:
            break

        if parts:
            arg = parts.pop(0)
        else:
            continue

        path = arg.split('.')
        node = guild
        if path[0] == 'guild' or path[0] == '':
            path.pop(0)

        try:
            for step in path:
                if step:
                    node = getattr(node, step)
        except Exception as e:
            print("Error in path")

        command(node, parts)

    await client.logout()
    time.sleep(0.5)



#die = {
#    1: '⚀'.lower(),
#    2: '⚁'.lower(),
#    3: '⚂'.lower(),
#    4: '⚃'.lower(),
#    5: '⚄'.lower(),
#    6: '⚅'.lower(),
#}

die = {
    1: '<:d1:780649001623617592>',
    2: '<:d2:780649001455452170>',
    3: '<:d3:780649001506570250>',
    4: '<:d4:780649001686138881>',
    5: '<:d5:780649001409708043>',
    6: '<:d6:780649001690595338>',
}

coins = [
    '<:c1:780661517975814194>',
    '<:c2:780661518521597952>',
    '<:c3:780661519171715083>',
    '<:c4:780661519553265664>',
    '<:c5:780661519721562113>',
    '<:c6:780661518785052703>',
    '<:c7:780661519213396009>',
    '<:c8:780661519381692436>',
    '<:c9:780661519767175188>',
]

roll_re = re.compile('^r[0-9]{1,2}')
debugging = set()

version = 1

class Options():
    def __init__(self):
        self.version = version
        self.roll_interval = 0.3
        self.roll_times = 6
        self.nicknames = {}
        self.roll_react = True
        # increase version when adding!

option_file = 'options.cfg'

def save_options():
    pickle.dump(options, open(option_file, 'wb'))

def load_options():
    return pickle.load(open(option_file, 'rb'))

try:
    options = load_options()
except Exception:
    options = Options()

if options.version < version:
    old_options = options
    options = Options()
    for k in dir(old_options):
        if k.startswith('_'): continue
        setattr(options, k, getattr(old_options, k))

def get_name(name):
    if name in options.nicknames:
        return options.nicknames[name]
    else:
        return name


def cast(t, v):
    if t == int:
        return int(v)
    elif t == float:
        return float(v)
    elif t == bool:
        v = v.lower()
        if v == "true" or v == "t":
            return True
        elif v == "false" or v == "f":
            return False
        return bool(v)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    args = [x for x in message.content.split(' ') if x]

    if args:
        command = args.pop(0).lower()

    try:
        if roll_re.match(command):
            if len(command) == 3:
                args = [command[1], command[2]]
            else:
                args = [command[1]]
            command = 'r'

        if command == 'r' or command == 'roll':
            dice = int(args[0])
            if len(args) > 1:
                tn = int(args[1])
            else:
                tn = None


            name = get_name(message.author.name)
            def roll_message(count, target, sorted = False):
                result = []
                hits = 0
                ones = 0
                for i in range(dice):
                    n = random.randint(1, 6)
                    result.append(n)
                    if n == 1:
                        ones += 1
                    elif n == 5:
                        hits += 1
                    elif n == 6:
                        hits += 2
                if sorted:
                    result.sort()
                return name + ': ' + ' '.join((die[x] for x in result)), hits, ones

            if options.roll_times <= 1:
                msg, hits, ones = roll_message(dice, tn, True)
                await message.channel.send(msg)
            else:
                msg, _, _ = roll_message(dice, tn)
                roll = await message.channel.send(msg)
                for i in range(options.roll_times - 2):
                    time.sleep(options.roll_interval)
                    msg, _, _ = roll_message(dice, tn)
                    await roll.edit(content=msg)
                time.sleep(options.roll_interval)
                msg, hits, ones = roll_message(dice, tn, True)
                await roll.edit(content=msg)

            if not options.roll_react: return

            if tn is None:
                await roll.add_reaction('🆗')
            elif hits >= tn:
                await roll.add_reaction('✅')
            else:
                await roll.add_reaction('🛑')

            if tn is not None and hits > tn:
                benefits = min(hits - tn, 9)
                for i in range(benefits):
                    await roll.add_reaction(coins[i])

            if ones >= dice / 2:
                if tn is None or hits < tn:
                    await roll.add_reaction('💀')
                else:
                    await roll.add_reaction('💩')


        elif command == 'config':
            if not args:
                config = []
                for k in sorted(dir(options)):
                    if not k.startswith("_"):
                        config.append(f'{k} = {getattr(options, k)}')
                await dm(message.author, 'Current config:\n' + '\n'.join(config))
                return

            while args:
                k = args.pop(0)
                v = args.pop(0)
                option = getattr(options, k, None)
                if option is not None:
                    setattr(options, k, cast(type(option), v))
            save_options()

        elif command == 'alias':
            name = ' '.join(args)
            options.nicknames[message.author.name] = name
            response = f'{message.author.name} will be known as {name}'
            await message.channel.send(response)
            save_options();

        elif command == 'debug':
            debugging.add(message.author.name)
            await dm(message.author, "Debugging turned ON")

        elif command == 'nodebug':
            debugging.remove(message.author.name)
            await dm(message.author, "Debugging turned OFF")

        else:
            return

    except Exception as e:
        member = message.author
        if member.name in debugging:
            await dm(member, "Sorry, I don't understand.  Type `nodebug` to turn off these messages.")
        print()
        print(str(e))
        print()


async def dm(member, message):
    if member.name:
        await member.create_dm()
        await member.dm_channel.send(message)

client.run(TOKEN)
