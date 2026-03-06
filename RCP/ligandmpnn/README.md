# LigandMPNN

Protein sequence design tool. Given a protein backbone structure (and optionally ligands, nucleic acids, metals), designs amino acid sequences that fold into the desired structure.

- **GitHub**: https://github.com/dauparas/LigandMPNN
- **Container**: `registry.rcp.epfl.ch/proteindesign-containers/ligandmpnn:2026.1`
- **Model weights**: Pre-downloaded in the container at `/opt/LigandMPNN/model_params/`. Also available on the shared-ro volume.

> For building and pushing the Docker image, see [docker/README.md](docker/README.md).

## Launch on RunAI

```bash
runai submit ligandmpnn-gXX \
  --project <your-project> \
  -i registry.rcp.epfl.ch/proteindesign-containers/ligandmpnn:2026.1 \
  --interactive \
  --attach \
  --node-pools default \
  -g 1 \
  --existing-pvc claimname=hackathon-proteindesign-scratch-gXX,path=/mnt/scratch \
  --existing-pvc claimname=hackathon-proteindesign-shared-ro,path=/mnt/shared-ro \
  --command -- /bin/bash
```

Replace `gXX` with your group number and `<your-project>` with your RunAI project name.

## Getting Started

### Design sequences for a protein backbone

```bash
cd /opt/LigandMPNN
mkdir -p /mnt/scratch/ligandmpnn-demo

python run.py \
  --model_type "ligand_mpnn" \
  --checkpoint_ligand_mpnn /opt/LigandMPNN/model_params/ligandmpnn_v_32_010_25.pt \
  --pdb_path /mnt/scratch/ligandmpnn-demo/input.pdb \
  --out_folder /mnt/scratch/ligandmpnn-demo/output \
  --number_of_batches 1 \
  --batch_size 8
```

### Design with a ligand context

```bash
python run.py \
  --model_type "ligand_mpnn" \
  --checkpoint_ligand_mpnn /opt/LigandMPNN/model_params/ligandmpnn_v_32_010_25.pt \
  --pdb_path /mnt/scratch/input_complex.pdb \
  --out_folder /mnt/scratch/output \
  --number_of_batches 1 \
  --batch_size 8
```

### Design with fixed residues

```bash
python run.py \
  --model_type "ligand_mpnn" \
  --checkpoint_ligand_mpnn /opt/LigandMPNN/model_params/ligandmpnn_v_32_010_25.pt \
  --pdb_path /mnt/scratch/input.pdb \
  --out_folder /mnt/scratch/output \
  --fixed_residues "C1 C2 C3 C4 C5" \
  --number_of_batches 1 \
  --batch_size 8
```

### Using ProteinMPNN (no ligand context)

```bash
python run.py \
  --model_type "protein_mpnn" \
  --checkpoint_protein_mpnn /opt/LigandMPNN/model_params/proteinmpnn_v_48_020.pt \
  --pdb_path /mnt/scratch/input.pdb \
  --out_folder /mnt/scratch/output \
  --number_of_batches 1 \
  --batch_size 8
```

## Available Model Checkpoints

| Model | Checkpoint | Use case |
|-------|-----------|----------|
| LigandMPNN | `ligandmpnn_v_32_010_25.pt` | Design with ligand/small molecule context |
| ProteinMPNN | `proteinmpnn_v_48_020.pt` | Protein-only sequence design |
| SolubleMPNN | `solublempnn_v_48_020.pt` | Design for soluble proteins |

All checkpoints are in `/opt/LigandMPNN/model_params/`.

### Using weights from shared volume

```bash
python run.py \
  --model_type "ligand_mpnn" \
  --checkpoint_ligand_mpnn /mnt/shared-ro/models/ligandmpnn/ligandmpnn_v_32_010_25.pt \
  --pdb_path input.pdb \
  --out_folder /mnt/scratch/output
```

## References

- [LigandMPNN GitHub](https://github.com/dauparas/LigandMPNN)
- [LigandMPNN paper](https://doi.org/10.1101/2023.12.22.573103)
