from funcs import encode_sentence, pad_sequence
import torch

# Набор данных
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

# Преобразуем вопросы и ответы в числовые векторы
input_data = [encode_sentence(sentence, word2idx) for sentence in questions]
target_data = [encode_sentence(sentence, word2idx) for sentence in answers]

# Приведение всех векторов к одной длине (например, 5)
max_len = 5

input_data = [pad_sequence(seq, max_len) for seq in input_data]
target_data = [pad_sequence(seq, max_len) for seq in target_data]

input_data = torch.tensor(input_data, dtype=torch.long)
target_data = torch.tensor(target_data, dtype=torch.long)
