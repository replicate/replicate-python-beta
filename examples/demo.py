from typing import Iterable, cast

import rich

from replicate import FileOutput, ReplicateClient

client = ReplicateClient()

outputs = client.run(
    "black-forest-labs/flux-schnell",
    input={"prompt": "astronaut riding a rocket like a horse"},
)
rich.print(outputs)
for index, output in enumerate(cast(Iterable[FileOutput], outputs)):
    with open(f"output_{index}.webp", "wb") as file:
        file.write(output.read())
