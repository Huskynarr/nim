#!/usr/bin/env python3
"""Vollbild-Kiosk-Fenster für Nim (GTK3 + WebKit2).

Standalone: ``python3 show.py`` – oder einfach ``index.html`` im Browser öffnen.
X oben rechts, ESC oder Q schließen das Fenster.
"""
import os
from pathlib import Path

# Kiosk-Robustheit: ohne GPU-Compositing (Canvas-2D braucht es nicht)
os.environ.setdefault("WEBKIT_DISABLE_COMPOSITING_MODE", "1")

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
try:
    gi.require_version("WebKit2", "4.1")
except ValueError:
    gi.require_version("WebKit2", "4.0")
from gi.repository import WebKit2


class AppWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Nim - Mathematisch Interaktiv")
        self.set_decorated(False)
        self.fullscreen()

        self.webview = WebKit2.WebView()
        settings = self.webview.get_settings()
        settings.set_enable_javascript(True)
        settings.set_enable_write_console_messages_to_stdout(True)
        html_file = Path(__file__).resolve().parent / "index.html"
        self.webview.load_uri(html_file.as_uri())

        btn_close = Gtk.Button(label="X")
        btn_close.set_halign(Gtk.Align.END)
        btn_close.set_valign(Gtk.Align.START)
        btn_close.connect("clicked", Gtk.main_quit)

        overlay = Gtk.Overlay()
        overlay.add(self.webview)
        overlay.add_overlay(btn_close)
        self.add(overlay)

        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.on_key)

    def on_key(self, _widget, event):
        if event.keyval in (Gdk.KEY_Escape, Gdk.KEY_q, Gdk.KEY_Q):
            Gtk.main_quit()
            return True
        return False


if __name__ == "__main__":
    win = AppWindow()
    win.show_all()
    Gtk.main()
