#!/usr/bin/env python

import os
import logging
from daemon import basic_daemonize as daemonize
from glob import glob
import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop

here = os.path.dirname(__file__)

def load_callbacks():
    paths = glob(os.path.join(here, '*', '*', '*.py'))
    for path in paths:
        source, event = path.split(os.path.sep)[-3:-1]

        py_source = open(path).read()
        code = compile(py_source, path, 'exec')
        module_globals = {}
        eval(code, module_globals)
        callback = module_globals['callback']

        yield source, event, callback

def main():
    DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    for source, event, callback in load_callbacks():
        session_bus.add_signal_receiver(callback, event, source)

    loop = gobject.MainLoop()
    daemonize()
    loop.run()

if __name__ == '__main__':
    logfile = os.path.join(here, 'dbus_events.log')
    logging.basicConfig(level=0, filename=logfile)
    logging.getLogger().setLevel(0)
    main()
