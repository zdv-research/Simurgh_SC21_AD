
categories = ["jmpp", "retp"]

microcode = '''
# Microcode for general purpose instructions
'''
for category in categories:
    exec("from . import %s as cat" % category)
    microcode += cat.microcode
