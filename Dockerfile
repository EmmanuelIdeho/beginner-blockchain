FROM python:3.14-slim

WORKDIR /app

COPY . . 

RUN pip install uv && uv sync

CMD ["uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]