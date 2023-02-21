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

os.chdir(os.path.dirname(os.path.abspath(__file__)))
run_once()
# Window features
w = Gtk.Window()
w.set_accept_focus(False)
#w.set_deletable(False)
#w.set_resizable(False)
w.set_keep_above(True)
w.set_skip_taskbar_hint(True)
w.set_skip_pager_hint(True)
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
# OSK widget
osk = KeyboardOSK(embeded=False,nocreate=True)
osk.update(lang,variant)
osk.create_layout(False)

osk.l[0].pack_start(exit, 1, True, True)
#osk.l[0].set_homogeneous(True)
#osk.l[1].set_homogeneous(True)
#osk.l[2].set_homogeneous(True)
#osk.l[3].set_homogeneous(True)
#osk.l[4].set_homogeneous(True)
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

#hb.pack_start(Gtk.Label(label="    "))
wwidth,wheight = w.get_size()
#hb.set_size_request(wwidth,50)
#layout.pack_start(osk.l[0], 1, True, True)
#layout.pack_start(osk.l[1], 1, True, True)
sutun_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

satir_1 = Gtk.Box()
satir_1_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
satir_1_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
satir_1_3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

satir_23 = Gtk.Box()
satir_23_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
satir_23_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
satir_23_3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

satir_4 = Gtk.Box()
satir_4_1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
satir_4_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
satir_4_3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

sutun_2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
#satir_3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

satir_1_1.pack_start(osk.l[1], 1, True, True)
satir_1_2.pack_start(osk.btnbspc, 1, True, True)
satir_1.pack_start(satir_1_1, 1, True, True)
satir_1.pack_start(satir_1_2, 1, True, True)
sutun_1.pack_start(satir_1, 1, True, True)

satir_23_1.pack_start(osk.l[2], 1, True, True)
satir_23_1.pack_start(osk.l[3], 1, True, True)
satir_23_2.pack_start(osk.btnenter, 1, True, True)
satir_23.pack_start(satir_23_1, 1, True, True)
satir_23.pack_start(satir_23_2, 1, True, True)
sutun_1.pack_start(satir_23, 1, True, True)

satir_4_1.pack_start(osk.l[4], 1, True, True)
satir_4_2.pack_start(osk.btnshft, 1, True, True)
satir_4.pack_start(satir_4_1, 1, True, True)
satir_4.pack_start(satir_4_2, 1, True, True)
sutun_1.pack_start(satir_4, 1, True, True)
sutun_1.pack_start(osk.l[5], 1, True, True)

sutun_2_1 = Gtk.Box()
sutun_2_2 = Gtk.Box()
sutun_2_3 = Gtk.Box()
sutun_2_4 = Gtk.Box()
sutun_2_5 = Gtk.Box()
sutun_2_1.pack_start(osk.btndel, 1, True, True)
sutun_2_1.pack_start(osk.btnprtsc, 1, True, True)

sutun_2_2.pack_start(osk.btnhome, 1, True, True)
sutun_2_2.pack_start(osk.btnend, 1, True, True)

sutun_2_3.pack_start(osk.btnpgup, 1, True, True)
sutun_2_3.pack_start(osk.btnpgdn, 1, True, True)
lleft=Gtk.Label("a")
sutun_2_4.pack_start(lleft, 1, True, False)
sutun_2_4.pack_start(osk.btnup, 1, True, True)
sutun_2_4.pack_start(Gtk.Label(""), 1, True, False)

sutun_2_5.pack_start(osk.btnleft, 1, True, True)
sutun_2_5.pack_start(osk.btndown, 1, True, True)
sutun_2_5.pack_start(osk.btnright, 1, True, True)

sutun_2.pack_start(sutun_2_1, 1, True, True)
sutun_2.pack_start(sutun_2_2, 1, True, True)
sutun_2.pack_start(sutun_2_3, 1, True, True)
sutun_2.pack_start(sutun_2_4, 1, True, True)
sutun_2.pack_start(sutun_2_5, 1, True, True)

kutu = Gtk.Box()
kutu.pack_start(sutun_1, 1, True, True)
kutu.pack_start(sutun_2, 1, True, True)


layout.pack_start(kutu, 1, True, True)
#layout.pack_start(osk.l[4], 1, True, True)
#layout.pack_start(osk.l[5], 1, True, True)

# Show window
w.add(layout)
w.show_all()
if os.environ["USER"]=="root" and not(os.path.isfile("{}/.osk".format(os.environ["HOME"]))):
    screensize = Gdk.Screen.get_default()
    w.resize(300,100)
    windowwidth, windowheight = w.get_size()
    w.move((screensize.get_width()-windowwidth)/2, screensize.get_height()-windowheight)
# css
screen = Gdk.Screen.get_default()
css = """
window, button {
    outline-style: none;
    border: 1px solid black;
    background: #000;
}
headerbar {
    outline-style: none;
    border: 1px solid black;
    /*background: #005;*/
background: rgb(16,32,48);
background: linear-gradient(0deg, rgba(16,32,48,1) 30%, rgba(60,98,111,1) 74%);
}
"""

gtk_provider = Gtk.CssProvider()
gtk_context = Gtk.StyleContext()
gtk_context.add_provider_for_screen(
screen, gtk_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
gtk_provider.load_from_data(css.encode("UTF-8"))
osk.style()
Gtk.main()
