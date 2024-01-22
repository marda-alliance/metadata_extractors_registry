<div align="center" style="padding-bottom: 1em;">
<img width="100px" align="center" src="https://avatars.githubusercontent.com/u/74017645?s=200&v=4">
</div>

# <div align="center">MaRDA Metadata Extractors: Registry</div>
## <div align="center">Contributing guidelines</div>

Contributions to this registry are welcome. We pledge to follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

You can contribute `FileType` and `Extractor` entries to this registry by creating pull requests (PRs), which should include YAML files under `./data/filetypes` and `./data/extractors`, respectively. These YAML files  must follow the schemas at [marda-alliance/metadata_extractors_schema](https://github.com/marda-alliance/metadata_extractors_schema) (see the [online documentation](https://marda-alliance.github.io/metadata_extractors_schema) for more details).

An example of the process can be seen in this [pull request](https://github.com/marda-alliance/metadata_extractors_registry/pull/54). The workflow steps are as follows:


### Opening a pull request
- One pull request (PR) per `Extractor`, please.
    - You can include multiple versions of one `Extractor` in separate `.yml` files.
    - Do not include multiple unrelated `Extractors` in a single PR.
- Include any missing `FileTypes` supported by the `Extractor` in the same PR.
- Please add the appropriate labels (`Extractor` and `FileType`).

### Example files
- If you are adding new `FileTypes` in this PR, add example files of those `FileTypes` using `git-lfs` into `marda_registry/data/lfs`. Do not commit example files into the repository directly. For example, to add a new file called `xmpl.tpe` (corresponding to the `FileType` with ID `example-type`) you would:

  ``` bash
    mkdir marda_registry/data/lfs/example-type  # create the dir using FileType ID
    cp xmpl.tpe marda_registry/data/lfs/example-type  # copy the example file
    git lfs install  # setup git-lfs, only necessary if you haven't used git-lfs before
    git add marda_registry/data/lfs/example-type/*  # track files
    ...
    git lfs ls-files  # check that your new example files are tracked before committing
    git commit
    git push
  ```

### Validation of Definitions
- Your PR will have to pass the testing using our continuous integration (CI) set-up. The CI checks the following three things:
    - `lint`, making sure the `yml` files you added are properly formatted,
    - `validate`, which validates the `yml` files against their schemas, and
    - `build`, which makes sure the new registry website can be built.

  Therefore, it is mainly the `lint` and `validate` actions you will have to pay attention to. In case anything is unclear or you cannot find the error, ping one of the [Registry Maintainers](./README.md#registry-maintainers).
- You can of course validate your definitions locally, by using the [![Schema](https://badgen.net/static/marda-alliance/metadata_extractors_schema/?icon=github)](https://github.com/marda-alliance/metadata_extractors_schema/) package, see the [Usage section](https://marda-alliance.github.io/metadata_extractors_schema/main/usage.html) of the documentation.

### Testing of Extraction
- You should check that your `yml` definitions can be used to install the `Extractor` and and extract any example files from the supported `FileTypes` locally, by using our [![Schema](https://badgen.net/static/marda-alliance/metadata_extractors_api/?icon=github)](https://github.com/marda-alliance/metadata_extractors_api/) package, see the [Installation](https://github.com/marda-alliance/metadata_extractors_api#installation) and [Usage](https://github.com/marda-alliance/metadata_extractors_api#usage) sections.

> At the moment, the above CI is not checking whether the extraction of the example files actually works. See [this issue](https://github.com/marda-alliance/metadata_extractors_registry/issues/34) for further details.

### Approval and Deployment
- If you are a first-time contributor to the project, we will need to pre-approve your PR so that the CI can be run. Ping one of the [Registry Maintainers](./README.md#registry-maintainers).
- Once the CI passes, and all issues that are raised during the review are addressed, your PR can be merged.
- Once your PR is merged into the Registry, your new definitions should be available at the [Registry Website](https://marda-registry.fly.dev/). Cheers!