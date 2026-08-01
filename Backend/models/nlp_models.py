import spacy
import stanza

nlp_en = spacy.load("en_core_web_sm")
nlp_hi = stanza.Pipeline("hi")