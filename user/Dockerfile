FROM python:3.12-slim-trixie

LABEL authors="Rostyslav"

# системные зависимости
RUN apt-get update && apt-get install -y curl build-essential
# установка uv (устанавливает все зависимости проекта)
ADD https://astral.sh/uv/install.sh /tmp/install_uv.sh
RUN bash /tmp/install_uv.sh && rm /tmp/install_uv.sh


# глобально ставим uvicorn, чтобы compose видел его
RUN python -m pip install --upgrade pip
RUN pip install "uv[all]" "uvicorn[standard]"

# рабочая директория внутри контейнера
WORKDIR /app

# копируем только lock-файлы, ставим зависимости через uv
COPY pyproject.toml uv.lock* ./
RUN uv sync --locked --all-extras

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uv", "run","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
