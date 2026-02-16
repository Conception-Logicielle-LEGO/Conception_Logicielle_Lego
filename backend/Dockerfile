FROM astral/uv:python3.13-trixie

WORKDIR /backend

COPY ./backend/pyproject.toml /backend
RUN uv sync 

COPY . /backend

ENTRYPOINT ["uv", "run","main.py"] 
