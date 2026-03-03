FROM astral/uv:python3.13-trixie

WORKDIR /backend

COPY ./backend/pyproject.toml .
RUN uv sync 

COPY . .

CMD ["uv", "run", "main.py"] 
