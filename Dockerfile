FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    clang \
    swig \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY phylib.c phylib.h phylib.i makefile ./
COPY Physics.py Server.py game.js display.css shoot.css shoot.html table.svg ./

RUN make PYTHON=/usr/local/include/python3.12/

ENV LD_LIBRARY_PATH=/app

CMD ["python", "Server.py"]
