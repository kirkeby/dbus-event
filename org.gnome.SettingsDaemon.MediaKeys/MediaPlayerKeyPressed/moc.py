'Integration between MOC and Gnome media-playback keys.'

import os

commands = {
    'Play': 'mocp --toggle-pause',
    'Next': 'mocp --next',
}

def callback(application, key):
    cmd = commands.get(key)
    if cmd:
        os.system(cmd)
