FROM astral/uv:python3.13-trixie /uv /uvx /bin/
COPY . . 
RUN uv sync 
ENTRYPOINT ["uv", "run","main.py"] 
