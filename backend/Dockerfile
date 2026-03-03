FROM astral/uv:python3.13-trixie

WORKDIR /backend

COPY ./backend/pyproject.toml /backend
RUN uv sync 

COPY . /backend

CMD ["uv", "run", "./backend/main.py"] 
