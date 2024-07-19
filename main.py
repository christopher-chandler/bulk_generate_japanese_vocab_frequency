# -*- coding: utf-8 -*-
"""
Created on 09/12/2014
@author: Myxoma

updated on 18/07/2024
@author: christopherchandler

This add-on inserts the frequency for a given Japanese word to a given
Anki field.
"""

# Standard
# None

# Pip
# None

# Custom
from .bunseki.main_tools_menu.anki_main_menu_tool import show_about_add_on
from .bunseki.edit_browser_menu.main_show_edit_menu_tabs import show_edit_menu
from anki.hooks import addHook
from .bunseki.add_on_update_info.pop_up import show_update_message

# Connect the function to Anki's profile loaded signal
# addHook("profileLoaded", show_update_message)

show_about_add_on()
show_edit_menu()
