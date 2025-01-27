-- Таблица для логирования модели
CREATE TABLE llm_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    session_id UUID NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    question_length INT NOT NULL,
    answer_length INT NOT NULL,
    response_time_ms INT NOT NULL,
    question_language VARCHAR(10),
    answer_language VARCHAR(10),
    question_tokens INT,
    answer_tokens INT,
    user_feedback_score INT,
    request_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    response_timestamp TIMESTAMP NOT NULL,
    model_version VARCHAR(50)
);

COMMENT ON TABLE llm_logs IS 'Таблица для анализа взаимодействий пользователей с LLM моделью';

COMMENT ON COLUMN llm_logs.id IS 'Уникальный идентификатор записи';
COMMENT ON COLUMN llm_logs.user_id IS 'ID пользователя';
COMMENT ON COLUMN llm_logs.session_id IS 'ID сессии общения пользователя с моделью';
COMMENT ON COLUMN llm_logs.question IS 'Вопрос, заданный пользователем';
COMMENT ON COLUMN llm_logs.answer IS 'Ответ, предоставленный моделью';
COMMENT ON COLUMN llm_logs.question_length IS 'Количество символов в вопросе пользователя';
COMMENT ON COLUMN llm_logs.answer_length IS 'Количество символов в ответе модели';
COMMENT ON COLUMN llm_logs.response_time_ms IS 'Время ответа модели в миллисекундах';
COMMENT ON COLUMN llm_logs.question_language IS 'Язык вопроса пользователя (например, ru, en)';
COMMENT ON COLUMN llm_logs.answer_language IS 'Язык ответа модели (например, ru, en)';
COMMENT ON COLUMN llm_logs.question_tokens IS 'Количество токенов в вопросе пользователя';
COMMENT ON COLUMN llm_logs.answer_tokens IS 'Количество токенов в ответе модели';
COMMENT ON COLUMN llm_logs.user_feedback_score IS 'Оценка ответа пользователем (от 1 до 5)';
COMMENT ON COLUMN llm_logs.request_timestamp IS 'Временная метка запроса пользователя';
COMMENT ON COLUMN llm_logs.response_timestamp IS 'Временная метка, когда модель вернула ответ';
COMMENT ON COLUMN llm_logs.model_version IS 'Версия модели, использованной для ответа';