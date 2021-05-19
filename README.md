
# Usage:

```
from dirtyopts import parse

doc = '''
#--argname type[+ for list] [default]  [doublespace -> comment]
--intarg int+ 3 4 5  i am a comment

# nodefault means the default of the type 
--strarg str  ->''

# you need to provide a string for bool arguments because where is no special treatment for them
>>>myprog --boolarg True   
'''

doc2 = '''
# i ignore unknown args so multiple args opbjects can be created neatly
--intargford2 int
'''

args = parse(doc)
args2 = parse(doc2)
```

