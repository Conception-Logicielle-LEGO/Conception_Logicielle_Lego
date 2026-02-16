FROM astral/uv:python3.13-trixie

WORKDIR ./backend

COPY . .
RUN uv sync 

ENTRYPOINT ["uv", "run","main.py"] 
