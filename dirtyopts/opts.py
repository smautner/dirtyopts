import re
import sys
import logging
doc='''
i guess we write stuff like so:
NAMEOFTHING [TYPE] [DEFAULT] [assert ALLOWED VALUES]  [DOUBLESPACE DESCRIPTION]

--myintarg int 12   comment
--mystring str asd  blabla
--mystring2 str asd assert asd asdf  comment
--myfu eval lambda x:x.max()
--another bool True
--zomg int+
--anotherf bool+ False False

#--help and -h are SPECIAL NOW :) 
#w1 at the beginning triggers debug mode
'''




######################
# READ THE DOCSTRING 
####################
#NEW REGEX
# 1:argname, 2:type 3:+ 4: default
getgroups = re.compile('--([\w]+) (\w+)(\+)? ?(.+)?')

def interpret_groups(argname, maker, islist, default, defaults, funcs, ass = []):

    # bool("False") is True, so we need this:
    makerf = eval(maker) if maker != 'bool' else boolbuilder

    
    if maker == 'eval': 
        funcs[argname] = lambda x: eval(" ".join(x))
        assert not ass, f'can not define value list here, change  dirtyopts for {argname}'
    elif islist:
        funcs[argname]  = lambda x: list(map(makerf,x))
        assert not ass, f'can not define value list for list, change dirtyops for {argname}'
    else:
        func = lambda x: makerf(x[0])
        funcs[argname]  = func if not ass else lambda z: checkass(ass,func,z, argname)
    


    if default:
        defaults[argname] = funcs[argname](default.split())  
    else:
        defaults[argname] = makerf() if not islist else [makerf()]


def checkass(ass,func,z, arg):
    assert z[0] in ass, f"invalid argument \"{z[0]}\" for  argument {arg}"
    return func(z)

def boolbuilder(x=None):
    if x in [None,'False']:
        return False
    if x in ["True"]:
        return True
    assert False, f"i dont know how to turn {x} into a bool"
        
    

def docstrparser(docstring, debug):
    defaults={}
    argfun={}
    for line in docstring.split('\n'):
        line= line.strip()
        if line and line[:2]=='--':
            line = line.split("  ")[0]

            line = line.split(" assert ")
            ass = line[1] if len(line) > 1 else []

            m=getgroups.match(line[0])
            matched = [m.group(x) for x in [1,2,3,4]]
            if debug: 
                print ("matches:", matched)
            
            interpret_groups(*matched, defaults, argfun,ass)
            if debug: 
                print ("default:", defaults[matched[0]] )
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

def argparser(args, debug):
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
    if debug:
        print(args)
        print(result)
    return result



############3
# READ THE ARGS
#############
class argz:
    def __init__(self,stuff):
        self.__dict__.update(stuff)


def parse(docstring , args =  sys.argv[1:], debug=False):
    if "-h" in args or "--help" in args:
        print (docstring)
    if args and args[0] == 'w1':
        debug = True
        args = args[1:]

    
    rawargs = argparser(args, debug)
    defaultargs, argfun = docstrparser(docstring, debug)

    for arg,v in rawargs.items():
        if arg not in argfun:
            if debug: logging.warning(f"this docstring doesnt handle: {arg}")
        else:
            assert v , f'given arg: "{arg}" is {v}  you musst give an explicit value!' 
            defaultargs[arg] = argfun[arg](v)
            if debug: print (f"overwritining {arg}  got:{v}  ->: {defaultargs[arg]}")

    return argz(defaultargs)

if __name__ == '__main__':
    print(parse(doc).__dict__)

