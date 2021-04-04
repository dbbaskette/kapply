from tempfile import TemporaryFile
from base64 import b64decode
from hashlib import sha256
import subprocess
import yaml
import json


def encode_resources(resources):
    resources_dump = json.dumps(resources)

    signature = sha256()
    signature.update(resources_dump.encode('utf-8'))
    signature = signature.hexdigest()

    return resources_dump, signature


def load_resources(revision):
    if revision is not None:
        resources_dump = revision['data']['resources']
        resources_dump = b64decode(resources_dump).decode('utf-8')
        return json.loads(resources_dump)

    return []


def fetch_resource(kind, name, namespace):
    if namespace is not None:
        cmd = ['kubectl', 'get', '-n', namespace, kind, name, '-o', 'json']

    else:
        cmd = ['kubectl', 'get', kind, name, '-o', 'json']

    with TemporaryFile('rb+') as outf:
        proc = subprocess.Popen(
            cmd,
            stdout=outf,
            stderr=subprocess.STDOUT
        )
        code = proc.wait()
        outf.seek(0)

        if code != 0:
            output = outf.read().decode('utf-8')

            if 'NotFound' in output:
                return None

            else:
                raise RuntimeError(output)

        return json.load(outf)


def apply_resource(resource):
    resource = yaml.dump(resource)
    proc = subprocess.Popen(
        ['kubectl', 'apply', '-f', '-'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    proc.stdin.write(resource.encode('utf-8'))
    proc.stdin.close()
    
    code = proc.wait()
    output = proc.stdout.read().decode('utf-8')

    if code != 0:
        raise RuntimeError(output)

    print(output, end='')


def apply_resources(resources):
    for resource in resources:
        if resource:
            apply_resource(resource)


def delete_resource(resource):
    namespace = resource['metadata'].get('namespace')
    name = resource['metadata']['name']
    kind = resource['kind'].lower()

    if namespace is not None:
        cmd = ['kubectl', 'delete', '-n', namespace, kind, name]

    else:
        cmd = ['kubectl', 'delete', kind, name]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    code = proc.wait()
    output = proc.stdout.read().decode('utf-8')

    if code != 0:
        raise RuntimeError(output)

    print(output, end='')


def delete_resources(resources):
    for resource in resources:
        if resource:
            delete_resource(resource)
