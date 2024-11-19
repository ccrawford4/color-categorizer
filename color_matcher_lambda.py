import math

# Predefined color dictionary with their hex values
COLOR_MAP = {
    'pink': '#FFC0CB',
    'red': '#FF0000', 
    'orange': '#FFA500',
    'yellow': '#FFFF00', 
    'green': '#008000', 
    'blue': '#0000FF', 
    'violet': '#8A2BE2', 
    'black': '#000000', 
    'brown': '#A52A2A', 
    'grey': '#808080', 
    'white': '#FFFFFF'
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    
    # Convert hex to RGB
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(color1, color2):
    """Calculate Euclidean distance between two RGB colors."""
    return math.sqrt(sum((a-b)**2 for a, b in zip(color1, color2)))

def find_closest_color(input_hex):
    """Find the closest predefined color to the input hex color."""
    try:
        # Convert input hex to RGB
        input_rgb = hex_to_rgb(input_hex)
        
        # Find the closest color
        closest_color = min(
            COLOR_MAP.items(), 
            key=lambda x: color_distance(hex_to_rgb(x[1]), input_rgb)
        )[0]
        
        return closest_color
    except Exception as e:
        return "Invalid hex color"

def lambda_handler(event, context):
    # Extract color from path
    try:
        # Get the full path from the event
        full_path = event.get('path', '')
        
        # Extract the hex color (last part of the path)
        hex_color = full_path.split('/')[-1]
        
        # Find and return the closest color name
        return find_closest_color(hex_color)
    
    except Exception as e:
        # Generic error handling
        return "Error processing request"