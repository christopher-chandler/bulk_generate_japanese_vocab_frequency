# -*- coding: utf-8 -*-
#
# Entry point for the add-on into Anki
# Please do not edit this if you do not know what you are doing.
#
# License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>

# Standard
import os

# Pip
from anki.hooks import addHook

# Custom
from .bunseki.settings.logger.basic_logger import catch_and_log_info
from . import main

catch_and_log_info(custom_message="Add was on successfully  started")
# addHook("browser.setupMenus", main.set_up_edit_menu)
