
# Install:

```
pip install dirtyopts
```

# Usage:

```
from dirtyopts import parse

doc = '''
#--NAMEOFTHING TYPE[+ for list] [DEFAULT] [assert ALLOWED VALUES]  [comment after 2 spaces :)]
--intarg int+ 3 4 5  i am a comment
--mystring str be assert mystring musst be one of these

# no default value means the default of the type
--strarg str  ->''


'''

other_behaviour = '''
# you can parse the args with multiple doc strings, as unknown args are ignored
--intarg2 int

# -h and --help will print this string

# giving w1 as first arg will trigger verbose mode for the parsing

# you need to provide a string for bool arguments because where is no special treatment for them
>>>myprog --boolarg True
'''

args = parse(doc)
args2 = parse(other_behaviour)
```

