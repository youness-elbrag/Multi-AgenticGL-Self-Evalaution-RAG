from transformers import BertTokenizer

def Tokenizer(name_model):
    Tokenizer = BertTokenizer.from_pretrained(name_model)
    return Tokenizer



