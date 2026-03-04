FROM astral/uv:python3.13-trixie

WORKDIR /backend

COPY pyproject.toml .
RUN uv sync 

COPY . .

ENTRYPOINT ["/bin/sh", "-c" , "uv run main.py"] 
