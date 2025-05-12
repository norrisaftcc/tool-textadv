# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a Python-based text adventure game project aimed at educational purposes. The goal is to create an engaging learning experience through interactive text adventures.

The project is inspired by classic 80s text adventure games and aims to:
- Educate students quickly in a fun way
- Use Streamlit with custom themes
- Include a demo for playability
- Create multipage HTML presentations for teaching
- Utilize automated testing for verification

## Development Environment

```bash
# Create/activate Python virtual environment
python -m venv textenv
source textenv/bin/activate  # For Unix/MacOS
textenv\\Scripts\\activate  # For Windows

# Install dependencies (when requirements.txt is added)
pip install -r requirements.txt
```

## Architecture Overview

The text adventure will follow a modern Python implementation of classic adventure game concepts:

1. **Game Engine**: Manages game loop and coordinates components
2. **World Model**: Represents rooms, connections, and objects using dictionaries or classes
3. **Player**: Tracks inventory, status, and current location
4. **Parser**: Processes user commands and translates them into game actions
5. **Game State**: Tracks overall game progress and conditions

The project may incorporate the "adventurelib" library (referenced in the README) and context7.

## Project Themes

- **Alpha Cloudplex**: The lore name for this MUD (Multi-User Dungeon)
- **The Boardwalk**: Main entry point where players appear when logging in
- Educational focus with carnival-like tutorials and simple games to teach text commands

## File Structure

```
tool-textadv/
├── README.md                     # Project overview
├── docs/
│   └── research/                 # Research and ideas
│       ├── research_text_adv.md  # Main research document
│       └── unsorted_ideas.md     # Brainstorming and concepts
├── textenv/                      # Python virtual environment
```

When implementing the project, follow the patterns and examples in the research document, which provides detailed examples of how to structure the code using both dictionary-based and class-based approaches.