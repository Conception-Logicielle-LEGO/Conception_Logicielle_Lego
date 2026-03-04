FROM astral/uv:python3.13-trixie

WORKDIR /backend

COPY pyproject.toml .
RUN uv sync 

COPY . .

ENTRYPOINT ["docker_backend_bash.sh"] 
