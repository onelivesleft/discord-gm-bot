from constants import *

def cmd_type(node):
    print(YELLOW + str(type(node)) + RESET_COLOR)


def cmd_dir(node, args):
    if type(node) == method:
        try:
            print(node(*args))
        except Exception as e:
            print(str(e))
        return
    elif type(node) == type([]):
        print(YELLOW + str(type([])) + RESET_COLOR)
        return

    parts = []
    for member in dir(node):
        if member.startswith('_'): continue
        obj = getattr(node, member)
        if type(obj) == method:
            prefix = BRIGHT_GREEN
        elif obj is None:
            prefix = BLUE
        else:
            prefix = WHITE
        parts.append(f'{prefix}{member.ljust(29)}{RESET_COLOR}')
        if len(parts) == 3:
            print(''.join(parts))
            parts.clear()

    if parts:
        print(''.join(parts))


def cmd_print(node):
    if type(node) == list:
        for item in node:
            print(item)
    else:
        print(str(node))

def cmd_quit():
    pass


commands = {
    'dir':  cmd_dir,
    'print': cmd_print,
    'type': cmd_type,
    'quit': cmd_quit,
}

aliases = {
    'd': 'dir',
    'p': 'print',
    't': 'type',
    'q': 'quit',
}


for alias in aliases:
    commands[alias] = commands[aliases[alias]]
