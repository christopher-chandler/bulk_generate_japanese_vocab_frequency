# Standard
# None

# Pip
from aqt import QMenu, QAction
from aqt.browser import Browser
from anki.hooks import addHook

# Custom
from .tab_functionality import (
    generate_information_for_selected_cards,
)


def set_up_edit_menu(browser: Browser) -> None:
    """
    Adds a submenu named "Japanese Frequency & Word Type Analyzer"
    to the edit menu of the Anki browser window.

    This submenu provides functionality to analyze and generate data for
    Japanese vocabulary within Anki.

    Args:
        browser (Browser): An instance of the Anki browser class.

    Returns:
        None
    """

    menu = browser.form.menuEdit
    submenu = QMenu("Japanese Frequency & Word Type Analyzer", browser)

    # Create actions
    bulk_generate_frequency = QAction("Generate Vocab Frequency", browser)
    bulk_generate_word_type = QAction("Generate Word Type Data", browser)

    # Connect actions to their handlers
    bulk_generate_frequency.triggered.connect(
        lambda _, brow=browser: generate_information_for_selected_cards(
            browser=brow,
            info_title="Frequency",
            data_generation_type="frequency",
            dictionary_source="freq_dict",
        )
    )
    bulk_generate_word_type.triggered.connect(
        lambda _, brow=browser: generate_information_for_selected_cards(
            browser=brow,
            info_title="Word Type",
            data_generation_type="word type",
            dictionary_source="jmdict",
        )
    )

    # Add actions to the submenu
    submenu.addAction(bulk_generate_frequency)
    submenu.addAction(bulk_generate_word_type)

    # Add submenu to the main edit menu
    menu.addSeparator()  # Optional: Add a separator for visual clarity
    menu.addMenu(submenu)


def show_edit_menu() -> None:
    """
    Registers a hook to automatically call the `set_up_edit_menu`
    unction whenever the Anki browser sets up its menus.

    This ensures the submenu is added whenever the user opens the Anki browser.

    Returns:
        None
    """
    addHook("browser.setupMenus", set_up_edit_menu)
