FROM astral/uv:python3.13-trixie

COPY . /backend
RUN uv sync 

ENTRYPOINT ["uv", "run","main.py"] 
