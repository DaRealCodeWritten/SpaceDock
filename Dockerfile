FROM python:3.7.3 as backend-dev
ENV PYTHONUNBUFFERED=1
WORKDIR /opt/spacedock
RUN pip3 install --upgrade pip setuptools wheel pip-licenses
ADD requirements.txt ./
RUN pip3 install -r requirements.txt
ADD . ./
RUN pip3 install -v ./

FROM backend-dev as celery
ADD requirements-celery.txt ./
RUN pip3 install -r requirements-celery.txt

FROM backend-dev as backend-prod
ADD requirements-prod.txt ./
RUN pip3 install -r requirements-prod.txt
