#!/usr/bin/env python3
"""
SVG CLI - A command-line tool for creating and editing SVG files using the Claude API.
"""

import os
import sys
import json
import click
import requests
import dotenv
from pathlib import Path
from typing import Optional

# Load environment variables
dotenv.load_dotenv()

# Get API key from the environment
API_KEY = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_API_KEY")
API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-3-opus-20240229"  # Using the latest Claude model

# System prompt to ensure SVG output
SVG_SYSTEM_PROMPT = """You are an expert SVG creator. The user will ask you to create or modify SVG images.

IMPORTANT INSTRUCTIONS:
1. Respond ONLY with valid SVG code
2. Do NOT include any explanations, comments, or markdown
3. Your response must start with <svg and end with </svg>
4. Create clean, optimized SVG code
5. Do not include any text outside the SVG tags

If editing an existing SVG, maintain its structure while implementing the requested changes."""


def validate_api_key() -> None:
    """Check if API key is available and valid."""
    if not API_KEY:
        click.echo("Error: Claude API key not found. Please set ANTHROPIC_API_KEY in your environment.")
        sys.exit(1)


def get_headers() -> dict:
    """Get the appropriate headers for Claude API authentication."""
    validate_api_key()
    
    # Default headers
    headers = {
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    
    # Add appropriate auth header based on API key format
    if API_KEY.startswith("sk-ant-"):
        headers["x-api-key"] = API_KEY
    else:
        headers["authorization"] = f"Bearer {API_KEY}"
    
    return headers

def create_svg(prompt: str) -> str:
    """Create an SVG based on the text prompt using Claude API."""
    headers = get_headers()
    
    data = {
        "model": MODEL,
        "max_tokens": 4096,
        "system": SVG_SYSTEM_PROMPT,
        "messages": [
            {"role": "user", "content": f"Create an SVG image based on this description: {prompt}"}
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        content = result["content"][0]["text"]
        
        # Extract SVG content
        if "<svg" in content and "</svg>" in content:
            svg_start = content.find("<svg")
            svg_end = content.find("</svg>") + 6
            return content[svg_start:svg_end]
        else:
            click.echo("Error: Claude's response did not contain valid SVG code.")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error calling Claude API: {e}")
        sys.exit(1)


def edit_svg(input_file: str, prompt: str) -> str:
    """Edit an existing SVG based on the prompt using Claude API."""
    # Read the input SVG file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            svg_content = f.read()
    except FileNotFoundError:
        click.echo(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    headers = get_headers()
    
    data = {
        "model": MODEL,
        "max_tokens": 4096,
        "system": SVG_SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": f"Here is an SVG file. {prompt}"},
                    {"type": "text", "text": svg_content}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        content = result["content"][0]["text"]
        
        # Extract SVG content
        if "<svg" in content and "</svg>" in content:
            svg_start = content.find("<svg")
            svg_end = content.find("</svg>") + 6
            return content[svg_start:svg_end]
        else:
            click.echo("Error: Claude's response did not contain valid SVG code.")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error calling Claude API: {e}")
        sys.exit(1)


@click.group()
def cli():
    """SVG CLI - Create and edit SVG files using Claude AI."""
    pass


@cli.command()
@click.argument("prompt")
@click.option("--output", "-o", required=True, help="Output SVG file path")
def create(prompt: str, output: str):
    """Create a new SVG file based on a text prompt."""
    click.echo(f"Creating SVG from prompt: {prompt}")
    svg_content = create_svg(prompt)
    
    # Save the SVG to file
    try:
        with open(output, "w", encoding="utf-8") as f:
            f.write(svg_content)
        click.echo(f"SVG created successfully: {output}")
    except IOError as e:
        click.echo(f"Error saving SVG file: {e}")
        sys.exit(1)


@cli.command()
@click.option("--input", "-i", required=True, help="Input SVG file path")
@click.option("--output", "-o", required=True, help="Output SVG file path")
@click.argument("prompt")
def edit(input: str, output: str, prompt: str):
    """Edit an existing SVG file based on a text prompt."""
    click.echo(f"Editing SVG {input} with prompt: {prompt}")
    svg_content = edit_svg(input, prompt)
    
    # Save the SVG to file
    try:
        with open(output, "w", encoding="utf-8") as f:
            f.write(svg_content)
        click.echo(f"SVG edited successfully: {output}")
    except IOError as e:
        click.echo(f"Error saving SVG file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()