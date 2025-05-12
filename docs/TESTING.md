# Testing the Text Adventure System

This document explains how to run tests for the Alpha Cloudplex text adventure system and how to write new tests for your own additions.

## Running Tests

To run all tests for the system, use the following command from the project root:

```bash
python -m unittest discover tests
```

To run a specific test file:

```bash
python -m unittest tests/test_engine.py
```

To run a specific test class:

```bash
python -m unittest tests.test_engine.TestRoom
```

To run a specific test method:

```bash
python -m unittest tests.test_engine.TestRoom.test_room_creation
```

## Test Coverage

The current test suite covers these key components:

1. **Core Engine (test_engine.py)**
   - Room creation and connections
   - Item creation and callbacks
   - Game state management
   - Content management

2. **Museum Module (test_museum.py)**
   - Museum structure and room connections
   - Item placement and properties
   - Interactive exhibits functionality
   - Key puzzle mechanics

3. **Command Handlers (test_command_handlers.py)**
   - Navigation commands (go, north, etc.)
   - Inventory management (take, drop, inventory)
   - Item examination and usage
   - Item-to-item interactions

## Writing Your Own Tests

When adding new features to the system, you should also add tests to ensure they work correctly. Here's how to structure your tests:

### 1. Create a Test File

Test files should be named `test_*.py` and placed in the `tests` directory. For a new module named `my_area.py`, you would create `tests/test_my_area.py`.

### 2. Import Required Modules

```python
import unittest
from unittest.mock import patch, MagicMock

from text_adv.engine import Room, Item, GameState, inventory, game_state
from text_adv.my_area import create_my_area, initialize_my_area
```

### 3. Create Test Classes

Each test class should inherit from `unittest.TestCase` and focus on a specific component:

```python
class TestMyArea(unittest.TestCase):
    """Tests for my custom area."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Reset the game state for testing
        GameState._instance = None
        self.test_game_state = GameState()
        
        # Initialize your area
        self.starting_room = create_my_area()
```

### 4. Write Test Methods

Test methods should start with `test_` and each test should focus on a single aspect:

```python
def test_area_structure(self):
    """Test that the area has the correct structure and connections."""
    self.assertEqual(self.starting_room.name, "Entry Point")
    
    # Check connections
    self.assertIn('north', self.starting_room.exits)
    second_room = self.starting_room.exits['north']
    self.assertEqual(second_room.name, "Digital Garden")
    self.assertEqual(second_room.exits['south'], self.starting_room)
```

### 5. Testing Functions with Side Effects

For functions that print to the console or modify global state, use `unittest.mock` to isolate the behavior:

```python
@patch('text_adv.my_area.print_styled')
def test_use_special_item(self, mock_print):
    """Test using the special item in my area."""
    # Find the item
    special_item = None
    for item in self.starting_room.items:
        if item.name == "special_item":
            special_item = item
            break
    
    self.assertIsNotNone(special_item)
    
    # Test using the item
    special_item.on_use()
    
    # Check that the right messages were printed
    mock_print.assert_any_call("The special item glows brightly!", "success")
```

### 6. Testing Command Handlers

When testing command handlers, you'll often need to mock the adventurelib matching function:

```python
@patch('text_adv.engine.print_styled')
@patch('text_adv.engine.adv.match_item', side_effect=lambda name, items: next((i for i in items if i.name == name), None))
def test_custom_command(self, mock_match, mock_print):
    """Test a custom command implementation."""
    from text_adv.my_area import my_custom_command
    
    # Set up the test environment
    game_state.current_room = self.starting_room
    
    # Run the command
    my_custom_command("test_argument")
    
    # Check the results
    mock_print.assert_called_with("Command executed successfully!", "success")
```

## Test-Driven Development

Consider using a test-driven development (TDD) approach when adding new features:

1. Write a test that defines the expected behavior
2. Run the test and see it fail
3. Implement the feature to make the test pass
4. Refactor the code while ensuring tests still pass
5. Repeat for additional features

This approach helps ensure your code works as expected and makes it easier to catch regressions when making changes.

## Continuous Testing

Get in the habit of running tests frequently during development:

- Run tests after implementing each new feature
- Run tests before committing changes to version control
- Run tests after refactoring existing code

This practice helps catch issues early when they're easier to fix.

## Test Organization Tips

- Group related tests in the same test class
- Use descriptive test method names that explain what's being tested
- Use `setUp` and `tearDown` methods to avoid duplicating code
- Add comments explaining the purpose of complex test logic
- Use assertions that provide helpful error messages

By following these guidelines, you'll create a robust test suite that ensures your text adventure works correctly and remains maintainable as it grows.