def calculate_word_count(filepath):
    with open(filepath, 'r') as file:
        text = file.read()
        words = text.split()
        return len(words)
    
# Path: src/core/utils.py