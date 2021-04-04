from .resources import fetch_resource, apply_resource

from base64 import b64encode
import subprocess
import yaml


def get_secret_name(name, signature):
    return f'kapply-release-{name}-revision-{signature}'


def get_revision(name, namespace, signature):
    secret_name = get_secret_name(name, signature)
    return fetch_resource('secret', secret_name, namespace)


def create_revision(name, namespace, signature, previous, resources_dump):
    apply_resource({
        'apiVersion': 'v1',
        'kind': 'Secret',
        'metadata': {
            'name': get_secret_name(name, signature),
            'namespace': namespace,
            'labels': {
                'app.kubernetes.io/managed-by': 'kapply',
                'kapply.io/kind': 'revision'
            }
        },
        'data': {
            'previousRevision': (
                b64encode(previous.encode('utf-8')).decode('utf-8')
                if previous is not None
                else ''
            ),
            'resources': b64encode(resources_dump.encode('utf-8')).decode('utf-8')
        }
    })


def new_revision(
    release_name,
    release_namespace,
    signature,
    previous_signature,
    resources_dump
):
    create_revision(
        release_name,
        release_namespace,
        signature,
        previous_signature,
        resources_dump
    )

    return get_revision(release_name, release_namespace, signature)
