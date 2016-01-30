import rados
import re

CEPH_CONF = 'demo/utils/ceph.conf'
KEYRING   = 'demo/utils/ceph.client.admin.keyring'
POOL      = 'data'
ioctx     = None

def connected(error_value=None):
    def decorator(f):
        def wrapped(*args, **kwargs):
            global ioctx
            try:
                cluster = rados.Rados(conffile=CEPH_CONF, 
                                      conf=dict(keyring=KEYRING))
                cluster.connect(timeout=2)
                ioctx = cluster.open_ioctx(POOL)
                return f(*args, **kwargs)
            except:
                return error_value
            finally:
                cluster.shutdown()
        return wrapped
    return decorator

@connected(error_value=[])
def get_object_list():
    return [o.key for o in ioctx.list_objects()]

@connected(error_value="")
def get_data(obj):
    return ioctx.read(str(obj))

@connected(error_value=False)
def delete_object(obj):
    ioctx.remove_object(str(obj))
    return True

@connected(error_value=False)
def store_object(name, data):
    ioctx.write_full(str(name), str(data))
    return True

def exists(name):
    return name in get_object_list()

def is_valid_name(name):
    return bool(re.match(r'^[a-zA-Z0-9\-]+$', name))

# should probably never be used
def startup_cluster():
    from subprocess import call
    call(['start-ceph'])

