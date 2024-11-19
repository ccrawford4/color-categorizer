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
    """
    Calculate advanced color distance using weighted Euclidean distance.
    Gives more weight to luminance and color differences.
    """
    # Weights for RGB components
    # Adjusted to be more sensitive to luminance and color nuances
    weights = (0.299, 0.587, 0.114)  # Standard luminance weights
    
    # Squared differences with weights
    weighted_sq_diff = [
        weights[i] * ((color1[i] - color2[i]) ** 2)
        for i in range(3)
    ]
    
    return math.sqrt(sum(weighted_sq_diff))

def calculate_luminance(rgb):
    """Calculate relative luminance of a color."""
    # Standard luminance calculation
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]

def find_closest_color(input_hex):
    """Find the closest predefined color to the input hex color."""
    try:
        # Convert input hex to RGB
        input_rgb = hex_to_rgb(input_hex)
        
        # Calculate input luminance
        input_luminance = calculate_luminance(input_rgb)
        
        # Find the closest color
        closest_color_item = min(
            COLOR_MAP.items(), 
            key=lambda x: (
                color_distance(hex_to_rgb(x[1]), input_rgb),
                abs(calculate_luminance(hex_to_rgb(x[1])) - input_luminance)
            )
        )[0]

        return closest_color_item
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