FROM python:3.12-slim-trixie

LABEL authors="Rostyslav"

RUN apt-get update && apt-get install -y curl build-essential
ADD https://astral.sh/uv/install.sh /tmp/install_uv.sh
RUN bash /tmp/install_uv.sh && rm /tmp/install_uv.sh

COPY pyproject.toml uv.lock* ./

#provide path for env
ENV PATH="/root/.local/bin/:$PATH"
#creating virtual env.
RUN uv venv .venv

#provide path for runing uvicron
ENV PATH="/.venv/bin/:$PATH"
#instgall project.toml and use uv.lock
RUN uv sync --locked --all-extras

WORKDIR /app
COPY . /app

ENV PYTHONUNBUFFERED=1

CMD ["bash"]
