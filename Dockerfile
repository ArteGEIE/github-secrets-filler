FROM python:3

LABEL org.opencontainers.image.source="https://github.com/ArteGEIE/github-secrets-filler"

ENV WORKDIR=/app
WORKDIR ${WORKDIR}

COPY bin/requirements.txt ${WORKDIR}
RUN pip install -r ${WORKDIR}/requirements.txt

COPY bin ${WORKDIR}

ENTRYPOINT [ "python", "main.py" ]
