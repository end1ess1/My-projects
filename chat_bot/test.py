import torch
import torch.nn as nn

# Пример простого набора данных
data = [
    ("привет", "Привет! Как твои дела?"),
    ("как дела", "Все хорошо, спасибо! Как у тебя?"),
    ("пока", "До скорого!"),
    ("как тебя зовут", "Меня зовут Бот."),
    ("что ты умеешь", "Я могу поддержать беседу."),
]

# Подготовка данных
questions = [pair[0] for pair in data]
answers = [pair[1] for pair in data]

# Словарь для преобразования слов в индексы
vocab = list(set(" ".join(questions + answers).split()))
word2idx = {word: idx for idx, word in enumerate(vocab)}
idx2word = {idx: word for word, idx in word2idx.items()}


def encode_sentence(sentence, word2idx):
    return [word2idx[word] for word in sentence.split()]


# Преобразуем вопросы и ответы в числовые векторы
input_data = [encode_sentence(sentence, word2idx) for sentence in questions]
target_data = [encode_sentence(sentence, word2idx) for sentence in answers]

# Приведение всех векторов к одной длине (например, 5)
max_len = 5


def pad_sequence(seq, max_len):
    return seq + [0] * (max_len - len(seq)) if len(seq) < max_len else seq[:max_len]


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


# Параметры модели
vocab_size = len(vocab)
embedding_dim = 10
hidden_dim = 20
output_dim = vocab_size

# Инициализация модели
model = SimpleChatBot(vocab_size, embedding_dim, hidden_dim, output_dim)

# Определим оптимизатор и функцию потерь
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Обучение
epochs = 100
for epoch in range(epochs):
    model.train()

    # Прогон через модель
    output = model(input_data)

    # Преобразование данных в нужный формат для функции потерь
    output = output.view(-1, output_dim)
    target = target_data.view(-1)

    loss = criterion(output, target)

    # Оптимизация
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item()}")

# Пример взаимодействия
while True:
    user_input = input("Ты: ")
    response = generate_response(user_input)
    print(f"Бот: {response}")
