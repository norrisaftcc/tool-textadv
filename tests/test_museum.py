"""
Tests for the museum module of the text adventure.

These tests ensure that the interactive learning museum functions correctly.
"""

import unittest
from unittest.mock import patch, MagicMock

from text_adv.engine import Room, Item, GameState, inventory, game_state
from text_adv.museum import create_museum, initialize_museum

class TestMuseum(unittest.TestCase):
    """Tests for the Interactive Learning Museum."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset the game state for testing
        GameState._instance = None
        self.test_game_state = GameState()
        
        # Initialize the museum
        self.entrance = create_museum()
        
    def test_museum_structure(self):
        """Test that the museum has the correct structure and connections."""
        # Check the entrance room
        self.assertEqual(self.entrance.name, "Museum Entrance Hall")
        
        # Check connections to other rooms
        self.assertIn('north', self.entrance.exits)
        self.assertIn('east', self.entrance.exits)
        self.assertIn('west', self.entrance.exits)
        self.assertIn('south', self.entrance.exits)
        
        # Check the connected rooms
        movement_room = self.entrance.exits['north']
        inventory_room = self.entrance.exits['east']
        items_room = self.entrance.exits['west']
        creation_room = self.entrance.exits['south']
        
        self.assertEqual(movement_room.name, "Gallery of Movement")
        self.assertEqual(inventory_room.name, "Hall of Inventory")
        self.assertEqual(items_room.name, "Chamber of Interactions")
        self.assertEqual(creation_room.name, "Workshop of Creation")
        
        # Check reverse connections
        self.assertEqual(movement_room.exits['south'], self.entrance)
        self.assertEqual(inventory_room.exits['west'], self.entrance)
        self.assertEqual(items_room.exits['east'], self.entrance)
        self.assertEqual(creation_room.exits['north'], self.entrance)
        
    def test_entrance_items(self):
        """Test that the entrance has the correct items."""
        # Get item names
        item_names = [item.name for item in self.entrance.items]
        
        # Check for required items
        self.assertIn('sign', item_names)
        self.assertIn('map', item_names)
        
        # Check properties
        for item in self.entrance.items:
            if item.name == 'sign':
                self.assertFalse(item.takeable)
                
    def test_movement_room(self):
        """Test the movement room and its items."""
        movement_room = self.entrance.exits['north']
        
        # Check items
        item_names = [item.name for item in movement_room.items]
        self.assertIn('guide', item_names)
        self.assertIn('compass', item_names)
        
        # Check compass properties
        compass = None
        for item in movement_room.items:
            if item.name == 'compass':
                compass = item
                break
                
        self.assertIsNotNone(compass)
        self.assertTrue(compass.takeable)
        self.assertIn(None, compass.use_callbacks)
        
    def test_inventory_room(self):
        """Test the inventory room and its items."""
        inventory_room = self.entrance.exits['east']
        
        # Check items
        item_names = [item.name for item in inventory_room.items]
        self.assertIn('plaque', item_names)
        self.assertIn('collection', item_names)
        self.assertIn('trinket', item_names)
        
        # Check collection properties
        collection = None
        for item in inventory_room.items:
            if item.name == 'collection':
                collection = item
                break
                
        self.assertIsNotNone(collection)
        self.assertTrue(collection.takeable)
        self.assertIn(None, collection.use_callbacks)
        
    def test_items_room(self):
        """Test the items interaction room and its objects."""
        items_room = self.entrance.exits['west']
        
        # Check items
        item_names = [item.name for item in items_room.items]
        self.assertIn('display', item_names)
        self.assertIn('key', item_names)
        self.assertIn('case', item_names)
        
        # Check key and case interaction
        key = None
        case = None
        for item in items_room.items:
            if item.name == 'key':
                key = item
            elif item.name == 'case':
                case = item
                
        self.assertIsNotNone(key)
        self.assertIsNotNone(case)
        self.assertTrue(key.takeable)
        self.assertFalse(case.takeable)
        
        # The key should have a callback for the case
        self.assertIn(case, key.use_callbacks)
        
    def test_creation_room(self):
        """Test the creation workshop room."""
        creation_room = self.entrance.exits['south']
        
        # Check items
        item_names = [item.name for item in creation_room.items]
        self.assertIn('manual', item_names)
        self.assertIn('notebook', item_names)
        
        # Check manual properties
        manual = None
        for item in creation_room.items:
            if item.name == 'manual':
                manual = item
                break
                
        self.assertIsNotNone(manual)
        self.assertFalse(manual.takeable)
        self.assertIn(None, manual.use_callbacks)

    @patch('text_adv.museum.print_styled')
    def test_use_sample_collection(self, mock_print):
        """Test the use_sample_collection function that adds items to room."""
        from text_adv.museum import use_sample_collection
        
        # Setup
        inventory_room = self.entrance.exits['east']
        game_state.current_room = inventory_room
        
        # Get the collection item
        collection = None
        for item in inventory_room.items:
            if item.name == 'collection':
                collection = item
                break
        
        self.assertIsNotNone(collection)
        
        # Count items before use
        initial_item_count = len(inventory_room.items)
        
        # Use the collection
        collection.on_use()
        
        # Should add three new items to the room
        self.assertEqual(len(inventory_room.items), initial_item_count + 3)
        
        # Check for the new items
        item_names = [item.name for item in inventory_room.items]
        self.assertIn('coin', item_names)
        self.assertIn('button', item_names)
        self.assertIn('marble', item_names)
        
        # Using it again shouldn't duplicate items
        collection.on_use()
        self.assertEqual(len(inventory_room.items), initial_item_count + 3)

    @patch('text_adv.museum.print_styled')
    def test_unlock_case(self, mock_print):
        """Test the key and case interaction."""
        from text_adv.museum import unlock_case
        
        # Setup
        items_room = self.entrance.exits['west']
        game_state.current_room = items_room
        
        # Get key and case
        key = None
        case = None
        for item in items_room.items:
            if item.name == 'key':
                key = item
            elif item.name == 'case':
                case = item
                
        self.assertIsNotNone(key)
        self.assertIsNotNone(case)
        
        # Count items before unlock
        initial_item_count = len(items_room.items)
        
        # Use the key on the case
        key.on_use(case)
        
        # Should add a badge to the room
        self.assertEqual(len(items_room.items), initial_item_count + 1)
        
        # Check for the badge
        item_names = [item.name for item in items_room.items]
        self.assertIn('badge', item_names)
        
        # Case description should be updated
        for item in items_room.items:
            if item.name == 'case':
                self.assertIn('unlocked', item.description.lower())

if __name__ == '__main__':
    unittest.main()