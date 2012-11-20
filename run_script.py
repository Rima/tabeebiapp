import sys, os

def import_module(name, package=None):
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)

#    name = name.rstrip('.py')
    __import__(name)

current_path = os.getcwd()
sys.path += [current_path]

from optparse import OptionParser

def checkArgs():
    parser = OptionParser()
    parser.add_option(
        '-s','--script',
        dest='script',
        action='store',
        type='string',
        help='This script sets the local sys.path to be the local current path so that we can run cronjobs and migration scripts.'
    )

    (options, args) = parser.parse_args()
    return vars(options)

options = checkArgs()
print options
import_module(options['script'])

