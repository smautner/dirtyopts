import re
import sys

doc='''
i guess we write stuff like so:
NAMEOFTHING [TYPE] [default: DEFAULT]  [DOUBLESPACE DESCRIPTION]

--myintarg int default:12   blabla
--something    we will assume that it is a bool i think
--mystring str default:asd  blabla
--myfu eval default: lambda x:x 
'''

#REGEX:
#0:name
#1:type
#2: NOTHIG
#3:defaultvalue
getgroups = re.compile( '--([\w]+) ?([\w]+)? ?(default:(.+))? ?')

def docstrparser(docstring):
    args={}
    argfun={}
    for line in docstring.split('\n'):
        line= line.strip()
        if line and line[:2]=='--':
            line = line.split("  ")[0]
            m=getgroups.match(line)
            #print('grps',m.group(1),m.group(2),m.group(4))
            # lets read the groups 
            name = m.group(1)
            argfun[name] = eval(m.group(2)) if m.group(2) else bool # set type
            args[name] = argfun[name](m.group(4))   # bool(None) is false so this is fine

    return args, argfun


def argparser(args):
    '''
    returns {arg:string}
    '''
    result = {}
    carg = None
    cstuff = ''
    for e in args:
        if e[0]== '-':
            if carg:
                result[carg] = cstuff.strip()
                cstuff = ''
            carg = e[2:]
        else:
            cstuff+=e
    if carg:result[carg] = cstuff.strip()
    return result

class argz:
    def __init__(self,stuff):
        self.__dict__.update(stuff)

def parse( docstring , args =  sys.argv[1:]):
    defaultargs, argfun = docstrparser(docstring)
    rawargs = argparser(args)

    for arg,v in rawargs.items():
        
        if arg in defaultargs:
            if v == '':
                defaultargs[arg] = True
            elif k in argfun:
                defaultargs[arg] = argfun[arg](v)


    return argz(resargs)

if __name__ == '__main__':
    print(parse(doc).__dict__)
