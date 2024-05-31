c.JupyterHub.trusted_downstream_ips = ['127.0.0.1']  # Adicione o IP do seu proxy reverso aqui
#c.JupyterHub.bind_url = 'http://127.0.0.1:8000'$TURMA

import os
turma = os.getenv('TURMA')
c.JupyterHub.base_url = turma