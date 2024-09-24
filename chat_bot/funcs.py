def encode_sentence(sentence, word2idx):
    return [word2idx[word] for word in sentence.split()]


def pad_sequence(seq, max_len):
    return seq + [0] * (max_len - len(seq)) if len(seq) < max_len else seq[:max_len]


def generate_response(torch, word2idx, max_len, idx2word, model, question):
    model.eval()
    with torch.no_grad():
        # Преобразуем вопрос в числовой вектор
        question_vector = encode_sentence(question, word2idx)
        question_vector = pad_sequence(question_vector, max_len)
        question_tensor = torch.tensor([question_vector], dtype=torch.long)

        # Прогон через модель
        output = model(question_tensor)
        output = output.squeeze(0)

        # Получаем предсказанные слова
        predicted_indices = torch.argmax(output, dim=1)
        predicted_words = [idx2word[idx.item()] for idx in predicted_indices]

        return " ".join(predicted_words)
