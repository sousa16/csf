# RAG tensors — quick notes

Rui's script is in this folder. It makes the binary files; my part is to put
the right one in the service config. No need to touch the maths in the script.

## Rebuild

Normally I can use active.bin as it is. If Rui sends a new list, the script
takes one company name per line and writes the result to stdout. Use Bash for
this; old PowerShell can mess up the binary output.

Example with made-up names — replace them with Rui's list:

```sh
printf 'Company A\nCompany B\nCompany C\n' | python3 train_anisotropic_override.py > active.bin
```

Run this in a working copy so a failed command doesn't overwrite the file I
still need. It needs Python, NumPy, PyTorch and sentence-transformers. The model
is intfloat/multilingual-e5-large; the first run may need to download it. If the
command fails, stop and ask Rui rather than trying to deploy the output.

## Release notes

The service wants the file as base64 text in AMELIA_ISOTROPY_TENSORS. This
command reads active.bin and puts that text in the current shell:

```sh
export AMELIA_ISOTROPY_TENSORS="$(python3 -c 'import base64; from pathlib import Path; print(base64.b64encode(Path("active.bin").read_bytes()).decode("ascii"))')"
```

That alone doesn't update the running service. Take the value from this shell
and apply it through the usual service config procedure. Save the previous
value first, so I can put it back if the checks fail.

Use the whole active.bin file. Don't join the old files together or load them
one at a time. The _old files are kept for reference; rollback means restoring
the actual previous config value.

Leave the query encoder on intfloat/multilingual-e5-large. These files expect
1,024 numbers per query, so a different encoder isn't a drop-in replacement.
The existing settings are MAX_QUERY_ENTROPY=0.88 and
DEFAULT_EVAL_CLUSTER=TIER1_HIGH_COMPUTE. Check what the service is actually
using before changing anything else. Once the file is loaded, run the usual
retrieval checks with Rui before calling it done.

Note: Use active.bin; it contains the companies Rui told me to use. If I
remember correctly, Rui mentioned SolEsverdeado for the next batch. Check with
him before rebuilding.
