# :construction: kapply

**Version control for Kubernetes manifests**

## Why?

Not all softwares provide an [Helm Chart](https://helm.sh) to deploy on
Kubernetes. You'll often find commands like:

```
$ kubectl apply -f https://example.com/a-very-long-static.yaml
```

The biggest problem to this method arise when you want to upgrade (aka: apply
the next version of your YAML file). If the new version "deletes" some
resources, the `kubectl apply` command won't.

## How?

This tool takes as input:

 - a release name and namespace
 - a Kubernetes manifest as YAML

A **SHA256** hash is created from the YAML and is used as *revision number*.

A secret for the *revision* is created with the following properties:

| Property | Value |
| --- | --- |
| metadata.name | `kapply-release-${release_name}-revision-${hash}` |
| metadata.namespace | `release_namespace` |
| data.previousRevision | `previous_hash` or `""` |
| data.resources | JSON of the manifest |

**NB:** Data within the secret are encoded in Base64.

Then a secret for the *release* is created with the following properties:

| Property | Value |
| --- | --- |
| metadata.name | `kapply-release-${release_name}` |
| metadata.namespace | `release_namespace` |
| data.revision | `hash` |

The *release* secret points to the current *revision*, which points to the
previous one.

Then, the manifest is applied (just like `kubectl apply` does).

Finally, we compare the current manifest with the previous one if any. And for
every resource that do not exist in the new one, we delete them.

**NB:** This is still a **WORK IN PROGRESS**, and therefore this tool is not
foolproof.

## Installation

This tool is currently developped in Python (as a Proof of Concept), but it
could be rewritten in Go or Rust.

It also calls `kubectl` instead of directly talking to the Kubernetes API
Server.

You will need [Poetry](https://python-poetry.org/) to build the project:

A single executable can be produced thanks to [PyInstaller](https://pyinstaller.readthedocs.io/).

To build the executable, just run:

```
$ make
```

It will be located at `dist/kapply` (or `dist/kapply.exe` if you're on Windows).

## Usage

```
Usage: kapply [OPTIONS]

  Version control for Kubernetes manifests

Options:
  -r, --release TEXT    Name of the release's secret  [required]
  -n, --namespace TEXT  Namespace of the release's secret  [required]      
  -f, --manifest TEXT   URL or path to file/directory containing Kubernetes
                        resources  [required]

  --help                Show this message and exit.
```

## License

This project is released under the terms of the [MIT License](./LICENSE.txt)
