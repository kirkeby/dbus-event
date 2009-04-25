import os
from commands import getoutput

mytunes_remote = '/home/sune/mytunes/mytunes-remote'
we_paused_mytunes = False

def callback(is_it_really):
    global we_paused_mytunes
    if is_it_really:
        status = getoutput('%s status' % mytunes_remote)
        we_paused_mytunes = '[play]' in status
        if we_paused_mytunes:
            os.system('%s pause' % mytunes_remote)
    elif we_paused_mytunes:
        os.system('%s play' % mytunes_remote)
