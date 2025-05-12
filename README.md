# Alpha Cloudplex Text Adventure

A Python-based text adventure game designed as an educational tool. Alpha Cloudplex is a simulation that knows it's a simulation, where humans and AI can interact on equal ground.

## Background

This project is inspired by classic 80s text adventure games, with a modern twist. The research folder contains ideas and implementation approaches based on traditional text adventure game concepts.

## Goals

- Educate students quickly in a fun and engaging way
- Provide a practical application of programming concepts
- Create an interactive experience that demonstrates text-based interfaces

## Features

- **Attractive**: Uses Streamlit and custom themes based on subject material
- **Illustrative**: Includes HTML presentations teaching students how it works
- **Playable**: Includes a fully functional demo
- **Verifiable**: Utilizes automated testing

## Implementation Details

The project is implemented in two versions:

1. **Console Version**: Terminal-based interface with colorful text using colorama
2. **Web Version**: Streamlit-based web interface with modern UI components

Both versions use the same core game engine.

## Game Setting

Players begin their adventure at "The Boardwalk" - the entry point to Alpha Cloudplex. The area features:

- Carnival games and rides that serve as tutorials
- Simple games to teach text-based commands
- Buildings that lead to other simulations

## Libraries Used

- **adventurelib**: Core text adventure functionality
- **colorama**: Colored terminal text
- **streamlit**: Web interface
- **context7**: (Planned for future integration)

## Getting Started

1. Clone the repository
2. Set up a virtual environment:
   ```bash
   python -m venv textenv
   source textenv/bin/activate  # On Windows: textenv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the console version:
   ```bash
   python -m src.text_adv.main
   ```
5. Or run the Streamlit version:
   ```bash
   streamlit run src/text_adv/streamlit_app.py
   ```

## Project Structure

```
tool-textadv/
├── docs/                      # Documentation and research
│   └── research/              # Research materials and game design
├── src/                       # Source code
│   └── text_adv/              # Game package
│       ├── assets/            # Game assets (ASCII art, etc.)
│       ├── engine.py          # Core game engine
│       ├── console.py         # Console interface
│       ├── streamlit_app.py   # Web interface
│       ├── boardwalk.py       # Boardwalk area implementation
│       └── main.py            # Main entry point
├── requirements.txt           # Project dependencies
├── TODO.md                    # Development tasks
└── README.md                  # This file
```

## Contributing

See the TODO.md file for planned features and enhancements.

## License

See the LICENSE file for details.

Good luck, have fun!