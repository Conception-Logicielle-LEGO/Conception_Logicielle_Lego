FROM astral/uv:python3.13-trixie

COPY ./backend/pyproject.toml /backend
RUN uv sync 

COPY . /backend

CMD ["uv", "run", "./backend/main.py"] 
