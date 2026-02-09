FROM astral/uv:python3.13-trixie
COPY . . 
RUN uv sync 
ENTRYPOINT ["uv", "run","main.py"] 
