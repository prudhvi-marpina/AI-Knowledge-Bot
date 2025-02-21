import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def preprocess_query(query):
    """
    Preprocess the user's query by tokenizing, removing stop words,
    and identifying entities with context.
    """
    doc = nlp(query)
    tokens = [token.text.lower() for token in doc if not token.is_stop and token.is_alpha]
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Extract key phrases from the query
    key_phrases = [chunk.text for chunk in doc.noun_chunks if not any(token.is_stop for token in chunk)]

    print(entities , key_phrases)

    return tokens, entities, key_phrases
