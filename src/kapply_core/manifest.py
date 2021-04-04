from functools import reduce
import requests
import yaml
import os


def get_manifest_file(location):
    with open(location) as f:
        return list(yaml.load_all(f, Loader=yaml.SafeLoader))


def get_manifest_dir(location):
    resource_paths = []
    for dirname, subdirs, files in os.walk(location):
        files = filter(
            lambda f: any([
                f.lower().endswith('.yml'),
                f.lower().endswith('.yaml')
            ]),
            files
        )
        files = map(
            lambda f: os.path.join(dirname, f),
            files
        )
        resource_paths += files
        
    resources = map(get_manifest_file, resource_paths)
    resources = reduce(
        lambda acc, rsrcs: acc + rsrcs,
        resources,
        []
    )
    return list(resources)


def get_manifest_url(location):
    resp = requests.get(location)

    if not (200 <= resp.status_code < 300):
        raise RuntimeError(f'Unable to fetch manifest "{location}": {resp.status_code}')

    return list(yaml.load_all(resp.text, Loader=yaml.SafeLoader))


def get_manifest_fs(location):
    location = os.path.expanduser(location)

    if not os.path.exists(location):
        raise RuntimeError(f'Unable to open manifest "{location}": no such file or directory')

    if os.path.isdir(location):
        return get_manifest_dir(location)

    else:
        return get_manifest_file(location)


def get_manifest(location):
    if '://' in location:
        if location.startswith('file://'):
            return get_manifest_fs(location[len('file://'):])

        return get_manifest_url(location)

    else:
        return get_manifest_fs(location)
