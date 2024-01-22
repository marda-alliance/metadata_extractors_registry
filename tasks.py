from pathlib import Path

from invoke import task

MODEL_DIRECTORY = Path(__file__).parent / "marda_registry" / "models"


@task
def regenerate_models(_):
    import glob

    import linkml.generators.pydanticgen as pd

    schemas = glob.glob("./schemas/schemas/*.yaml")

    print("Regenerating pydantic models")

    if not schemas:
        raise RuntimeError(
            "No schemas found; check that the `schemas` git submodule is available"
        )

    for schema in schemas:
        print(schema)
        schema_path = Path(schema)
        gen = pd.PydanticGenerator(schema, pydantic_version="2", verbose=True)
        output = gen.serialize()
        with open(MODEL_DIRECTORY / f"{schema_path.name.strip('.yaml')}.py", "w") as f:
            f.writelines(output)

    print("Done!")


@task(pre=[regenerate_models])
def validate_entries(_):
    print("Validating entries")

    from marda_registry.models import Extractor, FileType
    from marda_registry.utils import load_registry_collection

    counts = {}
    for type_ in (FileType, Extractor):
        counts[type_] = load_registry_collection(
            type_,
            database=None,
            validate=True,
        )
        print(f"Loaded {counts[type_]} {type_.__name__} entries")

    print("Done!")


@task
def check_for_yaml(_):
    from pathlib import Path

    print("Checking for erroneous .yaml files.")

    extractors = list(
        Path(__file__).parent.glob("./marda_registry/data/extractors/*.yaml")
    )
    filetypes = list(
        Path(__file__).parent.glob("./marda_registry/data/filetypes/*.yaml")
    )

    for e in extractors:
        print(f"Found {e} with bad file extension (should be .yml here)")

    for f in filetypes:
        print(f"Found {f} with bad file extension (should be .yml here)")

    if extractors or filetypes:
        raise RuntimeError(f"Found files with bad extensions: {filetypes} {extractors}")

    print("Done!")
