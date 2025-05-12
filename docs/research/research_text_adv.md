# From BASIC to Python: Crafting text adventures for the modern age

## Reviving a classic approach for today's programmers

Text adventures—also known as interactive fiction—are experiencing a renaissance in the coding education world. They combine storytelling with fundamental programming concepts, making them perfect for college freshmen learning Python. This guide bridges the gap between the influential 1983 Usborne book "Write Your Own Adventure Programs for Your Microcomputer" and modern Python programming, covering essential concepts while providing practical, beginner-friendly code examples.

The original Usborne book introduced thousands of young programmers to coding through text adventures on early microcomputers like the ZX Spectrum and Commodore 64. We'll modernize these concepts for Python while preserving the educational core that made these games such effective teaching tools.

## Understanding the Usborne approach

The 1983 "Write Your Own Adventure Programs" book focused on creating a text adventure called "Haunted House," teaching programming concepts through practical game development. The book used BASIC, the dominant beginner language of the era, with several core components:

### World representation
The original Usborne approach used numeric arrays to represent a game world as a grid—typically 8×8 rooms (64 total). Movement worked by adding or subtracting values from the player's current position variable (e.g., +8 to move north). Room descriptions were stored in DATA statements and accessed based on the player's location number.

```python
# Modern Python equivalent of the original BASIC room system
# Instead of a numeric grid, we'll use a dictionary of room objects

rooms = {
    'entrance': {
        'description': 'You stand at the entrance of a dark cave.',
        'exits': {'north': 'tunnel', 'west': 'forest'},
        'items': ['torch']
    },
    'tunnel': {
        'description': 'A narrow tunnel stretches before you, disappearing into darkness.',
        'exits': {'south': 'entrance', 'north': 'cavern'},
        'items': []
    }
}

# Current location tracked by room ID instead of numeric position
current_room = 'entrance'
```

### Object management
In the BASIC implementation, objects were represented by ID numbers, with their locations stored in arrays. An object with a location value of -1 was considered "in inventory." The game checked if objects were present in a room before allowing interactions with them.

```python
# Modern Python approach to items and inventory
items = {
    'torch': {
        'description': 'A wooden torch with a flickering flame.',
        'can_take': True
    },
    'key': {
        'description': 'A rusty iron key.',
        'can_take': True
    },
    'door': {
        'description': 'A heavy wooden door with iron hinges.',
        'can_take': False,
        'locked': True
    }
}

# Inventory as a simple list
inventory = []

def take_item(item_name):
    if item_name in rooms[current_room]['items']:
        if items[item_name]['can_take']:
            inventory.append(item_name)
            rooms[current_room]['items'].remove(item_name)
            print(f"You pick up the {item_name}.")
        else:
            print(f"You can't take the {item_name}.")
    else:
        print(f"There is no {item_name} here.")
```

### Player input handling
The Usborne book implemented a simple two-word parser (VERB NOUN) for commands. Input was processed as a string, separated into two parts, then matched against a vocabulary list. Common commands included movement directions and actions like TAKE, DROP, and LOOK.

## Designing a modern text adventure

### Game architecture overview

A well-structured Python text adventure separates concerns into distinct components:

1. **Game engine**: Manages the game loop and coordinates other components
2. **World model**: Represents rooms, connections, and objects
3. **Player**: Tracks inventory, status, and current location
4. **Parser**: Processes user commands and translates them into game actions
5. **Game state**: Tracks overall game progress and conditions

We'll use an object-oriented approach to organize these components while keeping the code beginner-friendly.

## World representation in Python

Modern Python text adventures typically use dictionaries or classes to represent rooms and their connections rather than the numeric grid from the Usborne approach.

### Dictionary-based approach

```python
# Simple dictionary-based world representation
def create_world():
    return {
        'hall': {
            'name': 'Grand Hall',
            'description': 'You stand in a grand entrance hall. Dusty portraits line the walls.',
            'exits': {'north': 'study', 'east': 'kitchen', 'south': 'garden'},
            'items': ['candle', 'matches']
        },
        'study': {
            'name': 'Study',
            'description': 'A cozy study with bookshelves and an old desk.',
            'exits': {'south': 'hall', 'east': 'laboratory'},
            'items': ['book', 'quill']
        },
        'kitchen': {
            'name': 'Kitchen',
            'description': 'An old kitchen with a large fireplace.',
            'exits': {'west': 'hall', 'north': 'pantry'},
            'items': ['knife', 'pot']
        }
    }
```

This approach is easier to understand for beginners than the original BASIC array method, while still being powerful enough to create complex games.

### Class-based approach

For a more structured approach, you can use classes to represent rooms:

```python
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}  # {"north": room_object, "south": room_object}
        self.items = []  # List of item names
    
    def add_exit(self, direction, room):
        self.exits[direction] = room
    
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    
    def describe(self):
        """Print full room description including exits and items"""
        print(self.name)
        print("=" * len(self.name))
        print(self.description)
        
        # List exits
        if self.exits:
            print("\nExits:")
            for direction in self.exits:
                print(f"  {direction}")
        
        # List items
        if self.items:
            print("\nYou see:")
            for item in self.items:
                print(f"  {item}")
```

You can then create and connect rooms like this:

```python
# Create rooms
hall = Room("Grand Hall", "You stand in a grand entrance hall. Dusty portraits line the walls.")
study = Room("Study", "A cozy study with bookshelves and an old desk.")
kitchen = Room("Kitchen", "An old kitchen with a large fireplace.")

# Connect rooms
hall.add_exit("north", study)
hall.add_exit("east", kitchen)
study.add_exit("south", hall)
kitchen.add_exit("west", hall)

# Add items
hall.add_item("candle")
hall.add_item("matches")
study.add_item("book")
kitchen.add_item("knife")
```

## Handling player movement

The original Usborne book handled movement by adding or subtracting values from a position variable. In our modern Python approach, we navigate between connected rooms by looking up the appropriate room in the exits dictionary.

```python
def move_player(direction):
    global current_room
    
    # Using dictionary-based world
    if direction in rooms[current_room]['exits']:
        current_room = rooms[current_room]['exits'][direction]
        display_room()
    else:
        print(f"You can't go {direction}.")

# For class-based rooms
def move_player_class_based(player, direction):
    if direction in player.location.exits:
        player.location = player.location.exits[direction]
        player.location.describe()
    else:
        print(f"You can't go {direction}.")
```

## Object and inventory management

The original Usborne approach used arrays to track object locations, with special values (-1) to indicate inventory. Our Python implementation uses more intuitive approaches:

### Simple inventory system

```python
def take_item(item_name):
    """Pick up an item from the current room and add it to inventory"""
    global inventory
    current_room_items = rooms[current_room]['items']
    
    if item_name in current_room_items:
        current_room_items.remove(item_name)
        inventory.append(item_name)
        print(f"You take the {item_name}.")
    else:
        print(f"There is no {item_name} here.")

def drop_item(item_name):
    """Drop an item from inventory into the current room"""
    global inventory
    if item_name in inventory:
        inventory.remove(item_name)
        rooms[current_room]['items'].append(item_name)
        print(f"You drop the {item_name}.")
    else:
        print(f"You don't have a {item_name}.")

def show_inventory():
    """Display the player's inventory"""
    if inventory:
        print("\nYou are carrying:")
        for item in inventory:
            print(f"- {item}")
    else:
        print("\nYour inventory is empty.")
```

### Class-based items and inventory

For more complex games, we can define an Item class:

```python
class Item:
    def __init__(self, name, description, can_take=True):
        self.name = name
        self.description = description
        self.can_take = can_take
    
    def examine(self):
        """Print the item description"""
        print(self.description)
    
    def use(self, player, target=None):
        """Default behavior when item is used"""
        print(f"You're not sure how to use the {self.name}.")

class Player:
    def __init__(self, name, starting_location):
        self.name = name
        self.location = starting_location
        self.inventory = []
    
    def take(self, item_name):
        """Take an item from the current room"""
        for item in self.location.items:
            if item.name.lower() == item_name.lower():
                if item.can_take:
                    self.location.items.remove(item)
                    self.inventory.append(item)
                    print(f"You take the {item.name}.")
                    return True
                else:
                    print(f"You can't take the {item.name}.")
                    return False
        print(f"There is no {item_name} here.")
        return False
    
    def drop(self, item_name):
        """Drop an item in the current room"""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                self.inventory.remove(item)
                self.location.items.append(item)
                print(f"You drop the {item.name}.")
                return True
        print(f"You don't have a {item_name}.")
        return False
```

## Command parsing

The original Usborne book used a simple two-word parser. We can implement something similar but with improved flexibility:

```python
def parse_command(command):
    """Parse a command into action and target"""
    words = command.lower().split()
    
    if not words:
        return (None, None)
    
    if len(words) == 1:
        return (words[0], None)
    else:
        # Join all words after the first as the target
        return (words[0], " ".join(words[1:]))

def process_command(command):
    """Process a command and call appropriate function"""
    action, target = parse_command(command)
    
    if action is None:
        return
    
    # Handle movement commands
    if action in ['go', 'move', 'walk']:
        if target:
            move_player(target)
        else:
            print("Go where?")
    elif action in ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west']:
        # Handle shortcut movement commands
        direction_map = {
            'n': 'north', 's': 'south', 
            'e': 'east', 'w': 'west'
        }
        direction = direction_map.get(action, action)
        move_player(direction)
    
    # Handle item interactions
    elif action in ['take', 'get', 'grab', 'pick']:
        if target:
            take_item(target)
        else:
            print("Take what?")
    elif action in ['drop', 'leave', 'put']:
        if target:
            drop_item(target)
        else:
            print("Drop what?")
    
    # Handle looking
    elif action in ['look', 'examine', 'inspect']:
        if target:
            examine_item(target)
        else:
            display_room()
    
    # Handle inventory
    elif action in ['inventory', 'i', 'items']:
        show_inventory()
    
    # Handle quit
    elif action in ['quit', 'exit', 'q']:
        return False
    
    # Unknown command
    else:
        print("I don't understand that command.")
    
    return True
```

## Game state management

The Usborne book tracked game state through various variables and flags. We can use a more structured approach:

```python
class GameState:
    def __init__(self):
        self.player = None
        self.rooms = {}
        self.items = {}
        self.game_running = True
        self.turns = 0
        self.flags = {
            'treasure_found': False,
            'door_unlocked': False,
            'ghost_encountered': False
        }
    
    def initialize_game(self):
        """Set up the initial game state"""
        # Create world
        self.create_world()
        
        # Create player in starting location
        self.player = Player("Adventurer", self.rooms['entrance'])
        
        # Place items in the world
        self.setup_items()
    
    def update(self):
        """Update game state after each turn"""
        self.turns += 1
        
        # Check special conditions
        if self.player.location == self.rooms['treasure_room'] and not self.flags['treasure_found']:
            print("You've found the legendary treasure! Congratulations!")
            self.flags['treasure_found'] = True
        
        # Check for game completion
        if self.flags['treasure_found'] and self.player.location == self.rooms['entrance']:
            print("You've escaped with the treasure! You win!")
            self.game_running = False
```

## Putting it all together: A complete mini-adventure

Here's a complete, playable text adventure that synthesizes all these concepts:

```python
def create_game():
    """Create and return a simple text adventure game"""
    # Create the game world
    rooms = {
        'entrance': {
            'name': 'Cave Entrance',
            'description': 'You stand at the entrance of a dark cave. Sunlight streams in from behind you.',
            'exits': {'north': 'tunnel'},
            'items': ['torch']
        },
        'tunnel': {
            'name': 'Narrow Tunnel',
            'description': 'A narrow, winding tunnel stretches before you.',
            'exits': {'south': 'entrance', 'east': 'cavern'},
            'items': ['rock']
        },
        'cavern': {
            'name': 'Large Cavern',
            'description': 'A large cavern with a high ceiling. Water drips somewhere in the darkness.',
            'exits': {'west': 'tunnel', 'north': 'treasure_room'},
            'items': ['key'],
            'locked': {'north': True}  # The north exit is locked
        },
        'treasure_room': {
            'name': 'Treasure Room',
            'description': 'A small chamber filled with gold and jewels!',
            'exits': {'south': 'cavern'},
            'items': ['treasure'],
            'win_condition': True  # Finding this room is required to win
        }
    }
    
    # Define items and their properties
    items = {
        'torch': {
            'description': 'A wooden torch with a flickering flame.',
            'can_take': True
        },
        'rock': {
            'description': 'A small, ordinary rock.',
            'can_take': True
        },
        'key': {
            'description': 'A rusty iron key.',
            'can_take': True
        },
        'treasure': {
            'description': 'A chest filled with gold coins and precious gems.',
            'can_take': True
        }
    }
    
    return rooms, items

def display_room(rooms, current_room):
    """Display the current room description, exits, and items"""
    room = rooms[current_room]
    
    print(f"\n{room['name']}")
    print("=" * len(room['name']))
    print(room['description'])
    
    # Display available exits
    exits = room['exits']
    if exits:
        print("\nExits:", end=" ")
        print(", ".join(exits.keys()))
    
    # Display items in the room
    items_in_room = room['items']
    if items_in_room:
        print("\nYou see:", end=" ")
        print(", ".join(items_in_room))

def play_game():
    """Main game function"""
    print("TEXT ADVENTURE GAME")
    print("==================")
    print("Enter commands to explore the cave.")
    print("Try: 'look', 'go [direction]', 'take [item]', 'use [item]', 'inventory', 'quit'")
    print("==================\n")
    
    # Initialize game
    rooms, items = create_game()
    current_room = 'entrance'
    inventory = []
    game_running = True
    found_treasure = False
    
    # Display initial room
    display_room(rooms, current_room)
    
    # Main game loop
    while game_running:
        # Get player command
        command = input("\n> ").lower()
        words = command.split()
        
        if not words:
            continue
        
        action = words[0]
        target = " ".join(words[1:]) if len(words) > 1 else None
        
        # Handle movement commands
        if action in ['go', 'move', 'north', 'south', 'east', 'west', 'n', 's', 'e', 'w']:
            # Map shorthand directions to full names
            direction_map = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
            direction = direction_map.get(action, action)
            
            # If it's a 'go' command, use the target as direction
            if direction in ['go', 'move'] and target:
                direction = target
            
            # Check if direction is valid
            if direction in rooms[current_room]['exits']:
                next_room = rooms[current_room]['exits'][direction]
                
                # Check for locked exits
                if 'locked' in rooms[current_room] and direction in rooms[current_room]['locked'] and rooms[current_room]['locked'][direction]:
                    if 'key' in inventory:
                        print("You unlock the door with your key and proceed.")
                        rooms[current_room]['locked'][direction] = False
                        current_room = next_room
                        display_room(rooms, current_room)
                    else:
                        print("The way is locked. You need a key.")
                else:
                    current_room = next_room
                    display_room(rooms, current_room)
                    
                    # Check win condition
                    if 'win_condition' in rooms[current_room] and 'treasure' in inventory:
                        print("\nCongratulations! You've found the treasure and made it back to the entrance! You win!")
                        game_running = False
            else:
                print(f"You can't go {direction}.")
        
        # Handle item commands
        elif action in ['take', 'get', 'pick']:
            if not target:
                print("Take what?")
                continue
                
            if target in rooms[current_room]['items']:
                if items[target]['can_take']:
                    inventory.append(target)
                    rooms[current_room]['items'].remove(target)
                    print(f"You take the {target}.")
                    
                    # Check if player has found the treasure
                    if target == 'treasure':
                        found_treasure = True
                        print("You've found the legendary treasure! Now find your way back to the entrance.")
                else:
                    print(f"You can't take the {target}.")
            else:
                print(f"There is no {target} here.")
                
        elif action in ['drop', 'put', 'leave']:
            if not target:
                print("Drop what?")
                continue
                
            if target in inventory:
                inventory.remove(target)
                rooms[current_room]['items'].append(target)
                print(f"You drop the {target}.")
            else:
                print(f"You don't have a {target}.")
        
        # Look around or examine something
        elif action in ['look', 'examine', 'inspect']:
            if not target:
                display_room(rooms, current_room)
            else:
                if target in rooms[current_room]['items']:
                    print(items[target]['description'])
                elif target in inventory:
                    print(items[target]['description'])
                else:
                    print(f"You don't see a {target} here.")
        
        # Display inventory
        elif action in ['inventory', 'i', 'items']:
            if inventory:
                print("\nYou are carrying:")
                for item in inventory:
                    print(f"- {item}")
            else:
                print("\nYour inventory is empty.")
        
        # Use an item
        elif action in ['use', 'activate']:
            if not target:
                print("Use what?")
                continue
                
            if target in inventory:
                if target == 'key' and current_room == 'cavern' and 'locked' in rooms[current_room] and 'north' in rooms[current_room]['locked']:
                    print("You use the key to unlock the northern passage.")
                    rooms[current_room]['locked']['north'] = False
                elif target == 'torch':
                    print("The torch illuminates your surroundings, making it easier to see.")
                else:
                    print(f"You're not sure how to use the {target} here.")
            else:
                print(f"You don't have a {target}.")
        
        # Quit the game
        elif action in ['quit', 'exit', 'q']:
            print("Thanks for playing!")
            game_running = False
        
        # Unknown command
        else:
            print("I don't understand that command.")

if __name__ == "__main__":
    play_game()
```

## Taking it further: Advanced concepts

Once you've mastered the basics, you can enhance your text adventure with:

1. **Class inheritance** for specialized items and rooms
2. **Event systems** for triggered actions and timed events
3. **More sophisticated parsing** using regular expressions
4. **Save/load functionality** using JSON serialization
5. **Dynamic world generation** for procedurally created adventures

### Specialized item example:

```python
class LightSource(Item):
    def __init__(self, name, description, can_take=True):
        super().__init__(name, description, can_take)
        self.is_lit = False
    
    def use(self, player, target=None):
        if not self.is_lit:
            self.is_lit = True
            print(f"You light the {self.name}.")
            player.has_light = True
        else:
            self.is_lit = False
            print(f"You extinguish the {self.name}.")
            player.has_light = False

class Key(Item):
    def __init__(self, name, description, lock_id):
        super().__init__(name, description)
        self.lock_id = lock_id
    
    def use(self, player, target=None):
        # Check if there's a locked door in the current room
        for item in player.location.items:
            if isinstance(item, Door) and item.lock_id == self.lock_id and item.locked:
                item.locked = False
                print(f"You unlock the {item.name} with the {self.name}.")
                return
        print("There's nothing here to unlock with this key.")
```

## Conclusion

We've translated the core concepts from the 1983 Usborne book "Write Your Own Adventure Programs for Your Microcomputer" into modern Python programming. By replacing BASIC arrays with dictionaries and objects, we've created more readable, maintainable code while preserving the educational value of text adventure game programming.

The fundamental principles behind text adventures—world modeling, state management, command parsing, and player interaction—remain as relevant today as they were in 1983. These concepts teach essential programming skills while allowing for creative expression.

As you continue developing your text adventure games, remember that the most important aspect is creating an engaging player experience. Focus on interesting locations, meaningful interactions, and challenging puzzles to make your game stand out.

Happy adventuring in Python!