FROM quay.io/jupyterhub/jupyterhub

RUN jupyterhub --generate-config

RUN apt-get install -y openssl

RUN python3 -m pip install jupyter-core jupyter-server jupyterlab notebook

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]