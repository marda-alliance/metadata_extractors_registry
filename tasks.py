from pathlib import Path

from invoke import task

MODEL_DIRECTORY = Path(__file__).parent / "marda_registry" / "models"


@task
def regenerate_models(_):
    import glob

    import linkml.generators.pydanticgen as pd

    schemas = glob.glob("./schemas/schemas/*.yml")

    if not schemas:
        raise RuntimeError("No schemas found")

    for schema in schemas:
        print(schema)
        schema_path = Path(schema)
        gen = pd.PydanticGenerator(schema, verbose=True)
        output = gen.serialize()
        with open(MODEL_DIRECTORY / f"{schema_path.name.strip('.yml')}.py", "w") as f:
            f.writelines(output)

        print("Done")
