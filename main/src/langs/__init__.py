import json

class Lang:
    def __init__(self, code):
        self.code = code
        with open('data/langs.json', 'r') as file:
            self.vocab = json.load(file)[code]

    def get_vocab(self, for_lang='eng', synonyms=False):
        vocabs = []
        for a in self.vocab:
            t = a[for_lang if for_lang in a.keys() else 'eng']
            note = a['note'] if 'note' in a.keys() else ''
            note_t_key = 'note-' + for_lang if for_lang in a.keys() else 'note-eng'
            note_t = a[note_t_key] if note_t_key in a.keys() else ''
            o = {'w': a[self.code], 't': ([t] if type(t) == str else t if type(t) == list else ['']) if synonyms else (
                t if type(t) == str else t[0] if type(t) == list else '')}
            if note: o['note'] = note
            if note_t: o['note-t'] = note_t
            vocabs.append(o)
        return vocabs