from base64 import decodebytes
import paramiko

from base.settings import REMOTE_HOST, REMOTE_HOST_KEY, REMOTE_PASSWORD, REMOTE_USERNAME


def upload_file_to_server(file_path, document_name):
    keydata = REMOTE_HOST_KEY.encode()
    keydata = paramiko.Ed25519Key(data=decodebytes(keydata))

    ssh = paramiko.SSHClient()

    ssh.get_host_keys().add(REMOTE_HOST, "ssh-rsa", keydata)
    ssh.connect(REMOTE_HOST, username=REMOTE_USERNAME, password=REMOTE_PASSWORD)

    sftp = ssh.open_sftp()
    sftp.put(localpath=file_path, remotepath=f"/home/comais/documentos/{document_name}")

    sftp.close()
    ssh.close()
