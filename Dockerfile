FROM python:3.10.9-alpine3.17 AS builder

COPY . .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.10.9-alpine3.17

WORKDIR /app
COPY . .
COPY --from=builder /app/wheels /wheels

ARG GROUP_ID=GROUP_ID \
    TIME_SLEEP=300 \
    WALL_CNT=20 \
    VK_TOKENS=VK_TOKENS

ENV PATH="/root/.local/bin:${PATH}" \
    GROUP_ID=$GROUP_ID \
    TIME_SLEEP=$TIME_SLEEP \
    WALL_CNT=$WALL_CNT \
    VK_TOKENS=$VK_TOKENS

RUN pip install --no-cache /wheels/*

ENTRYPOINT python3 main.py
