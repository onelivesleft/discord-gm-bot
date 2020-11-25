import os, sys, time, colorama, random, pickle
colorama.init()

from constants import *
from console_commands import *

import discord
from dotenv import load_dotenv


option_version = 4

class Options():
    def __init__(self):
        self.version = option_version
        self.roll_interval = 0.3
        self.roll_times = 6
        self.nicknames = {}
        self.roll_react = True
        self.debugging = set()
        self.icon_rolled       = '🎲'
        self.icon_success      = '✅'
        self.icon_failed       = '❌'
        self.icon_catastrophe  = '💀'
        self.icon_setback      = '💩'
        # increase version when adding!

hidden_options = set(['debugging', 'nicknames', 'version'])

option_file = 'options.cfg'

def save_options():
    pickle.dump(options, open(option_file, 'wb'))

def load_options():
    return pickle.load(open(option_file, 'rb'))

try:
    options = load_options()
except Exception:
    options = Options()

if options.version < option_version:
    old_options = options
    options = Options()
    for k in dir(old_options):
        if k.startswith('_'): continue
        setattr(options, k, getattr(old_options, k))


def get_name(name):
    if name in options.nicknames:
        return f'`{options.nicknames[name]}`'
    else:
        return f'`{name}`'


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
    else: #string
        return v


commands = {}
aliases = {}
command_help = {}

def register(name, alias, help_text):
    def wrap(f):
        commands[name] = f
        command_help[name] = help_text
        if alias is not None:
            aliases[alias] = name
        return f
    return wrap


@register('roll', 'r', '<pool> [<tn>] OR rX[Y] where X and Y are single digit <pool> and <tn>')
async def roll(message, *args):
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
        await roll.add_reaction(options.icon_rolled)
    elif hits >= tn:
        await roll.add_reaction(options.icon_success)
    else:
        await roll.add_reaction(options.icon_failed)

    if tn is not None and hits > tn:
        benefits = min(hits - tn, 9)
        for i in range(benefits):
            await roll.add_reaction(coins[i])

    if ones >= dice / 2:
        if tn is None or hits < tn:
            await roll.add_reaction(options.icon_catastrophe)
        else:
            await roll.add_reaction(options.icon_setback)


@register('config', None, '[<setting> <value>...] sets config options, or use without args to display.')
async def config(message, *args):
    if not args:
        config = []
        for k in sorted(dir(options)):
            if not k.startswith("_") and k not in hidden_options:
                label = k + ':'
                config.append(f'{label.ljust(20)}{getattr(options, k)}')
        await dm(message.author, '```\n' + '\n'.join(config) + '```')
        return

    args = list(args)
    e = Exception()
    output = []
    while args:
        k = args.pop(0)
        try:
            v = args.pop(0)
        except Exception:
            output.append('Missing value')
            break
        option = getattr(options, k, e)
        label = k + ':'
        if option is not e and k not in hidden_options:
            setattr(options, k, cast(type(option), v))
            output.append(f'{label.ljust(20)}{getattr(options, k)}')
        else:
            output.append(f'{label.ljust(20)}No such option')
    await dm(message.author, '```\n' + '\n'.join(output) + '```')
    save_options()


@register('reset', None, '<setting>...  resets config option to default value.')
async def reset(message, *args):
    defaults = Options()
    e = Exception()
    output = []
    for k in args:
        default = getattr(defaults, k, e)
        label = k + ':'
        if default is not e and k not in hidden_options:
            setattr(options, k, default)
            output.append(f'{label.ljust(20)}{getattr(options, k)}')
        else:
            output.append(f'{label.ljust(20)}No such option')
    await dm(message.author, '```\n' + '\n'.join(output) + '```')
    save_options()


@register('alias', None, '<name> : GM will call you by this name')
async def alias(message, *args):
    name = ' '.join(args)
    if name.replace(' ', '') == '':
        people = []
        for k in options.nicknames:
            label = k + ':'
            people.append(f'{label.ljust(20)}{options.nicknames[k]}')
        response = '```\n' +  '\n'.join(people) + '```'
    else:
        options.nicknames[message.author.name] = name
        response = f'{message.author.name} will be known as `{name}`'
    await message.channel.send(response)
    save_options();


@register('alias-off', None, 'Remove your alias')
async def noalias(message, *args):
    if message.author.name in options.nicknames:
        del(options.nicknames[message.author.name])
    response = f'{message.author.name} will be known as `{message.author.name}`'
    await message.channel.send(response)
    save_options();


@register('debug', None, 'Turn on debugging, GM will DM you error messages')
async def debug(message, *args):
    options.debugging.add(message.author.name)
    await dm(message.author, "Debugging turned ON")


@register('debug-off', None, 'Turn off debug messages')
async def nodebug(message, *args):
    options.debugging.remove(message.author.name)
    await dm(message.author, "Debugging turned OFF")


@register('help', '?', 'Display help')
async def help_cmd(message, *args):
    help_text = ['```']
    for name in sorted(commands):
        help_text.append(f'{name.ljust(10)}{command_help[name]}')
    help_text.append('```')
    await dm(message.author, '\n'.join(help_text))


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

    """while True:
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
"""


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
            command = 'roll'

        if command in aliases:
            command = aliases[command]

        if command in commands:
            await commands[command](message, *args)

    except Exception as e:
        member = message.author
        if member.name in options.debugging:
            await dm(member, f"Error:\n {str(e)}")


async def dm(member, message):
    if member.name:
        await member.create_dm()
        await member.dm_channel.send(message)


client.run(TOKEN)
