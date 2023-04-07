
FROM python:3.9

WORKDIR /code

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

RUN pip install .

CMD ["closedai", "--host", "0.0.0.0", "--port", "7860"]