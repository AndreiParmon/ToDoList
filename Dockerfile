FROM python:3.10-slim
WORKDIR /opt/todolist
ENV PIP_DISABLE_PIP_VERSION_CHEK=on\
    PIP_ON_CACHE_DIR=off\
    PYTHON_PATH=/opt/todolist
RUN pip install "poetry==1.5.1"
RUN groupadd --system service && useradd --system -g service api

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev  --no-ansi --no-root
COPY src/ ./
COPY entrypoint.sh ./entrypoint.sh
USER api
ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
