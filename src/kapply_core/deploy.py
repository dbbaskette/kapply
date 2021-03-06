from .resources import (
    encode_resources,
    load_resources,
    apply_resources,
    delete_resources
)

from .release import get_release, create_or_update_release
from .revision import get_revision, new_revision
from .namespace import ensure_namespace

from base64 import b64decode


def load_previous_signature(release):
    previous_signature = None

    if release is not None:
        previous_signature = release['data']['revision']
        previous_signature = b64decode(previous_signature).decode('utf-8')

    return previous_signature


def is_same_resource(item):
    def filter_func(other):
        item_meta = item['metadata']
        other_meta = other['metadata']

        return all([
            item_meta['name'] == other_meta['name'],
            item_meta.get('namespace') == other_meta.get('namespace')
        ])

    return filter_func


def get_deleted_resources(previous_resources, resources):
    deleted_resources = []

    for previous_resource in previous_resources:
        found = filter(is_same_resource(previous_resource), resources)

        if len(list(found)) == 0:
            deleted_resources.append(previous_resource)
    
    return deleted_resources


def deploy_release(release_name, release_namespace, resources):
    resources_dump, signature = encode_resources(resources)

    ensure_namespace(release_namespace)
    release = get_release(release_name, release_namespace)
    revision = get_revision(release_name, release_namespace, signature)

    previous_signature = load_previous_signature(release)

    if revision is None:
        revision = new_revision(
            release_name,
            release_namespace,
            signature,
            previous_signature,
            resources_dump
        )

    create_or_update_release(release_name, release_namespace, signature)
    previous_revision = get_revision(
        release_name,
        release_namespace,
        previous_signature
    )
    previous_resources = load_resources(previous_revision)

    resources = filter(
        lambda rsrc: rsrc is not None,
        resources
    )
    previous_resources = filter(
        lambda rsrc: rsrc is not None,
        previous_resources
    )

    deleted_resources = get_deleted_resources(previous_resources, resources)
    apply_resources(resources)
    delete_resources(deleted_resources)
