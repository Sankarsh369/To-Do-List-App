# styles.py
class AppStyles:
    # Colors
    PRIMARY_COLOR = "#5a95ff"  # Blue
    ACCENT_COLOR = "#4CAF50"   # Green for complete/add
    DELETE_COLOR = "#ff5c5c"   # Red for delete
    BG_COLOR = "#f4f7f6"       # Light Greyish Green background
    CARD_BG_COLOR = "#ffffff"  # White for main container and list items
    TEXT_COLOR = "#333333"     # Dark Grey for general text
    LIGHT_TEXT_COLOR = "#666666" # Lighter grey for meta info
    COMPLETED_TEXT_COLOR = "#888888" # Grey for completed task text
    OVERDUE_COLOR = "#d32f2f" # Darker red for overdue tasks
    # ADD THIS LINE:
    BORDER_COLOR = "#e0e0e0" # Define a border color

    # Fonts
    FONT_FAMILY = "Segoe UI" # A clean, modern default
    FONT_SIZE_LARGE = 14
    FONT_SIZE_MEDIUM = 12
    FONT_SIZE_SMALL = 10
    FONT_SIZE_XSMALL = 9

    # Padding and Spacing
    PADDING = 15
    ITEM_PADDING_Y = 10
    ITEM_PADDING_X = 15
    BUTTON_PAD_X = 10
    BUTTON_PAD_Y = 5

    # Borders and Radii (Tkinter often limited here, but for custom elements)
    BORDER_THICKNESS = 1
    BORDER_RADIUS = 8 # Visual cue, not directly applied by Tkinter widgets

    # Styles for ttk widgets
    # Define custom styles for ttk widgets
    # These will be set in gui.py using ttk.Style()
    TTK_BUTTON_STYLE = 'TButton'
    TTK_ENTRY_STYLE = 'TEntry'
    TTK_LABEL_STYLE = 'TLabel'
    TTK_FRAME_STYLE = 'TFrame'
    TTK_COMBOBOX_STYLE = 'TCombobox'
    TTK_CHECKBUTTON_STYLE = 'TCheckbutton'