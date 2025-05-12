"""
Tests for the command handlers of the text adventure engine.

These tests ensure that the command system processes user input correctly.
"""

import unittest
from unittest.mock import patch, MagicMock, call
import adventurelib as adv

from text_adv.engine import (
    Room, Item, GameState, inventory,
    look, show_inventory, take, drop, examine, use, use_on, go, go_direction,
    game_state
)

class TestCommandHandlers(unittest.TestCase):
    """Tests for the command handlers."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset the game state for testing
        GameState._instance = None
        self.test_game_state = GameState()
        
        # Create test rooms
        self.room1 = Room("Test Room 1")
        self.room1.name = "Test Room 1"
        
        self.room2 = Room("Test Room 2")
        self.room2.name = "Test Room 2"
        
        # Connect the rooms
        self.room1.exits['north'] = self.room2
        self.room2.exits['south'] = self.room1
        
        # Create test items
        self.key = Item("key", "A test key.")
        self.door = Item("door", "A test door.")
        self.door.takeable = False
        
        # Add items to rooms
        self.room1.add_item(self.key)
        self.room2.add_item(self.door)
        
        # Set current room
        game_state.current_room = self.room1
        
        # Clear inventory
        inventory.clear()
        
    @patch('text_adv.engine.print_styled')
    def test_look_command(self, mock_print):
        """Test the look command."""
        # Mock the describe method to avoid stdout pollution
        original_describe = self.room1.describe
        self.room1.describe = MagicMock()
        
        # Call the look command
        look()
        
        # Check if describe was called
        self.room1.describe.assert_called_once()
        
        # Restore original method
        self.room1.describe = original_describe
        
    @patch('text_adv.engine.print_styled')
    def test_inventory_command(self, mock_print):
        """Test the inventory command."""
        # Empty inventory
        show_inventory()
        mock_print.assert_called_with("You're not carrying anything.", "hint")
        
        # Add an item to inventory
        inventory.add(self.key)
        mock_print.reset_mock()
        
        # Show inventory with item
        show_inventory()
        mock_print.assert_any_call("You're carrying:", "command")
        
    @patch('text_adv.engine.print_styled')
    @patch('text_adv.engine.adv.match_item', side_effect=lambda name, items: next((i for i in items if i.name == name), None))
    def test_take_command(self, mock_match, mock_print):
        """Test the take command."""
        # Take a nonexistent item
        take("nonexistent")
        mock_print.assert_called_with("There's no nonexistent here.", "error")
        
        # Take the key
        take("key")
        mock_print.assert_called_with("You take the key.", "success")
        
        # Check that key was moved to inventory
        self.assertIn(self.key, inventory)
        self.assertNotIn(self.key, self.room1.items)
        
        # Try to take an untakeable item
        game_state.current_room = self.room2
        take("door")
        mock_print.assert_called_with("You can't take the door.", "error")
        
    @patch('text_adv.engine.print_styled')
    @patch('text_adv.engine.adv.match_item', side_effect=lambda name, items: next((i for i in items if i.name == name), None))
    def test_drop_command(self, mock_match, mock_print):
        """Test the drop command."""
        # Drop a nonexistent item
        drop("nonexistent")
        mock_print.assert_called_with("You don't have a nonexistent.", "error")
        
        # Add key to inventory
        inventory.add(self.key)
        self.room1.items.remove(self.key)
        
        # Drop the key
        drop("key")
        mock_print.assert_called_with("You drop the key.", "success")
        
        # Check that key was moved from inventory to room
        self.assertNotIn(self.key, inventory)
        self.assertIn(self.key, game_state.current_room.items)
        
    @patch('text_adv.engine.print_styled')
    @patch('text_adv.engine.adv.match_item', side_effect=lambda name, items: next((i for i in items if i.name == name), None))
    def test_examine_command(self, mock_match, mock_print):
        """Test the examine command."""
        # Setup mock for describe method
        original_describe = self.key.describe
        self.key.describe = MagicMock()
        
        # Examine a nonexistent item
        examine("nonexistent")
        mock_print.assert_called_with("You don't see a nonexistent here.", "error")
        
        # Examine item in room
        examine("key")
        self.key.describe.assert_called_once()
        
        # Examine item in inventory
        self.key.describe.reset_mock()
        inventory.add(self.key)
        self.room1.items.remove(self.key)
        
        examine("key")
        self.key.describe.assert_called_once()
        
        # Restore original method
        self.key.describe = original_describe
        
    @patch('text_adv.engine.print_styled')
    @patch('text_adv.engine.adv.match_item', side_effect=lambda name, items: next((i for i in items if i.name == name), None))
    def test_use_command(self, mock_match, mock_print):
        """Test the use command."""
        # Setup mock for on_use method
        original_on_use = self.key.on_use
        self.key.on_use = MagicMock(return_value=True)
        
        # Use a nonexistent item
        use("nonexistent")
        mock_print.assert_called_with("You don't have a nonexistent.", "error")
        
        # Use item in inventory
        inventory.add(self.key)
        use("key")
        self.key.on_use.assert_called_once()
        
        # Restore original method
        self.key.on_use = original_on_use
        
    @patch('text_adv.engine.print_styled')
    @patch('text_adv.engine.adv.match_item', side_effect=lambda name, items: next((i for i in items if i.name == name), None))
    def test_use_on_command(self, mock_match, mock_print):
        """Test the use_on command."""
        # Setup mock for on_use method
        original_on_use = self.key.on_use
        self.key.on_use = MagicMock(return_value=True)
        
        # Move to room with door
        game_state.current_room = self.room2
        
        # Use a nonexistent item
        use_on("nonexistent", "door")
        mock_print.assert_called_with("You don't have a nonexistent.", "error")
        
        # Use item on nonexistent target
        inventory.add(self.key)
        use_on("key", "nonexistent")
        mock_print.assert_called_with("You don't see a nonexistent here.", "error")
        
        # Use item on target
        use_on("key", "door")
        self.key.on_use.assert_called_once_with(self.door)
        
        # Restore original method
        self.key.on_use = original_on_use
        
    @patch('text_adv.engine.print_styled')
    def test_go_command(self, mock_print):
        """Test the go command."""
        # Mock describe to avoid stdout pollution
        original_describe = self.room2.describe
        self.room2.describe = MagicMock()
        
        # Go in a valid direction
        go("north")
        self.assertEqual(game_state.current_room, self.room2)
        self.room2.describe.assert_called_once()
        
        # Go in an invalid direction
        go("east")
        mock_print.assert_called_with("You can't go east.", "error")
        
        # Restore original method
        self.room2.describe = original_describe
        
    @patch('text_adv.engine.go')
    def test_go_direction_command(self, mock_go):
        """Test the go_direction command."""
        # Test various movement commands
        go_direction("north")
        mock_go.assert_called_with("north")
        
        go_direction("n")
        mock_go.assert_called_with("north")
        
        go_direction("invalid")
        mock_go.assert_not_called()

if __name__ == '__main__':
    unittest.main()