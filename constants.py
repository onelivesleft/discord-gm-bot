import re

RESET_COLOR = '\033[m'

BLACK   = '\033[0;30m'
RED     = '\033[0;31m'
GREEN   = '\033[0;32m'
YELLOW  = '\033[0;33m'
BLUE    = '\033[0;34m'
MAGENTA = '\033[0;35m'
CYAN    = '\033[0;36m'
WHITE   = '\033[0;37m'

BRIGHT_BLACK   = GREY = '\033[1;30m'
BRIGHT_RED     = '\033[1;31m'
BRIGHT_GREEN   = '\033[1;32m'
BRIGHT_YELLOW  = '\033[1;33m'
BRIGHT_BLUE    = '\033[1;34m'
BRIGHT_MAGENTA = '\033[1;35m'
BRIGHT_CYAN    = '\033[1;36m'
BRIGHT_WHITE   = '\033[1;37m'

BLACK_BACKGROUND   = '\033[40m'
RED_BACKGROUND     = '\033[41m'
GREEN_BACKGROUND   = '\033[42m'
YELLOW_BACKGROUND  = '\033[43m'
BLUE_BACKGROUND    = '\033[44m'
MAGENTA_BACKGROUND = '\033[45m'
CYAN_BACKGROUND    = '\033[46m'
WHITE_BACKGROUND   = '\033[47m'

def __foo():
    pass
function = type(__foo)

class __Foo():
    def foo(self):
        pass
__foo = __Foo()

method = type(__foo.foo)


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

roll_re = re.compile('^r[0-9]{1,3}$')
autoroll_quick_re  = re.compile('^[0-9]{1,3}$')
autoroll_re = re.compile('^[0-9]+(\s+[0-9]+)?(\s+[0-9]+)?$')
