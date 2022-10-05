#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from widget import KeyboardOSK

import os
import sys
import fcntl
import subprocess
fh=0
#https://stackoverflow.com/questions/380870/make-sure-only-a-single-instance-of-a-program-is-running
def run_once():
    global fh
    fh=open(os.path.realpath(__file__),'r')
    try:
        fcntl.flock(fh,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except:
        print("Process already running.")
        os._exit(0)

lang=subprocess.getoutput("setxkbmap -query | grep layout").split(":")[-1].strip().split(",")[0]
variant=subprocess.getoutput("setxkbmap -query | grep variant").split(":")[-1].strip().split(",")[0]


run_once()
# Window features
w = Gtk.Window()
w.set_opacity(1.0)
w.set_accept_focus(False)
#w.set_deletable(False)
w.set_keep_above(True)
#w.set_skip_taskbar_hint(True)
#w.set_skip_pager_hint(True)
# Exit event
def exit_event(widget=None):
    global w
    f = open("{}/.osk".format(os.environ["HOME"]),"w")
    height, width = w.get_size()
    x, y = w.get_position()
    f.write("{}:{}:{}:{}".format(height,width,x,y))
    f.flush()
    f.close()
    Gtk.main_quit()
# Restore position
if os.path.isfile("{}/.osk".format(os.environ["HOME"])):
    try:
        f = open("{}/.osk".format(os.environ["HOME"]),"r")
        o = f.read().split(":")
        if len(o) == 4:
            x = int(o[2])
            y = int(o[3])
            if x != 0 or y != 0:
                w.move(x, y)
            w.resize(int(o[0]),int(o[1]))
    except:
        pass
# Headerbar
hb = Gtk.HeaderBar()
exit = Gtk.Button()
exit.set_label(" ✖ ")
exit.set_name("key_normal")
exit.connect("clicked",exit_event)
w.connect("destroy",exit_event)
hb.pack_end(exit)
# OSK widget
osk = KeyboardOSK(embeded=False,nocreate=True)
osk.update(lang,variant)
osk.create_layout(False)
layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
# Integrate osk with window
if "--no-fx" in sys.argv:
    hb.set_custom_title(osk.l[1])
    w.set_titlebar(hb)
elif "--no-headerbar" in sys.argv:
    layout.pack_start(osk.l[0], 1, True, True)
    layout.pack_start(osk.l[1], 1, True, True)
    w.set_title("")
else:
    hb.set_custom_title(osk.l[0])
    w.set_titlebar(hb)
    layout.pack_start(osk.l[1], 1, True, True)
hb.pack_start(Gtk.Label(label="    "))
layout.pack_start(osk.l[2], 1, True, True)
layout.pack_start(osk.l[3], 1, True, True)
layout.pack_start(osk.l[4], 1, True, True)
layout.pack_start(osk.l[5], 1, True, True)
# Show window
w.add(layout)
w.show_all()
# css
screen = Gdk.Screen.get_default()
css = """
window, button, headerbar {
    outline-style: none;
    border: 1px solid black;
    background: #000;
}"""

gtk_provider = Gtk.CssProvider()
gtk_context = Gtk.StyleContext()
gtk_context.add_provider_for_screen(
screen, gtk_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
gtk_provider.load_from_data(css.encode("UTF-8"))
osk.style()
Gtk.main()
