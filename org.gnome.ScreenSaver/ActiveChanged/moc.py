'Pause MOC playback when screensaver is activated.'

import os
from commands import getoutput

we_paused_mytunes = False

def get_moc_info():
    return dict(line.split(': ', 1)
                for line in getoutput('mocp --info').split('\n')
                if ': ' in line)

def callback(is_it_really):
    global we_paused_mytunes
    if is_it_really:
        moc_info = get_moc_info()
        we_paused_mytunes = moc_info.get('State') == 'PLAY'
        if we_paused_mytunes:
            os.system('mocp --pause')
    elif we_paused_mytunes:
        os.system('mocp --unpause')
