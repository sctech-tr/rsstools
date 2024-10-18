import click
import json
from datetime import datetime
from .feed_creator import RSSFeedCreator
from .exceptions import RSSToolsError

@click.group()
def cli():
    """RSS Feed Creator and Editor - Create and manage RSS feeds easily."""
    pass

@cli.command()
@click.option('--title', '-t', required=True, help='Feed title')
@click.option('--link', '-l', required=True, help='Feed link')
@click.option('--description', '-d', required=True, help='Feed description')
@click.option('--output', '-o', required=True, help='Output file path')
def create(title, link, description, output):
    """Create a new RSS feed."""
    try:
        feed = RSSFeedCreator(title, link, description)
        feed.save(output)
        click.echo(f"Successfully created RSS feed: {output}")
    except RSSToolsError as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('feed_file')
@click.option('--title', '-t', required=True, help='Item title')
@click.option('--link', '-l', required=True, help='Item link')
@click.option('--description', '-d', required=True, help='Item description')
@click.option('--author', '-a', help='Item author')
@click.option('--pub-date', '-p', help='Publication date (ISO format)')
def add(feed_file, title, link, description, author, pub_date):
    """Add a new item to an RSS feed."""
    try:
        feed = RSSFeedCreator("", "", "")
        feed.load(feed_file)
        
        pub_date_obj = None
        if pub_date:
            pub_date_obj = datetime.fromisoformat(pub_date)
            
        feed.add_item(
            title=title,
            link=link,
            description=description,
            author=author,
            pub_date=pub_date_obj
        )
        
        feed.save(feed_file)
        click.echo(f"Successfully added item to feed: {title}")
    except RSSToolsError as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('feed_file')
@click.argument('guid')
def remove(feed_file, guid):
    """Remove an item from an RSS feed by its GUID."""
    try:
        feed = RSSFeedCreator("", "", "")
        feed.load(feed_file)
        
        if feed.remove_item(guid):
            feed.save(feed_file)
            click.echo(f"Successfully removed item with GUID: {guid}")
        else:
            click.echo(f"Item with GUID {guid} not found")
    except RSSToolsError as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('feed_file')
@click.argument('guid')
@click.option('--title', '-t', help='New title')
@click.option('--link', '-l', help='New link')
@click.option('--description', '-d', help='New description')
@click.option('--author', '-a', help='New author')
def update(feed_file, guid, title, link, description, author):
    """Update an item in the RSS feed."""
    try:
        feed = RSSFeedCreator("", "", "")
        feed.load(feed_file)
        
        updates = {}
        if title:
            updates['title'] = title
        if link:
            updates['link'] = link
        if description:
            updates['description'] = description
        if author:
            updates['author'] = author
            
        if feed.update_item(guid, **updates):
            feed.save(feed_file)
            click.echo(f"Successfully updated item with GUID: {guid}")
        else:
            click.echo(f"Item with GUID {guid} not found")
    except RSSToolsError as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('feed_file')
@click.option('--output', '-o', help='Output JSON file (optional)')
def list(feed_file, output):
    """List all items in an RSS feed."""
    try:
        feed = RSSFeedCreator("", "", "")
        feed.load(feed_file)
        items = feed.get_items()
        
        if output:
            with open(output, 'w') as f:
                json.dump(items, f, indent=2)
            click.echo(f"Items exported to: {output}")
        else:
            for item in items:
                click.echo("\n--- Item ---")
                for key, value in item.items():
                    click.echo(f"{key}: {value}")
    except RSSToolsError as e:
        click.echo(f"Error: {str(e)}", err=True)

def main():
    cli()