# Creating Your Own Text Adventure with Alpha Cloudplex

This tutorial will guide you through creating your own area in the Alpha Cloudplex text adventure system. By the end of this tutorial, you'll understand how to create rooms, items, and interactive elements using our framework.

## Prerequisites

Before beginning, make sure you have:

1. Installed Python 3.9 or later
2. Installed the required packages (`pip install -r requirements.txt`)
3. Familiarized yourself with the basic structure of the project

## Understanding the Engine

The `text_adv` package provides a powerful engine for creating text adventures. Here's a quick overview of the key components:

### Rooms

Rooms are the basic building blocks of your game world. Each room has:
- A name
- A short description (shown on subsequent visits)
- A long description (shown on first visit)
- Exits to other rooms
- Items that can be found in the room

### Items

Items are objects that players can interact with. Each item has:
- A name
- A description
- Properties like whether it can be taken
- Use callbacks that define what happens when the item is used

### NPCs

NPCs (Non-Player Characters) are implemented as special items with the `takeable` property set to `False`.

## Step 1: Create a New Area Module

First, let's create a new Python module for your area:

```python
"""
My Custom Area - An exciting new part of Alpha Cloudplex
"""

from text_adv.engine import Room, Item, game_state, inventory

def create_my_area():
    """Create and return the starting room of my custom area."""
    
    # Create rooms
    starting_room = Room("You stand in a brightly lit room with smooth white walls.")
    starting_room.name = "Entry Point"
    starting_room.long_description = """You find yourself in a pristine white room. 
The walls are smooth and seem to emit a soft glow. 
There's a sense of possibility in the air, as if this space is waiting to be defined."""
    
    second_room = Room("A colorful garden stretches before you, filled with digital flowers.")
    second_room.name = "Digital Garden"
    second_room.long_description = """As you enter, you're surrounded by a stunning array of flowers
that couldn't exist in the physical world. Some change colors as you watch,
others hover slightly above the ground, defying gravity."""
    
    # Connect rooms
    starting_room.exits['north'] = second_room
    second_room.exits['south'] = starting_room
    
    # Create items
    digital_key = Item("key", "A glowing digital key that pulses with blue energy.")
    digital_key.add_use_callback(lambda: print("The key glows brighter, but nothing happens... yet."))
    
    flower = Item("flower", "A strange digital flower that changes color as you watch.")
    flower.add_use_callback(lambda: use_flower())
    
    # Add items to rooms
    starting_room.add_item(digital_key)
    second_room.add_item(flower)
    
    # Return the starting room
    return starting_room

def use_flower():
    """Handle using the flower item."""
    from text_adv.engine import print_styled
    
    print_styled("You touch the digital flower.", "command")
    print_styled("It changes to match your mood, turning a peaceful blue color.", "success")
    print_styled("Somehow, you feel more relaxed now.", "hint")
    return True

def initialize_my_area():
    """Initialize the custom area and return the starting room."""
    return create_my_area()
```

## Step 2: Connect Your Area to the Main Game

Now, let's modify the main game to include your new area. Edit the `main.py` file:

```python
from text_adv.engine import setup_game as engine_setup, set_current_room
from text_adv.console import run_game
from text_adv.boardwalk import initialize_boardwalk
# Import your new area
from text_adv.my_area import initialize_my_area

def setup_game():
    """Set up the game world."""
    # Initialize the Boardwalk area
    boardwalk = initialize_boardwalk()
    
    # Initialize your custom area
    my_area = initialize_my_area()
    
    # Connect the Boardwalk to your area
    # Find a suitable room in the Boardwalk
    for room_name, room in boardwalk.exits.items():
        if room_name == "east":
            # Create a connection to your area
            room.exits['north'] = my_area
            my_area.exits['south'] = room
            break
    
    # Set the player's starting location
    set_current_room(boardwalk)
```

## Step 3: Adding Interactive Elements

Let's add some interactive elements to make your area more engaging:

### Adding an NPC

```python
def create_my_area():
    # ... previous code ...
    
    # Create an NPC
    guide = Item("guide", "A helpful digital assistant with a friendly smile.")
    guide.takeable = False
    starting_room.add_item(guide)
    
    # ... rest of the function ...
```

### Adding Special Interactions

To handle talking to your NPC, you can add a custom interaction function:

```python
def setup_npc_interactions():
    """Set up NPC interaction commands."""
    import adventurelib as adv
    from text_adv.engine import print_styled
    
    @adv.when('talk to guide')
    @adv.when('speak to guide')
    def talk_to_guide():
        """Talk to the guide NPC."""
        room = game_state.current_room
        
        # Check if the guide is in the current room
        found = False
        for item in room.items:
            if item.name.lower() == "guide" and not item.takeable:
                found = True
                break
        
        if not found:
            print_styled("There's no guide here to talk to.", "error")
            return
        
        print_styled('The guide smiles warmly.', 'speech')
        print_styled('"Welcome to your custom area! This is a space you created."', 'speech')
        print_styled('"Feel free to explore and see what you can find!"', 'speech')

def initialize_my_area():
    """Initialize the custom area and return the starting room."""
    setup_npc_interactions()
    return create_my_area()
```

## Step 4: Adding Puzzles

Let's add a simple puzzle to your area. We'll create a locked door that requires the key to open:

```python
def create_my_area():
    # ... previous code ...
    
    # Create a third room that's initially locked
    secret_room = Room("A hidden chamber filled with floating data visualizations.")
    secret_room.name = "Secret Data Chamber"
    secret_room.long_description = """You've discovered a hidden chamber where
data from across Alpha Cloudplex is visualized in stunning 3D projections.
Information flows like water through the air, forming patterns and structures."""
    
    # Add a locked door
    door = Item("door", "A sealed door with a glowing keyhole. It leads north.")
    door.takeable = False
    second_room.add_item(door)
    
    # Add a treasure in the secret room
    data_crystal = Item("crystal", "A beautiful crystal containing compressed data patterns.")
    secret_room.add_item(data_crystal)
    
    # Set up the locked connection
    # We don't actually connect the rooms yet - that happens when the key is used
    
    # Modify the key's use callback
    digital_key.add_use_callback(lambda: unlock_door(second_room, secret_room, door))
    
    # ... rest of the function ...
```

And add the unlock function:

```python
def unlock_door(current_room, target_room, door_item):
    """Handle unlocking the door with the key."""
    from text_adv.engine import print_styled, inventory
    
    # Check if we're in the right room
    if game_state.current_room != current_room:
        print_styled("There's no door here to unlock.", "error")
        return False
    
    # Check if the door is in the room
    found = False
    for item in current_room.items:
        if item == door_item:
            found = True
            break
    
    if not found:
        print_styled("There's no door here to unlock.", "error")
        return False
    
    # Unlock the door
    print_styled("You insert the digital key into the door's keyhole.", "command")
    print_styled("The key and door pulse with energy, then the door slides open.", "success")
    print_styled("A new path is revealed to the north!", "hint")
    
    # Connect the rooms
    current_room.exits['north'] = target_room
    target_room.exits['south'] = current_room
    
    # Remove the door item since it's now open
    current_room.remove_item(door_item)
    
    return True
```

## Step 5: Testing Your Area

Run the game to test your custom area:

```bash
python -m src.text_adv.main
```

Explore your creation, making sure that:
- All rooms are connected properly
- Items can be picked up and used
- NPCs respond correctly
- Puzzles work as expected

## Beyond the Basics

Once you've mastered these basics, you can explore more advanced features:

### Custom Commands

You can add custom commands specific to your area:

```python
import adventurelib as adv
from text_adv.engine import print_styled

@adv.when('dance')
def dance():
    """Perform a little dance."""
    print_styled("You do a little dance. How fun!", "success")
```

### Conditional Room Descriptions

Change room descriptions based on game state:

```python
def describe_room_based_on_state(room):
    """Customize room description based on game state."""
    if game_state.get_flag('lights_on'):
        return "The room is brightly lit, revealing colorful murals on the walls."
    else:
        return "The room is dark, with shadowy shapes suggesting decorations on the walls."
```

### Complex Puzzles

Create more complex puzzles that involve multiple items or steps:

```python
def solve_complex_puzzle():
    """Handle a multi-step puzzle solution."""
    if (game_state.get_flag('switch_1_activated') and 
        game_state.get_flag('switch_2_activated') and
        game_state.get_flag('switch_3_activated')):
        print_styled("As you activate the third switch, a mechanism whirs to life!", "success")
        print_styled("A hidden compartment opens in the wall, revealing a treasure.", "success")
        # Create and add a new reward item
        return True
    return False
```

## Conclusion

By following this tutorial, you've learned how to create your own area in Alpha Cloudplex. You've created rooms, items, NPCs, and puzzles, and connected them to the main game world.

Continue experimenting with different structures and interactions to create engaging and educational experiences for players!

Happy adventuring!