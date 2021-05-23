import re
import sys
import logging
doc='''
i guess we write stuff like so:
NAMEOFTHING [TYPE] [default: DEFAULT]  [DOUBLESPACE DESCRIPTION]

--myintarg int 12   blabla
--mystring str asd  blabla
--myfu eval lambda x:x 
--another bool True
--zomg int+
--anotherf bool+ False False


#--help and -h are SPECIAL NOW :) 
'''




######################
# READ THE DOCSTRING 
####################


#REGEX:
#1:name #2:type #3:list?  #4: NOTHIG #5:defaultvalue
#getgroups = re.compile( '--([\w]+) ?(\w+)?(\+)? ?(default:(.+))? ?')

#NEW REGEX
# 1:argname, 2:type 3:+ 4: default
getgroups = re.compile('--([\w]+) (\w+)(\+)? ?(.+)?')

def interpret_groups(argname, maker, islist, default, defaults, funcs):
    if maker == 'bool':
        makerf=lambda x: x=='True'
    else:
        makerf=eval(maker)

    if maker == 'eval': 
        funcs[argname] = lambda x: eval(" ".join(x))
    elif islist:
        funcs[argname]  = lambda x: list(map(makerf,x))
    else:
        funcs[argname]  = lambda x: makerf(x[0])
    
    if default:
        defaults[argname] = funcs[argname](default.split())  
    else:
        defaults[argname] = makerf() if not islist else [makerf()]




def docstrparser(docstring):
    defaults={}
    argfun={}
    for line in docstring.split('\n'):
        line= line.strip()
        if line and line[:2]=='--':
            line = line.split("  ")[0]
            m=getgroups.match(line)
            interpret_groups(*[m.group(x) for x in [1,2,3,4]], defaults, argfun)
    # bool(None) is false so this is fine
    return defaults, argfun


##############
#  READ THE ARGS
#############
def app(res,carg,cstuff):
    if not cstuff:
        logging.warning(f'arg missing: {carg}')
    res[carg] = cstuff
    return []

def argparser(args):
    '''
    returns {argname:list}
    '''
    result = {}
    carg = None
    cstuff = []
    for e in args:
        if e[:2]== '--':
            if carg:
                cstuff = app(result,carg, cstuff)
            carg = e[2:]
        else:
            cstuff.append(e)
    if carg:
        cstuff = app(result,carg, cstuff)
    return result



############3
# READ THE ARGS
#############
class argz:
    def __init__(self,stuff):
        self.__dict__.update(stuff)


def parse(docstring , args =  sys.argv[1:]):
    if "-h" in args or "--help" in args:
        print (docstring)
    rawargs = argparser(args)
    defaultargs, argfun = docstrparser(docstring)
    for arg,v in rawargs.items():
        if arg not in argfun:
            logging.warning(f"this docstring doesnt handle: {arg}")
        else:
            defaultargs[arg] = argfun[arg](v)

    return argz(defaultargs)

if __name__ == '__main__':
    print(parse(doc).__dict__)

