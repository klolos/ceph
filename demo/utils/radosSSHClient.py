import paramiko
import tempfile
import os
import re
from subprocess import call

CEPH_ADMIN = 'admin-node'
CEPH_ADMIN_PORT = 22
USERNAME = 'kostis'
PASSWORD = 'secretpw'
KEY_PATH = '/home/kostis/.ssh/id_rsa'
REMOTE_VAR_PATH = '/var/local/ceph-app'

def test_function():
    return get_data('test-object-3')

def _execute_cmd(cmd, username=USERNAME):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(CEPH_ADMIN, username=username)
        _, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.readlines()
        err = stderr.readlines()
        return out, err
    except Exception as e:
        return [], [str(e)]
    finally:
        ssh.close()

def get_object_list():
    out, err = _execute_cmd('rados -p data ls')
    return [l.strip() for l in out]

def get_data(obj):
    out, err = _execute_cmd('/home/kostis/get_data.sh ' + str(obj))
    return ''.join(out).strip()

def delete_object(obj):
    out, err = _execute_cmd('rados rm %s -p data' % str(obj))
    return not bool(err)

def store_object(name, data, username=USERNAME):
    transport = paramiko.Transport((CEPH_ADMIN, CEPH_ADMIN_PORT))
    key = paramiko.RSAKey.from_private_key_file(KEY_PATH)
    try:
        f = tempfile.NamedTemporaryFile()
        f.write(str.encode(str(data)))
        f.flush()

        # Transfer the data file to the admin node
        transport.connect(username=username, pkey=key)
        transport.open_channel("session", username, "localhost")
        sftp = paramiko.SFTPClient.from_transport(transport)
        remote_path = os.path.join(REMOTE_VAR_PATH, 
                                   os.path.basename(f.name))
        sftp.put(f.name, remote_path)

        # insert the data into ceph
        out, err = _execute_cmd('rados put %s %s -p data' % \
                                (str(name), remote_path))
        return not bool(err)
    except:
        return False
    finally:
        transport.close()

def is_valid_name(name):
    return bool(re.match(r'^[a-zA-Z0-9\-]+$', name))

def exists(name):
    return name in get_object_list()

def startup_cluster():
    call(['start-ceph'])

