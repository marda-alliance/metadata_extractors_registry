from pathlib import Path

from invoke import task

MODEL_DIRECTORY = Path(__file__).parent / "marda_registry" / "models"


@task
def regenerate_models(_):
    import glob

    import linkml.generators.pydanticgen as pd

    schemas = glob.glob("./schemas/schemas/*.yml")

    print("Regenerating pydantic models")

    if not schemas:
        raise RuntimeError("No schemas found")

    for schema in schemas:
        print(schema)
        schema_path = Path(schema)
        gen = pd.PydanticGenerator(schema, pydantic_version="2", verbose=True)
        output = gen.serialize()
        with open(MODEL_DIRECTORY / f"{schema_path.name.strip('.yml')}.py", "w") as f:
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
