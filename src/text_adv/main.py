"""
Main entry point for the text adventure game.
This module integrates all components and starts the game.
"""

from text_adv.engine import setup_game as engine_setup, set_current_room
from text_adv.console import run_game
from text_adv.boardwalk import initialize_boardwalk
from text_adv.museum import initialize_museum

def setup_game():
    """Set up the game world."""
    # Initialize the Boardwalk area
    boardwalk_start = initialize_boardwalk()
    
    # Initialize the Museum area
    museum_start = initialize_museum()
    
    # Connect the Boardwalk to the Museum
    # Find the arcade room in the Boardwalk to connect
    for direction, room in boardwalk_start.exits.items():
        if hasattr(room, 'name') and "Arcade" in room.name:
            arcade_room = room
            arcade_room.exits['up'] = museum_start
            museum_start.exits['down'] = arcade_room
            museum_start.add_item_to_content("A small sign notes that you can return to the Boardwalk by going DOWN.")
            break
    
    # Set the player's starting location
    set_current_room(boardwalk_start)

def main():
    """Main function to start the game."""
    # Set up the core engine
    engine_setup()
    
    # Override with our specific setup
    setup_game()
    
    # Run the console-based game
    run_game()

if __name__ == "__main__":
    main()