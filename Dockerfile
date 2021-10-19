FROM python:3

ENV WORKDIR=/app

WORKDIR ${WORKDIR}

COPY bin/requirements.txt ${WORKDIR}
RUN pip install -r ${WORKDIR}/requirements.txt

COPY bin ${WORKDIR}

ENTRYPOINT [ "python", "main.py" ]
