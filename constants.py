
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
