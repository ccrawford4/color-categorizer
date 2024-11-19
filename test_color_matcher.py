import unittest
import sys
sys.path.append('.')  # Ensure the main script is in the path
from color_matcher_lambda import find_closest_color, hex_to_rgb, color_distance

class TestColorMatcher(unittest.TestCase):
    def test_hex_to_rgb_conversion(self):
        """Test hex to RGB conversion"""
        self.assertEqual(hex_to_rgb('FFFFFF'), (255, 255, 255))
        self.assertEqual(hex_to_rgb('#000000'), (0, 0, 0))
        self.assertEqual(hex_to_rgb('FF0000'), (255, 0, 0))

    def test_color_distance_calculation(self):
        """Test color distance calculation"""
        # Identical colors should have zero distance
        self.assertAlmostEqual(color_distance((255,0,0), (255,0,0)), 0)
        
        # Different colors should have non-zero distance
        distance = color_distance((255,0,0), (0,255,0))
        self.assertGreater(distance, 0)

    def test_exact_color_matches(self):
        """Test matching for exact predefined colors"""
        # Exact hex values for predefined colors
        test_cases = {
            'FFFFFF': 'white',
            '000000': 'black',
            'FF0000': 'red',
            '0000FF': 'blue',
            '008000': 'green',
            'FFA500': 'orange'
        }
        
        for hex_color, expected_color in test_cases.items():
            with self.subTest(hex_color=hex_color):
                self.assertEqual(find_closest_color(hex_color), expected_color)

    def test_nearby_color_matches(self):
        """Test matching for colors near predefined colors"""
        test_cases = [
            # Near white
            ('F0F0F0', 'white'),
            # Near black
            ('101010', 'black'),
            # Near red
            ('FF3333', 'red'),
            # Near blue
            ('3333FF', 'blue'),
            # Near green
            ('00FF33', 'green')
        ]
        
        for hex_color, expected_color in test_cases:
            with self.subTest(hex_color=hex_color):
                self.assertEqual(find_closest_color(hex_color), expected_color)

    def test_edge_case_colors(self):
        """Test colors near the boundaries between predefined colors"""
        test_cases = [
            # Colors near the boundary between red and pink
            ('FF4500', 'red'),
            ('FF69B4', 'pink'),
            
            # Colors near the boundary between blue and violet
            ('0000CD', 'blue'),
            ('8A2BE2', 'violet'),
            
            # Colors near the boundary between yellow and orange
            ('FFD700', 'yellow'),
            ('FFA500', 'orange')
        ]
        
        for hex_color, expected_color in test_cases:
            with self.subTest(hex_color=hex_color):
                self.assertEqual(find_closest_color(hex_color), expected_color)

    def test_hash_prefix_handling(self):
        """Test handling of hex colors with and without # prefix"""
        test_cases = [
            'FFFFFF',
            '#FFFFFF',
            'ffffff',
            '#ffffff'
        ]
        
        for hex_color in test_cases:
            with self.subTest(hex_color=hex_color):
                self.assertEqual(find_closest_color(hex_color), 'white')

    def test_case_insensitivity(self):
        """Test case insensitivity of hex input"""
        test_cases = [
            'FF0000',
            'ff0000',
            'Ff0000',
            '#FF0000'
        ]
        
        for hex_color in test_cases:
            with self.subTest(hex_color=hex_color):
                self.assertEqual(find_closest_color(hex_color), 'red')

    def test_complex_color_matching(self):
        """Test complex color matching scenarios"""
        test_cases = [
            # Brownish/orange colors
            ('8B4513', 'brown'),  # Saddle Brown
            ('D2691E', 'orange'),  # Orange
            
            # Grayish colors
            ('778899', 'grey'),   # Slate Gray
            ('A9A9A9', 'grey'),   # Dark Gray
            
            # Pinkish colors
            ('DC143C', 'red'),    # Crimson
            ('FF1493', 'pink')    # Deep Pink
        ]
        
        for hex_color, expected_color in test_cases:
            with self.subTest(hex_color=hex_color):
                self.assertEqual(find_closest_color(hex_color), expected_color)

if __name__ == '__main__':
    unittest.main()