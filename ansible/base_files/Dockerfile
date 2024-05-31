FROM quay.io/jupyterhub/jupyterhub

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

RUN apt-get install -y openssl

RUN python3 -m pip install jupyter-core jupyter-server jupyterlab notebook

ENV TURMA=$TURMA

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]