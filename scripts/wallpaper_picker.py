#!/usr/bin/env python3

import os
import subprocess
import hashlib
from pathlib import Path

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk

WALLPAPER_DIR = Path.home() / "Downloads/pictureWalpapers"
CACHE_DIR = Path.home() / ".cache/wallpaper-picker-thumbs"

THUMB_W = 180
THUMB_H = 105

CACHE_DIR.mkdir(parents=True, exist_ok=True)

EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def make_thumb(path: Path) -> Path:
    key = hashlib.md5(str(path).encode()).hexdigest()
    thumb = CACHE_DIR / f"{key}.png"

    if thumb.exists():
        return thumb

    pixbuf = GdkPixbuf.Pixbuf.new_from_file(str(path))
    width = pixbuf.get_width()
    height = pixbuf.get_height()

    scale = max(THUMB_W / width, THUMB_H / height)
    new_w = int(width * scale)
    new_h = int(height * scale)

    scaled = pixbuf.scale_simple(new_w, new_h, GdkPixbuf.InterpType.BILINEAR)

    x = max((new_w - THUMB_W) // 2, 0)
    y = max((new_h - THUMB_H) // 2, 0)

    cropped = GdkPixbuf.Pixbuf.new(
        GdkPixbuf.Colorspace.RGB,
        True,
        8,
        THUMB_W,
        THUMB_H
    )

    scaled.copy_area(x, y, THUMB_W, THUMB_H, cropped, 0, 0)
    cropped.savev(str(thumb), "png", [], [])

    return thumb


def set_wallpaper(path: str):
    subprocess.Popen([
        "awww", "img", path,
        "--transition-type", "grow",
        "--transition-duration", "1.0",
        "--transition-fps", "60"
    ])
    Path.home().joinpath(".cache/current_wallpaper").write_text(path)
    Gtk.main_quit()


class WallpaperPicker(Gtk.Window):
    def __init__(self):
        super().__init__(title="Wallpapers")

        self.set_default_size(720, 430)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_name("wallpaper-window")

        css = b"""
        #wallpaper-window {
            background: rgba(11, 11, 11, 0.96);
            border-radius: 18px;
        }

        flowbox {
            background: transparent;
        }

        flowboxchild {
            padding: 8px;
            border-radius: 14px;
            border: 1px solid transparent;
            background: transparent;
        }

        flowboxchild:selected {
            border: 1px solid #00d9ff;
            background: rgba(0, 217, 255, 0.10);
        }
        """

        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        outer.set_margin_top(18)
        outer.set_margin_bottom(18)
        outer.set_margin_start(18)
        outer.set_margin_end(18)

        title = Gtk.Label(label="Wallpapers")
        title.set_xalign(0)
        title.set_markup('<span foreground="#00d9ff" weight="bold">Wallpapers</span>')
        outer.pack_start(title, False, False, 0)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.flow = Gtk.FlowBox()
        self.flow.set_max_children_per_line(3)
        self.flow.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.flow.set_activate_on_single_click(False)
        self.flow.connect("child-activated", self.on_activate)

        wallpapers = sorted(
            p for p in WALLPAPER_DIR.iterdir()
            if p.is_file() and p.suffix.lower() in EXTS
        )

        for wp in wallpapers:
            thumb = make_thumb(wp)

            img = Gtk.Image.new_from_file(str(thumb))
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            box.pack_start(img, True, True, 0)

            child = Gtk.FlowBoxChild()
            child.wallpaper_path = str(wp)
            child.add(box)

            self.flow.add(child)

        scrolled.add(self.flow)
        outer.pack_start(scrolled, True, True, 0)

        self.add(outer)

        self.connect("key-press-event", self.on_key)
        self.connect("destroy", Gtk.main_quit)

    def on_activate(self, flowbox, child):
        set_wallpaper(child.wallpaper_path)

    def on_key(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()

        if event.keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
            selected = self.flow.get_selected_children()
            if selected:
                set_wallpaper(selected[0].wallpaper_path)


if __name__ == "__main__":
    win = WallpaperPicker()
    win.show_all()
    Gtk.main()
