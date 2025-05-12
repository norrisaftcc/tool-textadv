"""
Streamlit web interface for the text adventure game.
This module provides a web-based UI using Streamlit.
"""

import streamlit as st
import time
import re
from text_adv.engine import setup_game, game_state
from text_adv.boardwalk import initialize_boardwalk

# Custom CSS for styling
def load_css():
    """Load custom CSS for styling the app."""
    st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .room-name {
        color: #61dafb;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .room-description {
        color: #ffffff;
        font-size: 16px;
        margin-bottom: 15px;
    }
    .item-name {
        color: #f9c74f;
        font-weight: bold;
    }
    .command {
        color: #4ade80;
    }
    .error {
        color: #ef4444;
    }
    .success {
        color: #22c55e;
    }
    .hint {
        color: #d8b4fe;
        font-style: italic;
    }
    .speech {
        color: #38bdf8;
        font-style: italic;
    }
    .game-history {
        height: 400px;
        overflow-y: auto;
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .command-input {
        background-color: #2d3748;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

class StreamlitInterface:
    """Streamlit interface for the text adventure game."""
    
    def __init__(self):
        """Initialize the Streamlit interface."""
        self.setup_session_state()
        load_css()
        
    def setup_session_state(self):
        """Set up the session state variables."""
        if 'initialized' not in st.session_state:
            st.session_state.initialized = False
            st.session_state.game_output = []
            st.session_state.command_history = []
            st.session_state.inventory = []
            st.session_state.current_room = None
            st.session_state.player_name = "Adventurer"
            st.session_state.game_started = False
    
    def initialize_game(self):
        """Initialize the game world."""
        if not st.session_state.initialized:
            # Set up the game
            setup_game()
            
            # Initialize the Boardwalk area
            starting_room = initialize_boardwalk()
            
            # Store the current room in session state
            st.session_state.current_room = starting_room
            
            # Mark as initialized
            st.session_state.initialized = True
            
            # Add initial game output
            self.add_output("Welcome to Alpha Cloudplex!", "header")
            self.add_output("A text-based adventure where humans and AI interact on equal ground.", "normal")
            self.add_output("Type 'help' at any time to see available commands.", "hint")
    
    def add_output(self, text, style="normal"):
        """Add text to the game output history."""
        # Apply HTML styling based on the style
        if style == "room_name":
            styled_text = f'<div class="room-name">{text}</div>'
        elif style == "room_desc":
            styled_text = f'<div class="room-description">{text}</div>'
        elif style == "item_name":
            styled_text = f'<span class="item-name">{text}</span>'
        elif style == "command":
            styled_text = f'<span class="command">{text}</span>'
        elif style == "error":
            styled_text = f'<span class="error">{text}</span>'
        elif style == "success":
            styled_text = f'<span class="success">{text}</span>'
        elif style == "hint":
            styled_text = f'<span class="hint">{text}</span>'
        elif style == "speech":
            styled_text = f'<span class="speech">{text}</span>'
        elif style == "header":
            styled_text = f'<h2>{text}</h2>'
        else:
            styled_text = f'<div>{text}</div>'
        
        st.session_state.game_output.append(styled_text)
    
    def describe_current_room(self):
        """Describe the current room in the Streamlit interface."""
        room = st.session_state.current_room
        
        # Add room name
        if hasattr(room, 'name'):
            self.add_output(room.name, "room_name")
            self.add_output("=" * len(room.name), "room_name")
        
        # Add room description
        if room.first_visit and hasattr(room, 'long_description') and room.long_description:
            self.add_output(room.long_description, "room_desc")
            room.first_visit = False
        else:
            self.add_output(room.description, "room_desc")
        
        # List items
        if hasattr(room, 'items') and room.items:
            self.add_output("\nYou see:", "normal")
            for item in room.items:
                self.add_output(f"  {item}", "item_name")
        
        # List exits
        exits = []
        for direction, _ in room.exits.items():
            exits.append(direction)
        
        if exits:
            self.add_output("\nExits: " + ", ".join(exits), "normal")
    
    def handle_command(self, command):
        """Handle a player command in the Streamlit interface."""
        command = command.strip().lower()
        
        # Add command to history
        st.session_state.command_history.append(command)
        
        # Display the command
        self.add_output(f"> {command}", "command")
        
        # Handle specific commands
        if command == "look":
            self.describe_current_room()
        
        elif command == "inventory" or command == "i":
            self.show_inventory()
        
        elif command == "help":
            self.show_help()
        
        elif command.startswith("go ") or command in ["north", "south", "east", "west", "up", "down", "n", "s", "e", "w", "u", "d"]:
            self.handle_movement(command)
        
        elif command.startswith("take ") or command.startswith("get "):
            self.handle_take(command)
        
        elif command.startswith("drop "):
            self.handle_drop(command)
        
        elif command.startswith("examine ") or command.startswith("look at ") or command.startswith("inspect "):
            self.handle_examine(command)
        
        elif command.startswith("use "):
            self.handle_use(command)
        
        elif command.startswith("talk to ") or command.startswith("speak to "):
            self.handle_talk(command)
        
        else:
            self.add_output("I don't understand that command. Type 'help' for a list of commands.", "error")
    
    def show_inventory(self):
        """Show the player's inventory."""
        if not st.session_state.inventory:
            self.add_output("You're not carrying anything.", "hint")
            return
        
        self.add_output("You're carrying:", "normal")
        for item in st.session_state.inventory:
            self.add_output(f"  {item}", "item_name")
    
    def show_help(self):
        """Show available commands."""
        self.add_output("AVAILABLE COMMANDS", "header")
        commands = [
            ("look", "Look around the current location"),
            ("go [direction]", "Move in a direction (north, south, east, west, etc.)"),
            ("take [item]", "Pick up an item"),
            ("drop [item]", "Drop an item from your inventory"),
            ("inventory", "View your inventory (shortcut: 'i')"),
            ("examine [item]", "Look at an item in detail"),
            ("use [item]", "Use an item"),
            ("use [item] on/with [target]", "Use an item on a target"),
            ("talk to [person]", "Talk to someone"),
            ("help", "Show this help message")
        ]
        
        for cmd, desc in commands:
            self.add_output(f"{cmd}: {desc}", "normal")
    
    def handle_movement(self, command):
        """Handle movement commands."""
        # Extract direction from command
        if command.startswith("go "):
            direction = command[3:].strip()
        else:
            direction = command
        
        # Map shortcuts to full directions
        direction_map = {
            'n': 'north', 's': 'south', 'e': 'east', 'w': 'west',
            'u': 'up', 'd': 'down'
        }
        direction = direction_map.get(direction, direction)
        
        # Check if direction is valid
        room = st.session_state.current_room
        if direction in room.exits:
            # Move to the new room
            st.session_state.current_room = room.exits[direction]
            self.describe_current_room()
        else:
            self.add_output(f"You can't go {direction}.", "error")
    
    def handle_take(self, command):
        """Handle take/get commands."""
        # Extract item name
        match = re.match(r"(take|get)\s+(.+)", command)
        if not match:
            self.add_output("Take what?", "error")
            return
        
        item_name = match.group(2).strip()
        
        # Check if item is in the room
        room = st.session_state.current_room
        found_item = None
        
        if hasattr(room, 'items'):
            for item in room.items:
                if item.name.lower() == item_name.lower():
                    found_item = item
                    break
        
        if found_item:
            # Check if item is takeable
            if getattr(found_item, 'takeable', True):
                # Add to inventory
                st.session_state.inventory.append(found_item)
                # Remove from room
                room.items.remove(found_item)
                self.add_output(f"You take the {found_item}.", "success")
            else:
                self.add_output(f"You can't take the {found_item}.", "error")
        else:
            self.add_output(f"There's no {item_name} here.", "error")
    
    def handle_drop(self, command):
        """Handle drop commands."""
        # Extract item name
        match = re.match(r"drop\s+(.+)", command)
        if not match:
            self.add_output("Drop what?", "error")
            return
        
        item_name = match.group(1).strip()
        
        # Check if item is in inventory
        found_item = None
        for item in st.session_state.inventory:
            if item.name.lower() == item_name.lower():
                found_item = item
                break
        
        if found_item:
            # Remove from inventory
            st.session_state.inventory.remove(found_item)
            # Add to room
            room = st.session_state.current_room
            if not hasattr(room, 'items'):
                room.items = []
            room.items.append(found_item)
            self.add_output(f"You drop the {found_item}.", "success")
        else:
            self.add_output(f"You don't have a {item_name}.", "error")
    
    def handle_examine(self, command):
        """Handle examine/look at/inspect commands."""
        # Extract item name
        match = re.match(r"(examine|look at|inspect)\s+(.+)", command)
        if not match:
            self.add_output("Examine what?", "error")
            return
        
        item_name = match.group(2).strip()
        
        # Check if item is in inventory or room
        found_item = None
        
        # Check inventory
        for item in st.session_state.inventory:
            if item.name.lower() == item_name.lower():
                found_item = item
                break
        
        # Check room if not found in inventory
        if not found_item:
            room = st.session_state.current_room
            if hasattr(room, 'items'):
                for item in room.items:
                    if item.name.lower() == item_name.lower():
                        found_item = item
                        break
        
        if found_item:
            # Display item description
            if hasattr(found_item, 'description'):
                self.add_output(found_item.description, "normal")
            else:
                self.add_output(f"You see nothing special about the {found_item}.", "normal")
        else:
            self.add_output(f"You don't see a {item_name} here.", "error")
    
    def handle_use(self, command):
        """Handle use commands."""
        # Check for "use X on Y" pattern
        on_match = re.match(r"use\s+(.+?)\s+(?:on|with)\s+(.+)", command)
        if on_match:
            item_name = on_match.group(1).strip()
            target_name = on_match.group(2).strip()
            
            # This would need more complex implementation to handle item interactions
            self.add_output(f"You try to use the {item_name} on the {target_name}, but nothing happens.", "normal")
            return
        
        # Simple "use X" pattern
        match = re.match(r"use\s+(.+)", command)
        if not match:
            self.add_output("Use what?", "error")
            return
        
        item_name = match.group(1).strip()
        
        # Check if item is in inventory
        found_item = None
        for item in st.session_state.inventory:
            if item.name.lower() == item_name.lower():
                found_item = item
                break
        
        if found_item:
            # Call the item's use method if it exists
            if hasattr(found_item, 'on_use'):
                found_item.on_use()
            else:
                self.add_output(f"You're not sure how to use the {found_item}.", "normal")
        else:
            self.add_output(f"You don't have a {item_name}.", "error")
    
    def handle_talk(self, command):
        """Handle talk to/speak to commands."""
        # Extract person name
        match = re.match(r"(?:talk|speak)\s+to\s+(.+)", command)
        if not match:
            self.add_output("Talk to whom?", "error")
            return
        
        person_name = match.group(1).strip()
        
        # Check if person is in the room
        room = st.session_state.current_room
        found_npc = None
        
        if hasattr(room, 'items'):
            for item in room.items:
                if item.name.lower() == person_name.lower() and not getattr(item, 'takeable', True):
                    found_npc = item
                    break
        
        if found_npc:
            # Handle specific NPCs
            if person_name.lower() == "guide":
                self.add_output('The guide turns to you with a friendly smile.', 'speech')
                self.add_output('"Welcome to the Logic Labyrinth! This maze is designed to help you practice navigation commands."', 'speech')
                self.add_output('"To move around, you can use commands like NORTH, SOUTH, EAST, and WEST, or the shortcuts N, S, E, and W."', 'speech')
                self.add_output('"You can also use GO DIRECTION, like GO NORTH."', 'speech')
                self.add_output('"Would you like to enter the maze? It\'s a great way to practice movement!"', 'speech')
                
            elif person_name.lower() == "vendor":
                self.add_output('The vendor waves cheerfully.', 'speech')
                self.add_output('"Welcome to Binary Bites! All our food may be virtual, but the experience is real!"', 'speech')
                self.add_output('"Our cotton candy is particularly popular. It\'s as sweet as real sugar, without the calories!"', 'speech')
                self.add_output('"Feel free to browse around. Everything here is free - it\'s just data, after all!"', 'speech')
                
            else:
                self.add_output(f"You try to talk to the {person_name}, but they don't respond.", "error")
        else:
            self.add_output(f"There's no {person_name} here to talk to.", "error")
    
    def render(self):
        """Render the Streamlit interface."""
        st.title("Alpha Cloudplex")
        st.subheader("A Text Adventure Where Reality and Simulation Meet")
        
        # Initialize the game if not already
        self.initialize_game()
        
        # Get player name if game not started
        if not st.session_state.game_started:
            with st.form("start_game"):
                player_name = st.text_input("What is your name, adventurer?", value="Adventurer")
                submit_button = st.form_submit_button("Begin Adventure")
                
                if submit_button:
                    st.session_state.player_name = player_name if player_name.strip() else "Adventurer"
                    st.session_state.game_started = True
                    game_state.player_name = st.session_state.player_name
                    self.add_output(f"Welcome, {st.session_state.player_name}! Your adventure is about to begin...", "success")
                    self.describe_current_room()
        
        # Display game content if game started
        if st.session_state.game_started:
            # Display game output
            game_output_html = "".join(st.session_state.game_output)
            st.markdown(f'<div class="game-history">{game_output_html}</div>', unsafe_allow_html=True)
            
            # Command input
            with st.form("command_form", clear_on_submit=True):
                cols = st.columns([4, 1])
                with cols[0]:
                    command = st.text_input("What would you like to do?", key="command_input")
                with cols[1]:
                    submit = st.form_submit_button("Submit")
                
                if submit and command:
                    self.handle_command(command)
                    st.experimental_rerun()

def main():
    """Main function to run the Streamlit app."""
    interface = StreamlitInterface()
    interface.render()

if __name__ == "__main__":
    main()