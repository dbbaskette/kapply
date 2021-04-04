from .resources import fetch_resource, apply_resource

from base64 import b64encode


def get_secret_name(name):
    return f'kapply-release-{name}'


def get_release(name, namespace):
    secret_name = get_secret_name(name)
    return fetch_resource('secret', secret_name, namespace)


def create_or_update_release(name, namespace, revision):
    apply_resource({
        'apiVersion': 'v1',
        'kind': 'Secret',
        'metadata': {
            'name': get_secret_name(name),
            'namespace': namespace,
            'labels': {
                'app.kubernetes.io/managed-by': 'kapply',
                'kapply.io/kind': 'release'
            }
        },
        'data': {
            'revision': b64encode(revision.encode('utf-8')).decode('utf-8')
        }
    })
