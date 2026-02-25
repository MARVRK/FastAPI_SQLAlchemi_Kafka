FROM python:3.12-slim-trixie

LABEL authors="Rostyslav"

# системные зависимости
RUN apt-get update && apt-get install -y curl build-essential
RUN apt-get install -y postgresql-client
# установка uv (устанавливает все зависимости проекта)
ADD https://astral.sh/uv/install.sh /tmp/install_uv.sh
RUN bash /tmp/install_uv.sh && rm /tmp/install_uv.sh

# рабочая директория внутри контейнера (создается)
WORKDIR /user

# копируем c указанной директории только lock-файлы, ставим зависимости через uv
COPY pyproject.toml uv.lock /user/

# глобально ставим uvicorn и uv чтобы compose видел его
# ставим зависимости через uv
RUN python -m pip install --upgrade pip && \
    pip install "uv[all]" "uvicorn[standard]" && \
    uv sync --locked --all-extras

# копируем весь проект, чтобы pip мог собрать пакет
COPY . .

ENV PYTHONUNBUFFERED=1

# копируем энтрипонт и даем ему права на установку
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
