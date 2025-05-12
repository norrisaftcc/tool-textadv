"""
Interactive Learning Museum - A tutorial area for the Alpha Cloudplex text adventure.

This module implements a museum with different rooms that teach various aspects
of the text adventure system. Each room focuses on a specific concept like
inventory management, movement, or item interactions.
"""

from text_adv.engine import Room, Item, game_state, inventory, print_styled

def create_museum():
    """Create and return the Interactive Learning Museum area."""
    
    # === Create museum rooms ===
    
    # Entrance Hall
    entrance = Room("A grand entrance hall with marble floors and a high ceiling.")
    entrance.name = "Museum Entrance Hall"
    entrance.long_description = """You stand in the grand entrance hall of the Interactive Learning Museum.
Marble floors gleam beneath your feet, and informational plaques line the walls.
A large sign welcomes you to the museum and explains its purpose.
Doorways lead in several directions to different exhibit halls."""
    
    # Movement Exhibit
    movement_room = Room("A room dedicated to teaching navigation and movement.")
    movement_room.name = "Gallery of Movement"
    movement_room.long_description = """This gallery is designed to teach navigation through text adventures.
Large arrow symbols adorn the floor, pointing in various directions.
The walls are decorated with maps and diagrams showing various game worlds.
Interactive displays demonstrate different ways to move between rooms."""
    
    # Inventory Exhibit
    inventory_room = Room("A room filled with display cases showing various items.")
    inventory_room.name = "Hall of Inventory"
    inventory_room.long_description = """The Hall of Inventory showcases the principles of item management.
Glass display cases contain a variety of intriguing objects, each with a description.
Wall panels explain how to pick up, drop, and examine items in your adventures.
You notice several interactive demonstrations around the room."""
    
    # Items and Interactions Exhibit
    items_room = Room("A workshop-like room with various interactive displays.")
    items_room.name = "Chamber of Interactions"
    items_room.long_description = """The Chamber of Interactions demonstrates how objects can be used in game worlds.
Mechanical displays show items being combined and used on various targets.
The room has a hands-on feel, with several stations where you can try things yourself.
A section is dedicated to puzzle mechanics commonly found in text adventures."""
    
    # Game Creation Exhibit
    creation_room = Room("A bright room set up like a classroom or workshop.")
    creation_room.name = "Workshop of Creation"
    creation_room.long_description = """The Workshop of Creation is designed to teach you how to build your own adventures.
Workstations with code examples and diagrams line the walls.
The center of the room has a large interactive table with a glowing 3D model of a game world.
This is where visitors learn to create their own rooms, items, and puzzles."""
    
    # === Connect the rooms ===
    entrance.exits['north'] = movement_room
    entrance.exits['east'] = inventory_room
    entrance.exits['west'] = items_room
    entrance.exits['south'] = creation_room
    
    movement_room.exits['south'] = entrance
    inventory_room.exits['west'] = entrance
    items_room.exits['east'] = entrance
    creation_room.exits['north'] = entrance
    
    # === Create and place items ===
    
    # Entrance Hall items
    welcome_sign = Item("sign", "A large welcome sign with information about the museum.")
    welcome_sign.takeable = False
    welcome_sign.add_use_callback(lambda: read_welcome_sign())
    
    museum_map = Item("map", "A handy map of the museum's exhibits.")
    museum_map.add_use_callback(lambda: show_museum_map())
    
    entrance.add_item(welcome_sign)
    entrance.add_item(museum_map)
    
    # Movement Room items
    movement_guide = Item("guide", "An interactive guide to movement commands.")
    movement_guide.takeable = False
    movement_guide.add_use_callback(lambda: read_movement_guide())
    
    compass = Item("compass", "A golden compass that always points to the museum entrance.")
    compass.add_use_callback(lambda: use_compass())
    
    movement_room.add_item(movement_guide)
    movement_room.add_item(compass)
    
    # Inventory Room items
    inventory_plaque = Item("plaque", "A detailed plaque explaining inventory management.")
    inventory_plaque.takeable = False
    inventory_plaque.add_use_callback(lambda: read_inventory_plaque())
    
    sample_collection = Item("collection", "A collection of sample items in a small pouch.")
    sample_collection.add_use_callback(lambda: use_sample_collection())
    
    trinket = Item("trinket", "A small decorative trinket perfect for practicing inventory commands.")
    
    inventory_room.add_item(inventory_plaque)
    inventory_room.add_item(sample_collection)
    inventory_room.add_item(trinket)
    
    # Items Room items
    interaction_display = Item("display", "An interactive display showing item usage mechanics.")
    interaction_display.takeable = False
    interaction_display.add_use_callback(lambda: use_interaction_display())
    
    key = Item("key", "A small key that seems to fit a display case.")
    
    locked_case = Item("case", "A locked display case with something interesting inside.")
    locked_case.takeable = False
    
    items_room.add_item(interaction_display)
    items_room.add_item(key)
    items_room.add_item(locked_case)
    
    # Creation Room items
    creation_manual = Item("manual", "A comprehensive guide to creating your own text adventures.")
    creation_manual.takeable = False
    creation_manual.add_use_callback(lambda: read_creation_manual())
    
    notebook = Item("notebook", "A blank notebook for jotting down game ideas.")
    notebook.add_use_callback(lambda: use_notebook())
    
    creation_room.add_item(creation_manual)
    creation_room.add_item(notebook)
    
    # Setup key to unlock case interaction
    key.add_use_callback(lambda target: unlock_case(target), locked_case)
    
    # Return the entrance room
    return entrance

# === Item interaction callbacks ===

def read_welcome_sign():
    """Read the museum welcome sign."""
    print_styled("You read the large welcome sign:", "command")
    print_styled("=" * 60, "system")
    print_styled("WELCOME TO THE INTERACTIVE LEARNING MUSEUM", "header")
    print_styled("A hands-on guide to text adventure mechanics", "system")
    print_styled("-" * 60, "system")
    print_styled("This museum is designed to teach you how the Alpha Cloudplex text adventure system works through interactive exhibits.", "system")
    print_styled("\nOur exhibits include:", "system")
    print_styled("- Gallery of Movement: Learn navigation commands", "system")
    print_styled("- Hall of Inventory: Master item management", "system")
    print_styled("- Chamber of Interactions: Discover object interactions", "system")
    print_styled("- Workshop of Creation: Design your own adventures", "system")
    print_styled("\nFeel free to explore, interact with displays, and take items that aren't fixed in place.", "system")
    print_styled("=" * 60, "system")
    return True

def show_museum_map():
    """Display the museum map."""
    print_styled("You unfold the museum map:", "command")
    
    map_art = """
    .-----------------.    .-----------------.
    |                 |    |                 |
    | MOVEMENT ROOM   |    |  INVENTORY ROOM |
    |                 |    |                 |
    '---------^-------'    '--------^--------'
              |                     |
              |                     |
    .---------+---------------------+---------.
    |                                         |
    |             ENTRANCE HALL               |
    |                                         |
    .---------+---------------------+---------.
              |                     |
              |                     |
    .---------v-------'    '--------v--------'
    |                 |    |                 |
    |   ITEMS ROOM    |    | CREATION ROOM   |
    |                 |    |                 |
    '-----------------'    '-----------------'
    """
    
    print_styled(map_art, "hint")
    print_styled("\nThe map shows the five main exhibits of the museum.", "hint")
    print_styled("You are currently in the " + game_state.current_room.name + ".", "hint")
    return True

def read_movement_guide():
    """Read the movement guide in the movement room."""
    print_styled("You examine the interactive movement guide:", "command")
    print_styled("=" * 60, "system")
    print_styled("NAVIGATING YOUR TEXT ADVENTURE", "header")
    print_styled("-" * 60, "system")
    print_styled("In Alpha Cloudplex, you can move between locations using these commands:", "system")
    print_styled("\nBasic direction commands:", "system")
    print_styled("- north, south, east, west (or n, s, e, w for short)", "system")
    print_styled("- up, down (or u, d for short)", "system")
    print_styled("\nAlternative movement commands:", "system")
    print_styled("- go north, move east, walk west", "system")
    print_styled("\nTo see where you can go:", "system")
    print_styled("- look (shows the current room and available exits)", "system")
    print_styled("\nTry these commands to explore the museum!", "system")
    print_styled("=" * 60, "system")
    return True

def use_compass():
    """Use the compass item."""
    current_room = game_state.current_room
    
    direction_to_entrance = None
    for direction, room in current_room.exits.items():
        if hasattr(room, 'name') and room.name == "Museum Entrance Hall":
            direction_to_entrance = direction
            break
    
    print_styled("You check the compass...", "command")
    
    if direction_to_entrance:
        print_styled(f"The needle points {direction_to_entrance}, toward the Museum Entrance.", "success")
    else:
        print_styled("The needle spins around and points south, indicating the Museum Entrance is that way.", "success")
    
    return True

def read_inventory_plaque():
    """Read the inventory management plaque."""
    print_styled("You read the inventory management plaque:", "command")
    print_styled("=" * 60, "system")
    print_styled("INVENTORY MANAGEMENT", "header")
    print_styled("-" * 60, "system")
    print_styled("Your inventory is the collection of items you're carrying.", "system")
    print_styled("\nBasic inventory commands:", "system")
    print_styled("- inventory (or i for short): View what you're carrying", "system")
    print_styled("- take [item]: Pick up an item from the room", "system")
    print_styled("- get [item]: Same as take", "system")
    print_styled("- drop [item]: Remove an item from inventory and place it in the room", "system")
    print_styled("\nInteracting with items:", "system")
    print_styled("- examine [item]: Look at an item in detail", "system")
    print_styled("- look at [item]: Same as examine", "system")
    print_styled("\nTry picking up the trinket in this room!", "system")
    print_styled("=" * 60, "system")
    return True

def use_sample_collection():
    """Use the sample collection item."""
    print_styled("You open the sample collection pouch...", "command")
    print_styled("Inside are several tiny labeled items: a coin, a button, and a marble.", "success")
    print_styled("This is perfect for practicing inventory management!", "success")
    
    # Check if already used
    if game_state.get_flag('sample_collection_used'):
        print_styled("You've already removed the items from the pouch.", "hint")
        return True
    
    # Add the small items to the room
    current_room = game_state.current_room
    
    coin = Item("coin", "A small gold coin with the museum's logo.")
    button = Item("button", "A decorative button made of polished wood.")
    marble = Item("marble", "A glass marble with swirling colors inside.")
    
    current_room.add_item(coin)
    current_room.add_item(button)
    current_room.add_item(marble)
    
    # Remove the collection from inventory if it's there
    for item in inventory:
        if item.name == "collection":
            inventory.remove(item)
            break
    
    # Set flag so we don't duplicate items
    game_state.set_flag('sample_collection_used', True)
    
    print_styled("You emptied the pouch, placing the items on the floor.", "success")
    return True

def use_interaction_display():
    """Use the interaction display in the items room."""
    print_styled("You activate the interaction display:", "command")
    print_styled("=" * 60, "system")
    print_styled("ITEM INTERACTIONS", "header")
    print_styled("-" * 60, "system")
    print_styled("Items in text adventures can be used on their own or with other items.", "system")
    print_styled("\nBasic interaction commands:", "system")
    print_styled("- use [item]: Activate or use an item", "system")
    print_styled("- use [item] on [target]: Use an item on another item or object", "system")
    print_styled("- use [item] with [target]: Same as above", "system")
    print_styled("\nExample interactions:", "system")
    print_styled("- use key on door: Try to unlock a door with a key", "system")
    print_styled("- use map: Look at a map item", "system")
    print_styled("\nTry using the key on the locked case in this room!", "system")
    print_styled("=" * 60, "system")
    return True

def unlock_case(target):
    """Use the key to unlock the display case."""
    print_styled("You insert the key into the locked case...", "command")
    
    # Check if we're in the right room
    if game_state.current_room.name != "Chamber of Interactions":
        print_styled("There's no case here to unlock.", "error")
        return False
    
    # Check if already unlocked
    if game_state.get_flag('case_unlocked'):
        print_styled("The case is already unlocked.", "hint")
        return True
    
    print_styled("The key fits perfectly! You turn it and the case unlocks with a satisfying click.", "success")
    print_styled("Inside the case is a beautiful golden badge that reads 'Expert Adventurer'.", "success")
    
    # Add the badge to the room
    current_room = game_state.current_room
    badge = Item("badge", "A golden 'Expert Adventurer' badge. Wearing it shows you understand item interactions.")
    current_room.add_item(badge)
    
    # Update the case description
    for item in current_room.items:
        if item.name == "case":
            item.description = "An unlocked display case that previously held a badge."
            break
    
    # Set flag
    game_state.set_flag('case_unlocked', True)
    
    return True

def read_creation_manual():
    """Read the creation manual in the creation room."""
    print_styled("You page through the creation manual:", "command")
    print_styled("=" * 60, "system")
    print_styled("CREATING YOUR OWN ADVENTURES", "header")
    print_styled("-" * 60, "system")
    print_styled("The Alpha Cloudplex system makes it easy to create your own text adventures!", "system")
    print_styled("\nBasic steps to create an adventure:", "system")
    print_styled("1. Define rooms with descriptions", "system")
    print_styled("2. Connect rooms with exits", "system")
    print_styled("3. Create items and place them in rooms", "system")
    print_styled("4. Add callbacks for item interactions", "system")
    print_styled("5. Define any special commands or behaviors", "system")
    print_styled("\nExample code to create a simple room:", "system")
    print_styled("""
    # Create a simple room
    treasure_room = Room("A glittering chamber filled with gold and jewels.")
    treasure_room.name = "Dragon's Hoard"
    
    # Add an item to the room
    crown = Item("crown", "A magnificent golden crown encrusted with gems.")
    treasure_room.add_item(crown)
    """, "hint")
    print_styled("\nCheck out the TUTORIAL.md file for a comprehensive guide!", "system")
    print_styled("=" * 60, "system")
    return True

def use_notebook():
    """Use the notebook item for game ideas."""
    print_styled("You open the notebook and see blank pages ready for your game ideas.", "command")
    print_styled("This would be perfect for sketching out room layouts or writing item descriptions.", "success")
    
    # If in inventory, add some content
    found_in_inventory = False
    for item in inventory:
        if item.name == "notebook":
            found_in_inventory = True
            break
    
    if found_in_inventory:
        print_styled("\nYou decide to jot down a simple game structure:", "success")
        print_styled("""
        My Adventure Game:
        - Starting Room: Forest Clearing
        - Key Locations: Haunted Cabin, Underground Cave, Mountaintop
        - Main Items: Ancient Key, Magic Amulet, Cryptic Map
        - Puzzles: Unlock the cabin, decode the map, activate the amulet
        """, "hint")
        
        # Update description to reflect the notes
        for item in inventory:
            if item.name == "notebook":
                item.description = "A notebook with your game ideas sketched inside."
                break
    
    return True

def setup_museum_guide():
    """Set up a special NPC guide for the museum."""
    import adventurelib as adv
    
    @adv.when('talk to curator')
    @adv.when('speak to curator')
    def talk_to_curator():
        """Talk to the museum curator."""
        room = game_state.current_room
        
        if not room.name.startswith("Museum"):
            print_styled("There's no curator here.", "error")
            return
        
        print_styled('A holographic figure appears before you - the museum curator.', 'speech')
        print_styled('"Welcome to the Interactive Learning Museum! I\'m the curator."', 'speech')
        print_styled('"Feel free to explore our exhibits and interact with the displays."', 'speech')
        print_styled('"Each room teaches a different aspect of text adventures."', 'speech')
        print_styled('"If you have questions, just ask me about any exhibit!"', 'speech')

def initialize_museum():
    """Initialize the museum area and return the entrance room."""
    setup_museum_guide()
    return create_museum()