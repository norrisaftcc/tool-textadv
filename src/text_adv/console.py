"""
Console interface for the text adventure game.
This module provides the terminal-based UI implementation.
"""

import os
import sys
import time
from colorama import init, Fore, Back, Style

from text_adv.engine import (
    set_current_room, start_game, setup_game,
    print_styled, ColorTheme, current_theme, game_state
)

# Initialize colorama
init(autoreset=True)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.03, style_name=None):
    """Print text slowly, character by character, with optional styling."""
    if style_name and style_name in current_theme:
        text = current_theme[style_name] + text
    
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_title(title_text, border_char='=', padding=1, style_name="header"):
    """Print a stylized title block."""
    width = len(title_text) + (padding * 2)
    
    if style_name and style_name in current_theme:
        border = current_theme[style_name] + (border_char * width)
        padded_title = current_theme[style_name] + (
            border_char * padding + 
            title_text + 
            border_char * padding
        )
    else:
        border = border_char * width
        padded_title = border_char * padding + title_text + border_char * padding
    
    print(border)
    print(padded_title)
    print(border)

def print_ascii_art(art_file):
    """Print ASCII art from a file."""
    try:
        with open(art_file, 'r') as f:
            art = f.read()
        print(art)
    except FileNotFoundError:
        print(f"ASCII art file not found: {art_file}")

def show_intro():
    """Display game introduction and title screen."""
    clear_screen()
    
    # Try to load ASCII art title if available
    ascii_art_path = os.path.join(os.path.dirname(__file__), 'assets', 'title.txt')
    if os.path.exists(ascii_art_path):
        print_ascii_art(ascii_art_path)
    else:
        print_title("ALPHA CLOUDPLEX", "=", 3, "header")
    
    print()
    slow_print("Welcome to the Alpha Cloudplex Text Adventure!", delay=0.02, style_name="system")
    print()
    slow_print("A text-based adventure where humans and AI interact on equal ground.", delay=0.02)
    print()
    slow_print("Type 'help' at any time to see available commands.", delay=0.02, style_name="hint")
    print()
    
    # Get player name
    print_styled("What is your name, adventurer?", "command")
    player_name = input("> ")
    game_state.player_name = player_name if player_name.strip() else "Adventurer"
    
    print()
    slow_print(f"Welcome, {game_state.player_name}! Your adventure is about to begin...", delay=0.03, style_name="success")
    print()
    input("Press Enter to continue...")

def setup_help_command():
    """Set up the help command."""
    import adventurelib as adv
    
    @adv.when('help')
    def help_command():
        """Show available commands."""
        print_title("AVAILABLE COMMANDS", "-", 1, "header")
        commands = [
            ("look", "Look around the current location"),
            ("go [direction]", "Move in a direction (north, south, east, west, etc.)"),
            ("take [item]", "Pick up an item"),
            ("drop [item]", "Drop an item from your inventory"),
            ("inventory", "View your inventory (shortcut: 'i')"),
            ("examine [item]", "Look at an item in detail"),
            ("use [item]", "Use an item"),
            ("use [item] on/with [target]", "Use an item on a target"),
            ("help", "Show this help message"),
            ("quit", "Exit the game")
        ]
        
        for cmd, desc in commands:
            print(f"{current_theme['command']}{cmd}{Style.RESET_ALL}: {desc}")

def run_game():
    """Main function to run the console-based game."""
    # Show intro
    show_intro()
    
    # Clear screen before starting
    clear_screen()
    
    # Set up custom help command
    setup_help_command()
    
    # Set up the game world
    setup_game()
    
    # Start the game loop
    start_game()

if __name__ == "__main__":
    run_game()