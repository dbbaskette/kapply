from kapply_core.manifest import get_manifest
from kapply_core.deploy import deploy_release
import click


@click.command()
@click.option(
    '-r', '--release',
    'release_name',
    required=True,
    help="Name of the release's secret"
)
@click.option(
    '-n', '--namespace',
    'release_namespace',
    required=True,
    help="Namespace of the release's secret"
)
@click.option(
    '-f', '--manifest',
    'manifest_location',
    required=True,
    help='URL or path to file/directory containing Kubernetes resources'
)
def main(release_name, release_namespace, manifest_location):
    """Version control for Kubernetes manifests"""

    resources = get_manifest(manifest_location)
    deploy_release(release_name, release_namespace, resources)


if __name__ == '__main__':
    main()
