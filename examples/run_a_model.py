import rich

from replicate import Replicate

client = Replicate()

outputs = client.run(
    "black-forest-labs/flux-schnell",
    input={"prompt": "astronaut riding a rocket like a horse"},
)
rich.print(outputs)
for index, output in enumerate(outputs):
    with open(f"output_{index}.webp", "wb") as file:
        file.write(output.read())
