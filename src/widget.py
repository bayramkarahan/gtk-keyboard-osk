#!/usr/bin/python3
import gi
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from pynput.keyboard import Key, Controller
import subprocess

# Definitions for classes
keyboard = Controller()
single_keys = [] 
alt_lock = False
# alt key fixes (xfce lxde cinnamon)
alt_enabled = False
big = False
alt = Gtk.Button(label=" ⌥ ")
capslock = Gtk.Button(label=" CapsLk ")

active_toggle = []
all_keys = []
class DialogExample(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Dialog", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label="This is a dialog to display additional information")

        box = self.get_content_area()
        box.add(label)
        self.show_all()
        
class KeyboardOSK(Gtk.Box):
    def __init__(self,embeded=True,nocreate=False):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        # keyboard layout definition
        self.kbd = {}
        self.kbd_s = {}
        self.kbd_a = {}
        self.kbd_as = {}
        self.l = []

        # Signal connect
        alt.connect("clicked", self.alt_toggle)
        capslock.connect("clicked", self.capslock_toggle)
        capslock.set_name("key_disabled")

        if not nocreate:
            self.update()
            self.create_layout(embeded)
        self.style()

    def create_layout(self,embeded=True):
        self.l = []
        for j in [0,1,2,3,4,5]:
            ll = Gtk.Box()

            self.l.append(ll)
            if embeded:
                self.pack_start(ll, 1, True, True)
        # F buttons (Row 0 or headerbar)
        self.l[0].pack_start(key(Key.f1, " f1 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f2, " f2 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f3, " f3 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f4, " f4 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f5, " f5 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f6, " f6 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f7, " f7 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f8, " f8 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f9, " f9 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f10, " f10 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f11, " f11 ").button,1,True,False)
        self.l[0].pack_start(key(Key.f12, " f12 ").button,1,True,False)
        # Row 1
        self.l[1].pack_start(key(Key.esc, "Esc").button, 1,True,False)
        self.add_key(41,1)
        for i in range(2,14):
            self.add_key(i,1)
        self.l[1].pack_start(key(Key.backspace, " ⌫ ").button, 1, True, False)
        self.l[1].pack_start(key(Key.delete, "Del").button,1,True,False)
        # Row 2
        self.l[2].pack_start(key(Key.tab, " Tab ").button, 1, True, False)
        for i in range(16,28):
            self.add_key(i,2)
        self.l[2].pack_end(key(Key.page_down, " PgDn ").button, 1, True, False)
        self.l[2].pack_start(key(Key.page_up, " PgUp ").button, 1, True, False)
        # Row 3
        self.l[3].pack_start(capslock, 1, True, False)
        for i in range(30,41):
            self.add_key(i,3)
        self.add_key(43,3)
        self.l[3].pack_end(key(Key.enter, " Enter ⏎  ").button, 1, True, False)
        # Row 4
        self.l[4].pack_start(key(Key.shift, "  ⇧  ", True).button, 1, True, False)
        self.add_key(86,4) # TLDE
        for i in range(44,54):
            self.add_key(i,4)
        self.l[4].pack_start(key(Key.home, " Home ").button, 1, True, False)
        self.l[4].pack_start(key(Key.end, " End ").button, 1, True, False)
        # Row 5
        self.l[5].pack_start(key(Key.ctrl, " Ctrl ", True).button, 1, True, False)
        self.l[5].pack_start(key(Key.cmd, " Alt ").button, 1, True, False)
        self.l[5].pack_start(alt, 1, True, False)
        self.l[5].pack_start(key(Key.space, 27*" ").button, 1, True, True)
        self.l[5].pack_start(key(Key.alt_gr, " AltGr ", True).button, 1, True, False)
        self.l[5].pack_start(key(Key.ctrl, " Ctrl ", True).button, 1, True, False)
        self.l[5].pack_start(key(Key.left, " ← ").button, 1, True, False)
        self.l[5].pack_start(key(Key.up, " ↑ ").button, 1, True, False)
        self.l[5].pack_start(key(Key.down, " ↓ ").button, 1, True, False)
        self.l[5].pack_start(key(Key.right, " → ").button, 1, True, False)
        

    def get_key(self,num):
        return key(self.kbd[str(num)],
                   m=" "+self.kbd[str(num)]+" ",
                   sft=" "+self.kbd_s[str(num)]+" ",
                   altgr=" "+self.kbd_a[str(num)]+" ",
                   altgr_sft=" "+self.kbd_as[str(num)]+" ",
                   toggle=False).button

    def add_key(self,num,row):
        self.l[row].pack_start(self.get_key(num), 1, True, True)

    def alt_toggle(self,widget):
        global alt_enabled
        global alt_lock
        if not alt_enabled:
            alt_enabled = True
        elif not alt_lock:
            alt_lock = True
        else:
            alt_enabled = False
            alt_lock = False
        if alt_enabled:
            widget.set_name("key_enabled")
        else:
            widget.set_name("key_normal")
        if alt_lock:
            widget.set_name("key_lock")

    def capslock_toggle(self,widget):
        global big
        if big:
            widget.set_name("key_normal")
        else:
            widget.set_name("key_lock")
        big = not big
        global active_toggle
        if big and Key.shift not in active_toggle:
            active_toggle.append(Key.shift)
        elif not big and Key.shift in active_toggle:
            active_toggle.remove(Key.shift)
        global all_keys
        for k in all_keys:
            k.update()

    def u2str(self,ucode):
        if ucode[0:2] == "U+":
            return chr(int(ucode[2:],16))
        elif ucode[0:2] == "+U":
            return chr(int(ucode[3:],16))
        return " "

    def update(self,keyboard="us",variant=""):
        output = subprocess.getoutput("ckbcomp -model pc106 -layout {} {} -compact".format(keyboard,variant))
        for line in output.split("\n"):
            if "=" not in line or line[0] == "#":
                continue
            try:
                num     = line.split("=")[0].strip().split(" ")[1]
                ucode   = line.split("=")[1].strip().split(" ")[0]
                scode   = line.split("=")[1].strip().split(" ")[1]
                acode   = line.split("=")[1].strip().split(" ")[2]
                ascode  = line.split("=")[1].strip().split(" ")[3]
                if acode == ucode:
                    acode = ""
                if scode == ascode:
                    ascode = ""
                self.kbd[num] = self.u2str(ucode)
                self.kbd_s[num] = self.u2str(scode)
                self.kbd_a[num] = self.u2str(acode)
                self.kbd_as[num] = self.u2str(ascode)
            except:
                pass
    def style(self):
        screen = Gdk.Screen.get_default()
        css = """
        button, label, entry {
            font-size: """+str(screen.get_height()/55)+"""px;
            font-family: monospace;
        }
        #key_enabled {
            color: #FFF;
            background: #8e0000;
        }
        #key_lock {
            color: #FFF;
            background: #008e00;
        }
        #key_normal, #key_lock, #key_enabled{
	    background: #102030;
            margin: 0px;
            padding: 0px;
            min-height: 32px;
            min-width: 32px;
            border: 3px solid #405060;
	    color:#FFF;
            border-radius:5px;
        }
        """
        gtk_provider = Gtk.CssProvider()
        gtk_context = Gtk.StyleContext()
        gtk_context.add_provider_for_screen(
           screen, gtk_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        gtk_provider.load_from_data(css.encode("UTF-8"))
        global capslock
        global alt
        alt.set_name("key_normal")
        capslock.set_name("key_normal")

class key:
    def __init__(self, n, m=None, toggle=False, flat=True, sft="", altgr="", altgr_sft=""):
        if not m:
            m = n
        self.key = n
        self.label = m
        self.label_sft = sft
        self.label_altgr = altgr
        self.label_altgr_sft = altgr_sft
        self.flat = flat
        self.button = Gtk.Button(label=m)
        self.active = False
        self.lock = False
        #print ("deneme")
        color = Gdk.color_parse('#aaaaaa')
        self.button.modify_bg(Gtk.StateType.PRELIGHT, color)

        if not toggle:
            self.button.connect("pressed", self.press)
            self.button.connect("released", self.release)
        else:
            self.button.connect("clicked", self.toggle)
        if toggle:
            single_keys.append(self)
        self.button.set_name("key_normal")
        global all_keys
        all_keys.append(self)
        
         
    def press(self, widget):
        global alt_enabled
        global big
        
        color = Gdk.color_parse('#aa0000')
        self.button.modify_bg(Gtk.StateType.PRELIGHT, color)

        self.button.set_name("key_enabled")
        if self.lock:
            self.button.set_name("key_lock")
        if big and self.flat:
            keyboard.press(Key.shift)
        if alt_enabled or alt_lock:
            keyboard.press(Key.alt)
        if self.key:
            keyboard.press(self.key)
            #time.sleep(0.1)
            
        if self.key not in active_toggle:
            active_toggle.append(self.key)
        for k in all_keys:
            k.update()
            
            
    def update(self):
        global active_toggle
        if Key.shift in active_toggle and Key.alt_gr not in active_toggle and self.label_sft:
            self.button.set_label(self.label_sft)
        elif Key.shift not in active_toggle and Key.alt_gr in active_toggle and self.label_altgr:
            self.button.set_label(self.label_altgr)
        elif Key.shift in active_toggle and Key.alt_gr in active_toggle and self.label_altgr_sft:
            self.button.set_label(self.label_altgr_sft)
        else:
            self.button.set_label(self.label)

    def release(self, widget):
        global alt_enabled
        
        color = Gdk.color_parse('#aaaaaa')
        self.button.modify_bg(Gtk.StateType.PRELIGHT, color)

        if big and self.flat:
            keyboard.release(Key.shift)
        if not self.lock:
            self.active = False
            self.button.set_name("key_normal")
            if self.key:
                keyboard.release(self.key)
        if self not in single_keys:
            for key in single_keys:
                if not key.lock and key.active:
                    key.release(self.key)
            if not alt_lock:
                alt_enabled = False
                alt.set_name("key_normal")
            keyboard.release(Key.alt)
        if self.key in active_toggle:
            active_toggle.remove(self.key)
        for k in all_keys:
            k.update()

    def toggle(self, widget):
        global active_toggle
        if not self.active:
            self.active = True
        elif not self.lock:
            self.lock = True
        else:
            self.active = False
            self.lock = False
        if self.active or self.lock:
            self.press(widget)
        else:
            self.release(widget)
        global all_keys
