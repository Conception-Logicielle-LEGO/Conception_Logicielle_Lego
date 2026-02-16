FROM astral/uv:python3.13-trixie

COPY pyproject.toml 
RUN uv sync 

COPY ..
ENTRYPOINT ["uv", "run","main.py"] 
