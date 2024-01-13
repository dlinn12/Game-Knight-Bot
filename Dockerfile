FROM --platform=linux/arm/v7 python:3.10.1-buster AS builder

RUN pip install --upgrade pip && \
	pip install --user discord.py && \
	pip install --user python-dotenv

FROM --platform=linux/arm/v7 python:3.10.1-slim-buster

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local:$PATH

CMD ["python3", "main.py"]