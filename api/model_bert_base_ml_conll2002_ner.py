import torch
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification
)


class Model:

    label_list = [
        "B-LOC",
        "B-MISC",
        "B-ORG",
        "B-PER",
        "I-LOC",
        "I-MISC",
        "I-ORG",
        "I-PER",
        "O"
    ]

    def __init__(self):
        self._tokenizer = AutoTokenizer.from_pretrained("wietsedv/bert-base-multilingual-cased-finetuned-conll2002-ner")
        self._model = AutoModelForTokenClassification.from_pretrained("wietsedv/bert-base-multilingual-cased-finetuned-conll2002-ner")

    def run(self, text, params):
        # Bit of a hack to get the tokens with the special tokens
        tokens = self._tokenizer.tokenize(self._tokenizer.decode(self._tokenizer.encode(text)))
        inputs = self._tokenizer.encode(text, return_tensors="pt")

        outputs = self._model(inputs)[0]
        predictions = torch.argmax(outputs, dim=2)

        result = [(token, self.label_list[prediction]) for token, prediction in zip(tokens, predictions[0].tolist())]
        return self.getEntities(result)

    def getEntities(self, result):
        entities = []
        label2score = {
            'B-PER': 3,
            'B-ORG': 3,
            'B-MISC': 3,
            'B-LOC': 3,
            'I-PER': 2,
            'I-ORG': 2,
            'I-MISC': 2,
            'I-LOC': 2,
            'O': 0
        }

        # FIXME: A bit of a hack to associate sub-words with original words, improvements welcome
        cursor = None
        cursor_type = ''
        for i in range(len(result)):
            c, l = result[i]
            print(f"c:{c}, l:{l}")
            if c in ['[CLS]', '[SEP]']:
                continue
            score = label2score[l]
            if score == 3:
                if cursor:
                    entities.append((cursor, cursor_type))
                cursor, cursor_type = c, l
            elif score == 2:
                if cursor:
                    if c.startswith('#'):
                        cursor += c.replace('##', '')
                    else:
                        cursor += ' ' + c
                else:
                    cursor, cursor_type = c, l
            elif score == 0 and cursor:
                if c.startswith('#'):
                    cursor += c.replace('##', '')
                else:
                    entities.append((cursor, cursor_type))
                    cursor = None

        return entities
