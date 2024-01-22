<div align="center" style="padding-bottom: 1em;">
<img width="100px" align="center" src="https://avatars.githubusercontent.com/u/74017645?s=200&v=4">
</div>

# <div align="center">MaRDA Metadata Extractors: Registry</div>

<div align="center">


[![Documentation](https://badgen.net/badge/docs/marda-registry.fly.dev/blue?icon=firefox)](https://marda-registry.fly.dev)
![Github status](https://badgen.net/github/checks/marda-alliance/metadata_extractors_registry/?icon=github)

</div>

A place to develop and discuss the MaRDA Extractors WG registry.
The idea is to collect various file formats used in materials science and chemistry, describe them with metadata, and provide links to software projects that can parse them.

By providing this data in a web API, it hoped that users can discover new extractors more easily and metadata standards can be developed for the output of extractors to enable schemas to proliferate throughout the field.

The state of the `main` branch is deployed to https://marda-registry.fly.dev/, with API docs (and built-in client) accessible at https://marda-registry.fly.dev/redoc.

## Contributing

You are welcome to contribute file type and extractor entries to this registry, by opening a pull request. Please see the [contributing guidelines](./CONTRIBUTING.md) for detailed steps. After submitting a pull request, this data will be validated and added to the deployed database once it is merged.

## Development

Clone repository with submodules and install deps in a fresh Python virtualenv:

```
git clone git@github.com:marda-alliance/marda_extractors_registry --recurse-submodules
pip install -r requirements.txt
```

Use `invoke` and the tasks in `tasks.py` to generate pydantic models for all
schemas defined in the schema repo:

```
invoke regenerate-models
```

From the repository root directory, launch the server with uvicorn:

```
uvicorn marda_registry.app:app
```

then navigate to http://localhost:5000 to test.

## Deployment

The registry app can be easily deployed via the given [Dockerfile](./Dockerfile).
After cloning the repository (with submodules, following the instructions above), the image can be built for a given schema version by running

```shell
docker build . -t marda-registry
```

and then launched with

```shell
docker run -p 8080 --env PORT=8080 marda-registry
```

or equivalent command.

## Registry Maintainers
- Matthew Evans, [@ml-evs](https://github.com/ml-evs)
- Peter Kraus, [@PeterKraus](https://github.com/PeterKraus)
