# rsstools

A powerful Python tool for creating, editing, and managing RSS feeds with both programmatic and command-line interfaces.

## Features

- Create new RSS feeds with all required elements
- Add, update, and remove items from feeds
- Load and save RSS feeds to XML files
- Validate feed structure and required elements
- Command-line interface for easy management
- Support for optional elements like author and publication date
- JSON export capability for feed items

## Installation

### Dependencies

First, ensure you have Python 3.7 or higher installed. This package requires the following dependencies:

```
click>=8.0.0
```

### Installing via pip (recommended)

1. Run this command:
```bash
pip install rsstools
```

### Installing via pyz

1. Download the latest pyz from the releases tab.
2. Run:

```bash
pip install rsstools.pyz
```

### Installing from source

This package requires the following dependencies:
```
click>=8.0.0
```

1. Clone the repository:
```bash
git clone https://github.com/sctech-tr/rsstools.git
cd rsstools
```

2. Install the package:
```bash
pip install .
```

## Usage

### Command Line Interface

1. Create a new RSS feed:
```bash
rsstools create -t "My Blog" -l "https://myblog.com" -d "My personal blog" -o feed.xml
```

2. Add an item to the feed:
```bash
rsstools add feed.xml \
-t "First Post" \
-l "https://myblog.com/first" \
-d "My first post" \
-a "John Doe" \
-p "2024-10-18T12:00:00"
```

3. List all items in a feed:
```bash
rsstools list feed.xml
```

4. Export items to JSON:
```bash
rsstools list feed.xml -o items.json
```

5. Update an item:
```bash
rsstools update feed.xml "https://myblog.com/first" -t "Updated Post Title"
```

6. Remove an item:
```bash
rsstools remove feed.xml "https://myblog.com/first"
```

### Python API

```python

from rsstools import RSSFeedCreator
from datetime import datetime

# Create a new feed
feed = RSSFeedCreator(
    title="My Blog",
    link="https://myblog.com",
    description="My personal blog about technology"
)

# Add an item
feed.add_item(
    title="First Post",
    link="https://myblog.com/first-post",
    description="This is my first blog post",
    author="John Doe",
    pub_date=datetime.now()
)

# Save the feed
feed.save("blog_feed.xml")

# Load an existing feed
feed.load("blog_feed.xml")

# Update an item
feed.update_item(
    guid="https://myblog.com/first-post",
    title="Updated First Post"
)

# Remove an item
feed.remove_item(guid="https://myblog.com/first-post")

# Get all items
items = feed.get_items()
```

## Contributing

1. Fork the repository
2. Open a PR

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Error Handling

The package uses custom exceptions (`RSSToolsError`) for error handling. Always wrap your code in try-except blocks when using the API:

```python
from rsstools import RSSFeedCreator, RSSToolsError

try:
    feed = RSSFeedCreator("My Blog", "https://myblog.com", "My blog description")
    feed.save("feed.xml")
except RSSToolsError as e:
    print(f"Error: {str(e)}")
```

## Common Issues and Solutions

1. **Invalid Feed Structure**: Ensure your RSS feed follows the standard RSS 2.0 format.
2. **File Permissions**: Make sure you have write permissions in the directory where you're saving the feed.
3. **Date Format**: When using the CLI, provide dates in ISO format (YYYY-MM-DDTHH:MM:SS).

## Getting Help

Use the `--help` flag with any command to see available options:
```bash
rsstools --help
rsstools create --help
rsstools add --help
```