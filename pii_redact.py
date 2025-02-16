import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

import re
from nltk import word_tokenize, pos_tag, ne_chunk

def redact_names_nltk(text):
    # Tokenize the text and perform POS tagging
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)
    
    # Use NLTK's named entity chunker to identify named entities
    named_entities = ne_chunk(tagged_tokens)
    
    # Extract person names
    person_names = set()
    for subtree in named_entities:
        if isinstance(subtree, nltk.Tree):  # This is a named entity
            if subtree.label() == 'PERSON':  # Only pick out 'PERSON' entities
                person_names.add(" ".join(word for word, tag in subtree))
    
    # Create a unique list of person names while maintaining the order of first appearance
    unique_person_names = list(person_names)
    
    # Create a mapping of names to "Person X" (e.g., "Person A", "Person B", etc.)
    name_map = {name: f"Person {chr(97 + i)}" for i, name in enumerate(unique_person_names)}
    
    # Replace names that are followed by a colon with "Person X"
    redacted_text = text
    for name, person in name_map.items():
        # Replace names before a colon with the respective "Person X"
        redacted_text = re.sub(r'(?<=:)\s*' + re.escape(name), person, redacted_text)
    
    # Replace all other occurrences of names with "REDACTED_NAME"
    for name in unique_person_names:
        redacted_text = re.sub(r'\b' + re.escape(name) + r'\b', 'REDACTED_NAME', redacted_text)
    
    # Replace the first occurrence of each name (that is a speaker) with "Person A", "Person B", etc.
    redacted_text_with_speakers = ""
    speaker_count = 0
    for line in redacted_text.split("\n"):
        if ":" in line:  # If this line represents a speaker
            speaker_name = line.split(":")[0].strip()
            if speaker_name in name_map:
                redacted_text_with_speakers += line.replace(speaker_name, name_map[speaker_name]) + "\n"
            else:
                redacted_text_with_speakers += line + "\n"
        else:
            redacted_text_with_speakers += line + "\n"
    
    return redacted_text_with_speakers

# Example usage
# input_text = """John: Hey, Emma, how have you been?
# Emma: I've been good, just busy with work. Any plans for the weekend?
# John: Glad to hear. I'm gonna hit up the golf course with Dominic tomorrow."""

# redacted_text = redact_names_nltk(input_text)
# print(redacted_text)