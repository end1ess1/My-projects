from openai import OpenAI

client = OpenAI(
    api_key="sk-XXXXXXXXXXXXXXXX", # ваш ключ в VseGPT после регистрации
    base_url="https://api.vsegpt.ru/v1",
)

# prompt = "Напиши последовательно числа от 1 до 10"

# messages = []
# messages.append({"role": "user", "content": prompt})

# response_big = client.chat.completions.create(
#     model="anthropic/claude-3-haiku",
#     messages=messages,
#     temperature=0.7,
#     n=1,
#     max_tokens=3000,
# )

# response = response_big.choices[0].message.content
# print("Response:",response)

client.embeddings.create(
  model="text-embedding-ada-002",
  input="The food was delicious and the waiter...",
  encoding_format="float"
)

print()