import spacy
import stanza
from gliner import GLiNER

nlp_en = spacy.load("en_core_web_sm")
nlp_hi = stanza.Pipeline("hi")
ner_model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
