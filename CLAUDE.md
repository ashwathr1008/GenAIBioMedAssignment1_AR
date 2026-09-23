# Assignment 1: ProGen2 finetuning (02-741 / 11-781 Generative AI for Biomedicine)

Assignment spec: https://genaibiomed.github.io/GenAIBioMedAssignment1/

## Compute: PSC Bridges-2

- PSC username: `raghuram`
- Charge ID: `cis260266p` (the course allocation, set as default; GPU SUs only, **no RM/CPU allocation**)
- `$HOME` = `/jet/home/raghuram` (25 GB, keep small)
- `$PROJECT` = `/ocean/projects/cis260266p/raghuram` (Ocean; put envs, checkpoints, outputs here)
- Repo on Bridges-2: `$PROJECT/GenAIBioMedAssignment1_AR`
- Never run heavy work on login nodes (`bridges2-login*` / `br0*`). Check with `hostname`.

## How the user connects

VS Code Remote-SSH from Windows to host `b2-gpu` (defined in the user's local `~/.ssh/config`).
It goes through the login node and runs `salloc --partition=GPU-shared --gres=gpu:v100-32:1 --time=4:00:00`,
so a VS Code session *is* a Slurm job on a V100 node: it ends after 4 h or when the remote connection closes.
Other local hosts: `bridges2` (login node), `b2-data` (data.bridges2.psc.edu, for scp/rsync).

## Environment

```bash
module load anaconda3/2024.10-1
conda activate $PROJECT/envs/progen   # python 3.9.16, torch 2.7.0 (cu128), transformers 4.49.0
```

Pretrained weights: `pretrained_model/progen2-small/` (downloaded per the spec). Finetuned outputs go in `models/`.

## Running

- Short runs / debugging: directly in the VS Code terminal (already on the GPU node).
- Long training: submit a batch job so it survives VS Code disconnects, e.g.

```bash
#!/bin/bash
#SBATCH -p GPU-shared
#SBATCH --gres=gpu:v100-32:1
#SBATCH -t 08:00:00
#SBATCH -o logs/%x-%j.out
module load anaconda3/2024.10-1
conda activate $PROJECT/envs/progen
python train.py
```

  Submit with `sbatch`, monitor with `squeue -u raghuram`, cancel with `scancel <jobid>`.
- Opening a second VS Code window on `b2-gpu` starts a second GPU job (Windows OpenSSH has no connection reuse). Check `squeue` for strays.
- Check the remaining balance with `projects`.

## Deliverables

A zip of the completed code (no data files) plus a PDF report on the top-5 designed candidates:
AlphaFold3 visualizations, sequences, pTM/pLDDT, substitution tables, positional distribution analysis,
the decoding strategy, and an interpretation paragraph. See the spec for details.
