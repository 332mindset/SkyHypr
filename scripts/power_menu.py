#!/usr/bin/env python3

import subprocess
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

ACTIONS = [
    ("", "Lock", "hyprlock"),
    ("", "Logout", "hyprctl dispatch exit"),
    ("󰤄", "Sleep", "systemctl suspend"),
    ("", "Reboot", "systemctl reboot"),
    ("", "Shutdown", "systemctl poweroff"),
]

class PowerMenu(Gtk.Window):
    def __init__(self):
        super().__init__(title="Power Menu")

        self.set_default_size(360, 420)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_name("power-window")

        css = b"""
        #power-window {
            background: rgba(8, 8, 8, 0.96);
            border-radius: 20px;
        }

        button {
            background: rgba(18, 18, 18, 0.92);
            color: #d0d0d0;
            border: 1px solid #2a2a2a;
            border-radius: 16px;
            padding: 14px;
            margin: 6px;
            font-family: JetBrainsMono Nerd Font;
            font-size: 15px;
            font-weight: 600;
        }

        button:hover {
            background: rgba(0, 217, 255, 0.12);
            color: #00d9ff;
            border-color: #00d9ff;
        }

        label {
            color: #d0d0d0;
            font-family: JetBrainsMono Nerd Font;
        }

        .title {
            color: #00d9ff;
            font-size: 16px;
            font-weight: bold;
        }
        """

        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_margin_top(18)
        box.set_margin_bottom(18)
        box.set_margin_start(18)
        box.set_margin_end(18)

        title = Gtk.Label(label="Power Menu")
        title.get_style_context().add_class("title")
        box.pack_start(title, False, False, 6)

        for icon, text, command in ACTIONS:
            button = Gtk.Button(label=f"{icon}  {text}")
            button.connect("clicked", self.run_action, command)
            box.pack_start(button, False, False, 0)

        self.add(box)
        self.connect("key-press-event", self.on_key)
        self.connect("destroy", Gtk.main_quit)

    def run_action(self, button, command):
        Gtk.main_quit()
        subprocess.Popen(command, shell=True)

    def on_key(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()

if __name__ == "__main__":
    win = PowerMenu()
    win.show_all()
    Gtk.main()
