from .agent import LSTMModel
from .params import(
    vocab_size,
    embedding_dim,
    hidden_size,
    num_layers,
    dropout,
    num_hours
)
ProjectEstimator = LSTMModel(vocab_size=vocab_size,
                  embedding_dim=embedding_dim,
                  hidden_size=hidden_size,
                  num_layers=num_layers,
                  dropout=dropout,
                 num_hours=num_hours)