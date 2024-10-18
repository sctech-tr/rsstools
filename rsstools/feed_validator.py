import xml.etree.ElementTree as ET
from .exceptions import RSSToolsError

def validate_feed(feed: ET.Element) -> bool:
    """Validate RSS feed structure and required elements."""
    required_channel_elements = ['title', 'link', 'description']
    required_item_elements = ['title', 'link', 'description']
    
    channel = feed.find('channel')
    if channel is None:
        raise RSSToolsError("Missing channel element")
        
    # Validate channel elements
    for element in required_channel_elements:
        if channel.find(element) is None:
            raise RSSToolsError(f"Missing required channel element: {element}")
            
    # Validate items
    for item in channel.findall('item'):
        for element in required_item_elements:
            if item.find(element) is None:
                raise RSSToolsError(f"Missing required item element: {element}")
                
    return True