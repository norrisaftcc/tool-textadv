"""
Boardwalk area implementation - the starting area for the game.
"""

import random
from text_adv.engine import Room, Item, game_state, inventory

def create_boardwalk():
    """Create the Boardwalk area rooms and items."""
    
    # Create rooms
    pier_end = Room("You stand at the end of a long wooden pier. The ocean stretches out before you, waves gently lapping against the pilings below.")
    pier_end.name = "Pier End"
    pier_end.long_description = """You stand at the end of a long wooden pier extending out over the ocean. 
Waves gently lap against the pilings below, creating a soothing rhythm. 
The weathered boards creak slightly beneath your feet. 
To the north, you can see the bustling boardwalk with its colorful attractions."""
    
    boardwalk = Room("A lively boardwalk stretches east and west, filled with games, rides, and various attractions.")
    boardwalk.name = "Boardwalk"
    boardwalk.long_description = """The boardwalk is alive with activity. Colorful booths line both sides, 
offering games of chance and skill. The smell of cotton candy and popcorn fills the air. 
Music plays from somewhere nearby, adding to the carnival atmosphere. 
People and what appear to be AI entities mingle freely, enjoying the attractions."""
    
    arcade = Room("A retro arcade filled with vintage video games and new holographic experiences.")
    arcade.name = "Pixel Palace Arcade"
    arcade.long_description = """The arcade is a blend of nostalgia and futuristic technology. 
Classic cabinet games from the 1980s stand alongside advanced holographic gaming stations. 
The room pulses with electronic sounds and flashing lights. 
A large sign overhead reads 'PIXEL PALACE: WHERE REALITY IS WHAT YOU MAKE IT'."""
    
    food_court = Room("A bustling food court with various virtual food stalls.")
    food_court.name = "Binary Bites Food Court"
    food_court.long_description = """The food court is a sensory delight, despite being entirely virtual. 
Stalls offer everything from classic carnival treats to exotic cuisine from around the world. 
AI vendors cheerfully take orders while patrons sit at tables enjoying conversations.
A large fountain in the center features a statue of a person and robot sharing a meal."""
    
    maze_entrance = Room("The entrance to what appears to be a simple maze attraction.")
    maze_entrance.name = "Logic Labyrinth Entrance"
    maze_entrance.long_description = """A colorful archway marks the entrance to 'THE LOGIC LABYRINTH'. 
A sign explains this is a tutorial area designed to help newcomers learn the basic navigation commands.
An AI guide with a glowing blue outline stands nearby, ready to offer assistance.
A map on the wall shows the layout of a simple maze beyond the entrance."""
    
    # Connect rooms
    pier_end.exits['north'] = boardwalk
    boardwalk.exits['south'] = pier_end
    boardwalk.exits['east'] = food_court
    boardwalk.exits['west'] = arcade
    boardwalk.exits['north'] = maze_entrance
    food_court.exits['west'] = boardwalk
    arcade.exits['east'] = boardwalk
    maze_entrance.exits['south'] = boardwalk
    
    # Create items
    welcome_pamphlet = Item("pamphlet", "A colorful pamphlet titled 'Welcome to Alpha Cloudplex!'")
    welcome_pamphlet.add_use_callback(lambda: read_pamphlet())
    
    token = Item("token", "A shiny arcade token with 'Pixel Palace' embossed on one side.")
    
    cotton_candy = Item("cotton candy", "A fluffy cloud of pink cotton candy on a paper cone.")
    cotton_candy.add_use_callback(lambda: eat_cotton_candy())
    
    map_item = Item("map", "A simple map of the boardwalk area.")
    map_item.add_use_callback(lambda: show_map())
    
    # Add items to rooms
    pier_end.add_item(welcome_pamphlet)
    arcade.add_item(token)
    food_court.add_item(cotton_candy)
    boardwalk.add_item(map_item)
    
    # Add NPCs (represented as items for now)
    guide = Item("guide", "An AI guide with a friendly blue glow. You can TALK TO GUIDE.")
    guide.takeable = False
    maze_entrance.add_item(guide)
    
    vendor = Item("vendor", "A cheerful food vendor. You can TALK TO VENDOR.")
    vendor.takeable = False
    food_court.add_item(vendor)
    
    return pier_end

# Callback functions for items
def read_pamphlet():
    """Read the welcome pamphlet."""
    from text_adv.engine import print_styled
    
    print_styled("You open the pamphlet and read:", "command")
    print_styled("=" * 50, "system")
    print_styled("WELCOME TO ALPHA CLOUDPLEX", "header")
    print_styled("Where Reality and Simulation Meet!", "system")
    print_styled("-" * 50, "system")
    print_styled("Alpha Cloudplex is a simulation that knows it's a simulation, where humans and AI interact on equal ground.", "system")
    print_styled("The Boardwalk is your entry point to our world. Here you'll find:", "system")
    print_styled("  * Tutorial attractions to learn the basics", "system")
    print_styled("  * Gateways to other simulated environments", "system")
    print_styled("  * Social spaces to meet other entities", "system")
    print_styled("-" * 50, "system")
    print_styled("Enjoy your stay!", "system")
    print_styled("=" * 50, "system")
    return True

def eat_cotton_candy():
    """Eat the cotton candy."""
    from text_adv.engine import print_styled
    
    print_styled("You take a bite of the cotton candy.", "success")
    print_styled("It dissolves instantly on your tongue with a burst of sweetness.", "success")
    print_styled("Even though this is a simulation, the taste is remarkably realistic!", "hint")
    
    # Remove from inventory after eating
    for item in inventory:
        if item.name == "cotton candy":
            inventory.remove(item)
            break
    
    return True

def show_map():
    """Show the boardwalk map."""
    from text_adv.engine import print_styled
    
    map_art = """
    .---------.    .---------------.    .-------------.
    |  Arcade  |----| BOARDWALK    |----| Food Court  |
    '---------'    |   CENTRAL     |    '-------------'
                   |               |
                   |               |
                   .---------------.
                          |
                          |
                   .---------------.
                   |   MAZE        |
                   |   ENTRANCE    |
                   '---------------'
                          |
                          |
                          v
                      (Maze...)
                          |
                          |
                   .---------------.
                   |    PIER       |
                   |    END        |
                   '---------------'
                          |
                          v
                        OCEAN
    """
    
    print_styled("You examine the map of the boardwalk area:", "command")
    print_styled(map_art, "hint")
    return True

# Additional functions for NPC interactions
def setup_npc_interactions():
    """Set up NPC interaction commands."""
    import adventurelib as adv
    from text_adv.engine import print_styled
    
    @adv.when('talk to PERSON')
    @adv.when('speak to PERSON')
    @adv.when('ask PERSON')
    def talk_to(person):
        """Talk to an NPC."""
        room = game_state.current_room
        
        person_lower = person.lower()
        
        # Check if the NPC is in the current room
        found = False
        for item in room.items:
            if item.name.lower() == person_lower and not item.takeable:
                found = True
                break
        
        if not found:
            print_styled(f"There's no {person} here to talk to.", "error")
            return
        
        # Guide dialogue
        if person_lower == "guide":
            print_styled('The guide turns to you with a friendly smile.', 'speech')
            print_styled('"Welcome to the Logic Labyrinth! This maze is designed to help you practice navigation commands."', 'speech')
            print_styled('"To move around, you can use commands like NORTH, SOUTH, EAST, and WEST, or the shortcuts N, S, E, and W."', 'speech')
            print_styled('"You can also use GO DIRECTION, like GO NORTH."', 'speech')
            print_styled('"Would you like to enter the maze? It\'s a great way to practice movement!"', 'speech')
            
        # Vendor dialogue
        elif person_lower == "vendor":
            print_styled('The vendor waves cheerfully.', 'speech')
            print_styled('"Welcome to Binary Bites! All our food may be virtual, but the experience is real!"', 'speech')
            print_styled('"Our cotton candy is particularly popular. It\'s as sweet as real sugar, without the calories!"', 'speech')
            print_styled('"Feel free to browse around. Everything here is free - it\'s just data, after all!"', 'speech')
            
        else:
            print_styled(f"You try to talk to the {person}, but they don't respond.", "error")

def initialize_boardwalk():
    """Initialize the boardwalk area and return the starting room."""
    setup_npc_interactions()
    return create_boardwalk()