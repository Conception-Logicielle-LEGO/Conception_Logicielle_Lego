FROM astral/uv:python3.13-trixie

WORKDIR /backend

COPY pyproject.toml .
RUN uv sync

COPY . .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

