from invoke import task

@task
def regenerate_models(c):
    import linkml.generators.pydanticgen as pd
    import glob

    schemas = glob.glob("./schemas/schemas/*.yml")

    if not schemas:
        raise RuntimeError("No schemas found")

    for schema in schemas:
        print(schema)
        gen = pd.PydanticGenerator(schema, output="./models", verbose=True)
        gen.serialize()
        print("Done")

