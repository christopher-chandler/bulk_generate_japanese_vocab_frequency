# -*- coding: utf-8 -*-
#
# Entry point for the add-on into Anki
# Please do not edit this if you do not know what you are doing.
#
# Copyright: (c) 2017 Glutanimate <https://glutanimate.com/>
# License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>

# Standard
# None

# Custom
from . import main

# Pip
from anki.hooks import addHook

# Hook Add-on
addHook("browser.setupMenus", main.set_up_edit_menu)