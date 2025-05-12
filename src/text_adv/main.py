"""
Main entry point for the text adventure game.
This module integrates all components and starts the game.
"""

from text_adv.engine import setup_game as engine_setup, set_current_room
from text_adv.console import run_game
from text_adv.boardwalk import initialize_boardwalk

def setup_game():
    """Set up the game world."""
    # Initialize the Boardwalk area
    starting_room = initialize_boardwalk()
    
    # Set the player's starting location
    set_current_room(starting_room)

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