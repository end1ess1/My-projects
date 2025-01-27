-- Таблица для логирования модели
CREATE TABLE llm_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    username VARCHAR(50),
    chat_id UUID NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    question_length INT NOT NULL,
    answer_length INT NOT NULL,
    response_time_ms INT NOT NULL,
    question_language VARCHAR(10),
    answer_language VARCHAR(10),
    question_date VARCHAR(30)
    answer_date VARCHAR(30)
    model_version VARCHAR(50)
);

COMMENT ON TABLE llm_logs IS 'Таблица для анализа взаимодействий пользователей с LLM моделью';

COMMENT ON COLUMN llm_logs.first_name IS 'Уникальный идентификатор записи';
COMMENT ON COLUMN llm_logs.last_name IS 'ID пользователя';
COMMENT ON COLUMN llm_logs.username IS 'Юзернейм в ТГ';
COMMENT ON COLUMN llm_logs.id IS 'Уникальный id';
COMMENT ON COLUMN llm_logs.user_id IS 'ID юзера';
COMMENT ON COLUMN llm_logs.session_id IS 'ID сессии';
COMMENT ON COLUMN llm_logs.question IS 'Вопрос, заданный юзером';
COMMENT ON COLUMN llm_logs.answer IS 'Ответ, предоставленный моделью';
COMMENT ON COLUMN llm_logs.question_length IS 'Количество символов в вопросе юзера';
COMMENT ON COLUMN llm_logs.answer_length IS 'Количество символов в ответе модели';
COMMENT ON COLUMN llm_logs.response_time_ms IS 'Время ответа модели в секундах';
COMMENT ON COLUMN llm_logs.question_language IS 'Язык вопроса пользователя (например, ru, en)';
COMMENT ON COLUMN llm_logs.answer_language IS 'Язык ответа модели (например, ru, en)';
COMMENT ON COLUMN llm_logs.model_version IS 'Версия модели, использованной для ответа';
COMMENT ON COLUMN llm_logs.question_date IS 'Дата вопроса для модели';
COMMENT ON COLUMN llm_logs.answer_date IS 'Дата ответа модели';