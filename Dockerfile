FROM registry.access.redhat.com/rhscl/python-36-rhel7:1-51.1561731164
# https://access.redhat.com/containers/?tab=overview#/registry.access.redhat.com/rhscl/python-36-rhel7

EXPOSE 8080

USER root

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir && \
    pip install .

# Modell aus Modell-Repository ziehen
RUN dvc pull model.pkl.dvc

# Berechtigungen setzen
RUN chgrp -R 0 . && \
    chmod -R g=u . && \
    chmod -R g+rw . && \
    chmod a+x run.sh

USER 1001

CMD ./run.sh