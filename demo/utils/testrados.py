
import rados

cluster = rados.Rados(conffile = 'ceph.conf', conf = dict (keyring = 'ceph.client.admin.keyring'))
cluster.connect()
ioctx = cluster.open_ioctx('data')
print([o.key for o in ioctx.list_objects()])
print ioctx.read('object-4')

