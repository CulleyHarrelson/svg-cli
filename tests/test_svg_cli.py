#!/usr/bin/env python3
"""
Unit tests for the SVG CLI application.
"""

import os
import sys
import unittest
from unittest import mock
from click.testing import CliRunner

# Add the parent directory to the path so we can import the main script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the main script
# Use importlib to handle module names with hyphens
import importlib.util
import os

# Load the module dynamically
spec = importlib.util.spec_from_file_location(
    "svg_cli", 
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'svg-cli.py'))
)
svg_cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(svg_cli)

# Extract the needed functions and objects
cli = svg_cli.cli
create_svg = svg_cli.create_svg
edit_svg = svg_cli.edit_svg
validate_api_key = svg_cli.validate_api_key

# Mock response for Claude API
MOCK_SVG_RESPONSE = {
    "content": [
        {
            "text": "<svg width=\"100\" height=\"100\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"blue\"/></svg>",
            "type": "text"
        }
    ]
}


class TestSvgCli(unittest.TestCase):
    """Test suite for the SVG CLI application."""

    def setUp(self):
        """Set up test environment."""
        self.runner = CliRunner()
        # Mock environment variable
        self.env_patcher = mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_api_key"})
        self.env_patcher.start()

    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()

    def test_validate_api_key_success(self):
        """Test API key validation when key exists."""
        # This should not raise SystemExit
        validate_api_key()

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_validate_api_key_failure(self):
        """Test API key validation when key does not exist."""
        # Make sure both env vars are cleared
        with mock.patch.object(svg_cli, 'API_KEY', None):
            with self.assertRaises(SystemExit):
                validate_api_key()

    @mock.patch('requests.post')
    def test_create_svg(self, mock_post):
        """Test SVG creation with a mocked API response."""
        # Configure the mock to return a successful response
        mock_response = mock.Mock()
        mock_response.json.return_value = MOCK_SVG_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = create_svg("Create a blue circle")
        self.assertIn("<svg", result)
        self.assertIn("</svg>", result)
        self.assertIn("blue", result)

    @mock.patch('requests.post')
    def test_edit_svg(self, mock_post):
        """Test SVG editing with a mocked API response."""
        # Configure the mock to return a successful response
        mock_response = mock.Mock()
        mock_response.json.return_value = MOCK_SVG_RESPONSE
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Create a temporary SVG file for testing
        with self.runner.isolated_filesystem():
            with open("test.svg", "w") as f:
                f.write("<svg width=\"100\" height=\"100\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"red\"/></svg>")
            
            result = edit_svg("test.svg", "Change the circle to blue")
            self.assertIn("<svg", result)
            self.assertIn("</svg>", result)
            self.assertIn("blue", result)

    def test_create_command(self):
        """Test the 'create' command."""
        with mock.patch.object(svg_cli, 'create_svg', return_value="<svg>Test SVG</svg>"):
            with self.runner.isolated_filesystem():
                result = self.runner.invoke(cli, ["create", "--output", "output.svg", "Create a test SVG"])
                self.assertEqual(0, result.exit_code)
                self.assertIn("SVG created successfully", result.output)
                
                # Check if the file was created
                self.assertTrue(os.path.exists("output.svg"))
                with open("output.svg", "r") as f:
                    content = f.read()
                    self.assertEqual("<svg>Test SVG</svg>", content)

    def test_edit_command(self):
        """Test the 'edit' command."""
        with mock.patch.object(svg_cli, 'edit_svg', return_value="<svg>Edited SVG</svg>"):
            with self.runner.isolated_filesystem():
                # Create an input file first
                with open("input.svg", "w") as f:
                    f.write("<svg>Original SVG</svg>")
                    
                result = self.runner.invoke(cli, ["edit", "--input", "input.svg", "--output", "output.svg", "Edit this SVG"])
                self.assertEqual(0, result.exit_code)
                self.assertIn("SVG edited successfully", result.output)
                
                # Check if the file was created
                self.assertTrue(os.path.exists("output.svg"))
                with open("output.svg", "r") as f:
                    content = f.read()
                    self.assertEqual("<svg>Edited SVG</svg>", content)


if __name__ == '__main__':
    unittest.main()