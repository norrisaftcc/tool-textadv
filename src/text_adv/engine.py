"""
Core game engine for the text adventure using adventurelib.
This module provides the foundation for both console and web interfaces.
"""

import adventurelib as adv
from colorama import init, Fore, Back, Style
import random

# Initialize colorama
init(autoreset=True)

# Define color themes
class ColorTheme:
    """Color themes for different types of text in the game."""
    
    # Default theme
    DEFAULT = {
        "room_name": Fore.CYAN + Style.BRIGHT,
        "room_desc": Fore.WHITE,
        "item_name": Fore.YELLOW,
        "item_desc": Fore.WHITE,
        "command": Fore.GREEN,
        "error": Fore.RED,
        "success": Fore.GREEN + Style.BRIGHT,
        "hint": Fore.MAGENTA + Style.DIM,
        "speech": Fore.CYAN + Style.ITALIC,
        "system": Fore.WHITE + Back.BLUE,
        "header": Fore.BLACK + Back.WHITE + Style.BRIGHT
    }
    
    # Add more themes as needed
    SPOOKY = {
        "room_name": Fore.RED + Style.BRIGHT,
        "room_desc": Fore.WHITE + Style.DIM,
        "item_name": Fore.YELLOW,
        "item_desc": Fore.WHITE + Style.DIM,
        "command": Fore.GREEN,
        "error": Fore.RED + Style.BRIGHT,
        "success": Fore.GREEN,
        "hint": Fore.MAGENTA + Style.DIM,
        "speech": Fore.CYAN,
        "system": Fore.WHITE + Back.RED,
        "header": Fore.WHITE + Back.RED + Style.BRIGHT
    }

    @staticmethod
    def get_theme(theme_name="DEFAULT"):
        """Get a color theme by name."""
        return getattr(ColorTheme, theme_name, ColorTheme.DEFAULT)

# Current theme
current_theme = ColorTheme.DEFAULT

# Enhanced print functions
def print_styled(text, style_name):
    """Print text with the specified style from the current theme."""
    if style_name in current_theme:
        print(current_theme[style_name] + text)
    else:
        print(text)

# Game state singleton
class GameState:
    """Singleton class to manage global game state."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance.init()
        return cls._instance
    
    def init(self):
        """Initialize the game state."""
        self.turn_count = 0
        self.flags = {}
        self.variables = {}
        self.current_room = None
        self.player_name = "Adventurer"
        
    def increment_turn(self):
        """Increment the turn counter."""
        self.turn_count += 1
        
    def set_flag(self, flag_name, value=True):
        """Set a game flag."""
        self.flags[flag_name] = value
        
    def get_flag(self, flag_name, default=False):
        """Get a game flag, with a default if not found."""
        return self.flags.get(flag_name, default)
    
    def set_var(self, var_name, value):
        """Set a game variable."""
        self.variables[var_name] = value
        
    def get_var(self, var_name, default=None):
        """Get a game variable, with a default if not found."""
        return self.variables.get(var_name, default)

# Initialize game state
game_state = GameState()

# Enhanced Room class
class Room(adv.Room):
    """Enhanced Room class with additional functionality."""
    
    def __init__(self, description):
        super().__init__(description)
        self.first_visit = True
        self.visit_count = 0
        self.long_description = ""
        self.short_description = description
    
    def describe(self):
        """Print the room description, with special handling for first visits."""
        self.visit_count += 1
        
        # Print room name if available
        if hasattr(self, 'name'):
            print_styled(self.name, "room_name")
            print_styled("=" * len(self.name), "room_name")
        
        # Print appropriate description
        if self.first_visit and self.long_description:
            print_styled(self.long_description, "room_desc")
            self.first_visit = False
        else:
            print_styled(self.short_description, "room_desc")
        
        # List items
        if self.items:
            print("\nYou see:")
            for item in self.items:
                print_styled(f"  {item}", "item_name")
        
        # List exits
        exits = []
        for direction, room in self.exits.items():
            exits.append(direction)
        
        if exits:
            print("\nExits:", ", ".join(exits))
    
    def add_item(self, item):
        """Add an item to the room."""
        if not hasattr(self, 'items'):
            self.items = adv.Bag()
        self.items.add(item)
    
    def remove_item(self, item):
        """Remove an item from the room."""
        if hasattr(self, 'items') and item in self.items:
            self.items.remove(item)

# Enhanced Item class
class Item(adv.Item):
    """Enhanced Item class with additional functionality."""
    
    def __init__(self, name, description):
        super().__init__(name)
        self.description = description
        self.takeable = True
        self.hidden = False
        self.use_callbacks = {}
        
    def describe(self):
        """Print the item description."""
        print_styled(self.description, "item_desc")
    
    def on_use(self, target=None):
        """Handle using the item, possibly on a target."""
        if target in self.use_callbacks:
            return self.use_callbacks[target]()
        elif None in self.use_callbacks:
            return self.use_callbacks[None]()
        else:
            print_styled(f"You're not sure how to use the {self}.", "error")
            return False
    
    def add_use_callback(self, callback, target=None):
        """Add a callback for when the item is used."""
        self.use_callbacks[target] = callback

# Player inventory
inventory = adv.Bag()

# Setup adventurelib
@adv.when('look')
def look():
    """Look around the current room."""
    game_state.current_room.describe()

@adv.when('inventory')
@adv.when('i')
def show_inventory():
    """Show player inventory."""
    if not inventory:
        print_styled("You're not carrying anything.", "hint")
        return
    
    print_styled("You're carrying:", "command")
    for item in inventory:
        print_styled(f"  {item}", "item_name")

@adv.when('take ITEM')
@adv.when('get ITEM')
@adv.when('pick up ITEM')
def take(item):
    """Take an item from the current room."""
    obj = adv.match_item(item, game_state.current_room.items)
    if not obj:
        print_styled(f"There's no {item} here.", "error")
        return
    
    if not getattr(obj, 'takeable', True):
        print_styled(f"You can't take the {item}.", "error")
        return
    
    game_state.current_room.items.remove(obj)
    inventory.add(obj)
    print_styled(f"You take the {obj}.", "success")

@adv.when('drop ITEM')
def drop(item):
    """Drop an item from inventory into the current room."""
    obj = adv.match_item(item, inventory)
    if not obj:
        print_styled(f"You don't have a {item}.", "error")
        return
    
    inventory.remove(obj)
    game_state.current_room.items.add(obj)
    print_styled(f"You drop the {obj}.", "success")

@adv.when('examine ITEM')
@adv.when('look at ITEM')
@adv.when('inspect ITEM')
def examine(item):
    """Examine an item in the room or inventory."""
    obj = adv.match_item(item, game_state.current_room.items) or adv.match_item(item, inventory)
    if not obj:
        print_styled(f"You don't see a {item} here.", "error")
        return
    
    obj.describe()

@adv.when('use ITEM')
def use(item):
    """Use an item from inventory."""
    obj = adv.match_item(item, inventory)
    if not obj:
        print_styled(f"You don't have a {item}.", "error")
        return
    
    obj.on_use()

@adv.when('use ITEM on TARGET')
@adv.when('use ITEM with TARGET')
def use_on(item, target):
    """Use an item on a target."""
    item_obj = adv.match_item(item, inventory)
    if not item_obj:
        print_styled(f"You don't have a {item}.", "error")
        return
    
    # Target could be an item in room or inventory
    target_obj = (adv.match_item(target, game_state.current_room.items) or 
                  adv.match_item(target, inventory))
    
    if target_obj:
        item_obj.on_use(target_obj)
    else:
        print_styled(f"You don't see a {target} here.", "error")

# Direction movement handlers
@adv.when('north', direction='north')
@adv.when('south', direction='south')
@adv.when('east', direction='east')
@adv.when('west', direction='west')
@adv.when('up', direction='up')
@adv.when('down', direction='down')
@adv.when('n', direction='north')
@adv.when('s', direction='south')
@adv.when('e', direction='east')
@adv.when('w', direction='west')
@adv.when('u', direction='up')
@adv.when('d', direction='down')
def go(direction):
    """Move in a direction."""
    room = game_state.current_room.exit(direction)
    if room:
        game_state.current_room = room
        room.describe()
        game_state.increment_turn()
    else:
        print_styled(f"You can't go {direction}.", "error")

@adv.when('go DIRECTION')
@adv.when('move DIRECTION')
@adv.when('walk DIRECTION')
def go_direction(direction):
    """Go in a specified direction."""
    direction = direction.lower()
    directions = {
        'north': 'north', 'south': 'south', 'east': 'east', 'west': 'west',
        'up': 'up', 'down': 'down',
        'n': 'north', 's': 'south', 'e': 'east', 'w': 'west',
        'u': 'up', 'd': 'down'
    }
    
    if direction in directions:
        go(directions[direction])
    else:
        print_styled(f"I don't understand which direction '{direction}' is.", "error")

def set_current_room(room):
    """Set the current room and describe it."""
    game_state.current_room = room
    room.describe()

def start_game():
    """Start the game loop."""
    adv.start()

# Main setup function to be called by front-end interfaces
def setup_game():
    """Set up the game world (to be extended by game creators)."""
    # This would be extended with actual game content
    pass