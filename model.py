import ollama

def build_prompt(rgb_val) :
    return (f'Given this RGB color {rgb_val} identify which of these colors its closest to: '
            f'1. RED'
            f'2. ORANGE'
            f'3. YELLOW'
            f'4. GREEN'
            f'5. BLUE'
            f'6. PURPLE'
            f'7. PINK'
            f'8. BLACK'
            f'9. WHITE'
            f'10. GRAY'
            f'ONLY ANSWER WITH THE NAME OF THE COLOR'
    )

def get_results(rgb_val) :
    response = ollama.chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': build_prompt(rgb_val),
        },
    ])
    return response['message']['content']