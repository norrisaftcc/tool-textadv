"""
Tests for the text adventure engine.

These tests ensure that the core functionality of the engine works correctly.
"""

import unittest
from unittest.mock import patch, MagicMock

from text_adv.engine import (
    Room, Item, GameState, inventory, 
    print_styled, current_theme, game_state
)

class TestRoom(unittest.TestCase):
    """Tests for the Room class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.room = Room("A test room.")
        self.room.name = "Test Room"
        self.room.long_description = "This is a long description for testing."
        
        self.other_room = Room("Another test room.")
        self.other_room.name = "Other Room"
        
    def test_room_creation(self):
        """Test that a room can be created with basic properties."""
        self.assertEqual(self.room.description, "A test room.")
        self.assertEqual(self.room.name, "Test Room")
        self.assertEqual(self.room.long_description, "This is a long description for testing.")
        self.assertEqual(self.room.short_description, "A test room.")
        self.assertTrue(self.room.first_visit)
        self.assertEqual(self.room.visit_count, 0)
        
    def test_room_exits(self):
        """Test that rooms can be connected with exits."""
        # In adventurelib, exits is a method, not a dictionary
        # You have to set the attribute directly for named exits
        setattr(self.room, 'north', self.other_room)
        setattr(self.other_room, 'south', self.room)

        self.assertEqual(self.room.exit('north'), self.other_room)
        self.assertEqual(self.other_room.exit('south'), self.room)
        
    def test_add_item(self):
        """Test that items can be added to a room."""
        item = Item("test_item", "A test item.")
        self.room.add_item(item)

        # Check that an item with the same name is in the room
        found = False
        for i in self.room.items:
            if i.name == item.name:
                found = True
                break
        self.assertTrue(found)

    def test_remove_item(self):
        """Test that items can be removed from a room."""
        item = Item("test_item", "A test item.")
        self.room.add_item(item)
        self.room.remove_item(item)

        # Check that no item with the same name is in the room
        found = False
        for i in self.room.items:
            if i.name == item.name:
                found = True
                break
        self.assertFalse(found)
        
    def test_add_item_to_content(self):
        """Test that content can be added to room descriptions."""
        additional_content = "There's a new feature in this room."
        self.room.add_item_to_content(additional_content)
        
        self.assertIn(additional_content, self.room.long_description)
        self.assertIn(additional_content, self.room.short_description)

class TestItem(unittest.TestCase):
    """Tests for the Item class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.item = Item("test_item", "A test item for testing.")
        
    def test_item_creation(self):
        """Test that an item can be created with basic properties."""
        self.assertEqual(self.item.name, "test_item")
        self.assertEqual(self.item.description, "A test item for testing.")
        self.assertTrue(self.item.takeable)
        self.assertFalse(self.item.hidden)
        
    def test_item_callbacks(self):
        """Test that callbacks can be added to items."""
        callback_called = [False]
        
        def test_callback():
            callback_called[0] = True
            return True
        
        self.item.add_use_callback(test_callback)
        
        # Test the callback
        result = self.item.on_use()
        self.assertTrue(result)
        self.assertTrue(callback_called[0])
        
    def test_targeted_callbacks(self):
        """Test that targeted callbacks work correctly."""
        target_item = Item("target", "A target item.")
        
        target_callback_called = [False]
        default_callback_called = [False]
        
        def target_callback():
            target_callback_called[0] = True
            return True
            
        def default_callback():
            default_callback_called[0] = True
            return True
        
        # Add callbacks
        self.item.add_use_callback(default_callback)
        self.item.add_use_callback(target_callback, target_item)
        
        # Test targeted callback
        result = self.item.on_use(target_item)
        self.assertTrue(result)
        self.assertTrue(target_callback_called[0])
        self.assertFalse(default_callback_called[0])
        
        # Reset and test default callback
        target_callback_called[0] = False
        result = self.item.on_use()
        self.assertTrue(result)
        self.assertFalse(target_callback_called[0])
        self.assertTrue(default_callback_called[0])

class TestGameState(unittest.TestCase):
    """Tests for the GameState class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset the singleton for testing
        GameState._instance = None
        self.game_state = GameState()
        
    def test_singleton_pattern(self):
        """Test that GameState follows the singleton pattern."""
        second_instance = GameState()
        self.assertIs(self.game_state, second_instance)
        
    def test_flags(self):
        """Test that flags can be set and retrieved."""
        self.game_state.set_flag('test_flag')
        self.assertTrue(self.game_state.get_flag('test_flag'))
        
        self.game_state.set_flag('value_flag', False)
        self.assertFalse(self.game_state.get_flag('value_flag'))
        
        # Test default value
        self.assertFalse(self.game_state.get_flag('nonexistent_flag'))
        self.assertEqual(self.game_state.get_flag('nonexistent_flag', 'default'), 'default')
        
    def test_variables(self):
        """Test that variables can be set and retrieved."""
        self.game_state.set_var('test_var', 'test_value')
        self.assertEqual(self.game_state.get_var('test_var'), 'test_value')
        
        self.game_state.set_var('int_var', 42)
        self.assertEqual(self.game_state.get_var('int_var'), 42)
        
        # Test default value
        self.assertIsNone(self.game_state.get_var('nonexistent_var'))
        self.assertEqual(self.game_state.get_var('nonexistent_var', 'default'), 'default')
        
    def test_turn_counter(self):
        """Test that the turn counter works correctly."""
        initial_turns = self.game_state.turn_count
        self.game_state.increment_turn()
        self.assertEqual(self.game_state.turn_count, initial_turns + 1)
        
    def test_reset(self):
        """Test that the reset method works correctly."""
        self.game_state.turn_count = 10
        self.game_state.set_flag('test_flag')
        self.game_state.set_var('test_var', 'test_value')
        
        self.game_state.reset()
        
        self.assertEqual(self.game_state.turn_count, 0)
        self.assertFalse(self.game_state.get_flag('test_flag'))
        self.assertIsNone(self.game_state.get_var('test_var'))

if __name__ == '__main__':
    unittest.main()