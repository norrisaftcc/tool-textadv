# Development Environment

## Setup

```bash
# Create/activate Python virtual environment
python -m venv textenv
source textenv/bin/activate  # For Unix/MacOS
textenv\\Scripts\\activate  # For Windows

# Install dependencies
pip install -r requirements.txt
```

## File Structure

```
tool-textadv/
├── README.md                     # Project overview
├── docs/
│   ├── claude/                   # Claude-specific documentation
│   │   ├── architecture.md       # Architecture details
│   │   └── development.md        # This file
│   └── research/                 # Research and ideas
│       ├── research_text_adv.md  # Main research document
│       └── unsorted_ideas.md     # Brainstorming and concepts
├── src/                          # Source code
│   └── text_adv/                 # Main package
├── tests/                        # Test suite
└── textenv/                      # Python virtual environment
```