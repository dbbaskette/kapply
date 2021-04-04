from .resources import fetch_resource, apply_resource


def get_namespace(ns):
    return fetch_resource('namespace', ns, None)


def create_namespace(ns):
    apply_resource({
        'apiVersion': 'v1',
        'kind': 'Namespace',
        'metadata': {
            'name': ns,
            'labels': {
                'app.kubernetes.io/managed-by': 'kapply'
            }
        }
    })


def ensure_namespace(namespace):
    ns = get_namespace(namespace)

    if ns is None:
        create_namespace(namespace)
