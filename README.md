# SVG CLI

A command-line tool for creating and editing SVG files using the Claude API.

## Features

- Create new SVG files from text prompts
- Edit existing SVG files with AI assistance
- Simple command-line interface
- Secure credential management

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/svg-cli.git
cd svg-cli

# Install the package
pip install -e .
```

## Configuration

Create a `.env` file in the project root with your Claude API key:

```
CLAUDE_API_KEY=your_api_key_here
```

## Usage

### Create a new SVG

```bash
svg-cli create --output filename.svg "Create a simple logo with a blue circle and a yellow star"
```

### Edit an existing SVG

```bash
svg-cli edit --input existing.svg --output modified.svg "Make the background red and add a border"
```

### Get help

```bash
svg-cli --help
```

## Requirements

- Python 3.8+
- Claude API access

## License

MIT