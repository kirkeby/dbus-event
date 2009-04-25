#!/usr/bin/env python

import logging
from daemon import daemonize
from glob import glob
import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop

def load_callbacks():
    paths = glob('*/*/*.py')
    for path in paths:
        source, event, filename = path.split('/')

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
    logging.basicConfig(level=0, filename='dbus_events.log')
    logging.getLogger().setLevel(0)
    main()
