import torch.nn as nn
import torch.nn.functional as F

class LSTMModel(nn.Module):

    def __init__(self, vocab_size, embedding_dim, hidden_size, num_layers, dropout,num_hours):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(input_size = embedding_dim,
                            hidden_size = hidden_size,
                            num_layers = num_layers,
                            dropout = dropout,
                            batch_first = True,
                            bidirectional = True)
        self.linear1 = nn.Linear(40*100, 10)
        self.linear2 = nn.Linear(10, num_hours)

    def forward(self, inputs):
        emb = self.embedding(inputs)
        lstm_out, _ = self.lstm(emb)

        out_feat1 = self.linear1(lstm_out.reshape(lstm_out.size()[0], -1))
        out_feat2 = self.linear2(out_feat1)


        duration = F.sigmoid(out_feat2)

        return duration

