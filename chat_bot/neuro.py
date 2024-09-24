import torch.nn as nn


class SimpleChatBot(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(SimpleChatBot, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.RNN(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        embedded = self.embedding(x)  # Преобразование индексов в векторы
        output, hidden = self.rnn(embedded)  # Прогон через RNN
        output = self.fc(output)  # Прогон через линейный слой для предсказания
        return output