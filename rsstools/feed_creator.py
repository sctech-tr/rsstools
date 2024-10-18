from datetime import datetime
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from .feed_validator import validate_feed
from .templates import RSS_TEMPLATE
from .exceptions import RSSToolsError

class RSSFeedCreator:
    def __init__(self, title: str, link: str, description: str):
        """Initialize a new RSS feed."""
        self.feed = ET.fromstring(RSS_TEMPLATE)
        self.channel = self.feed.find('channel')
        self._set_required_elements(title, link, description)

    def _set_required_elements(self, title: str, link: str, description: str):
        """Set the required RSS channel elements."""
        elements = {
            'title': title,
            'link': link,
            'description': description,
            'lastBuildDate': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        }
        
        for name, value in elements.items():
            elem = self.channel.find(name)
            if elem is None:
                elem = ET.SubElement(self.channel, name)
            elem.text = value

    def add_item(self, title: str, link: str, description: str, 
                 pub_date: Optional[datetime] = None,
                 guid: Optional[str] = None,
                 author: Optional[str] = None) -> None:
        """Add a new item to the RSS feed."""
        item = ET.SubElement(self.channel, 'item')
        
        # Required elements
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'link').text = link
        ET.SubElement(item, 'description').text = description
        
        # Optional elements
        if pub_date:
            ET.SubElement(item, 'pubDate').text = pub_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        else:
            ET.SubElement(item, 'pubDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            
        if guid:
            ET.SubElement(item, 'guid').text = guid
        else:
            ET.SubElement(item, 'guid').text = link
            
        if author:
            ET.SubElement(item, 'author').text = author

    def remove_item(self, guid: str) -> bool:
        """Remove an item from the RSS feed by its GUID."""
        for item in self.channel.findall('item'):
            if item.find('guid').text == guid:
                self.channel.remove(item)
                return True
        return False

    def update_item(self, guid: str, **kwargs) -> bool:
        """Update an existing item's attributes."""
        for item in self.channel.findall('item'):
            if item.find('guid').text == guid:
                for key, value in kwargs.items():
                    elem = item.find(key)
                    if elem is not None:
                        elem.text = value if not isinstance(value, datetime) else value.strftime('%a, %d %b %Y %H:%M:%S GMT')
                return True
        return False

    def save(self, filename: str) -> None:
        """Save the RSS feed to a file."""
        try:
            validate_feed(self.feed)
            tree = ET.ElementTree(self.feed)
            tree.write(filename, encoding='utf-8', xml_declaration=True)
        except Exception as e:
            raise RSSToolsError(f"Failed to save RSS feed: {str(e)}")

    def load(self, filename: str) -> None:
        """Load an existing RSS feed from a file."""
        try:
            tree = ET.parse(filename)
            self.feed = tree.getroot()
            self.channel = self.feed.find('channel')
            validate_feed(self.feed)
        except Exception as e:
            raise RSSToolsError(f"Failed to load RSS feed: {str(e)}")

    def get_items(self) -> List[Dict]:
        """Get all items in the feed."""
        items = []
        for item in self.channel.findall('item'):
            item_dict = {}
            for child in item:
                item_dict[child.tag] = child.text
            items.append(item_dict)
        return items