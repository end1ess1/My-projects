from data import vocab, input_data, target_data
from neuro import SimpleChatBot
import torch.nn as nn
import torch

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