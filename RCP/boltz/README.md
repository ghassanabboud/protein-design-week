# Boltz

Biomolecular structure prediction for proteins, ligands, and nucleic acids. Also supports binding affinity prediction.

- **GitHub**: https://github.com/jwohlwend/boltz
- **Container**: `registry.rcp.epfl.ch/proteindesign-containers/boltz:2026.1`
- **License**: MIT (code and weights)

> For building and pushing the Docker image, see [docker/README.md](docker/README.md).

## Launch on RunAI

```bash
runai submit boltz-gXX \
  --project <your-project> \
  -i registry.rcp.epfl.ch/proteindesign-containers/boltz:2026.1 \
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

### Check installation

```bash
boltz predict --help
```

### Predict a protein structure

Boltz uses YAML input format:

```bash
mkdir -p /mnt/scratch/boltz-demo
cd /mnt/scratch/boltz-demo

cat > protein.yaml << 'EOF'
version: 1
sequences:
- protein:
    id: A
    sequence: MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTGVITKDEAEKLFNQDVTAAAEELGLTQWPMFVVIIAKSATSAAHEEVKPSLL
EOF

boltz predict protein.yaml --use_msa_server
```

### Protein-ligand complex

```bash
cat > complex.yaml << 'EOF'
version: 1
sequences:
- protein:
    id: A
    sequence: MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTGVITKDEAEKLFNQDVTAAAEELGLTQWPMFVVIIAKSATSAAHEEVKPSLL
- ligand:
    id: B
    smiles: N[C@@H](Cc1ccc(O)cc1)C(=O)O
EOF

boltz predict complex.yaml --use_msa_server
```

### Binding affinity prediction

```bash
cat > affinity.yaml << 'EOF'
version: 1
sequences:
- protein:
    id: A
    sequence: MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTGVITKDEAEKLFNQDVTAAAEELGLTQWPMFVVIIAKSATSAAHEEVKPSLL
- ligand:
    id: B
    smiles: N[C@@H](Cc1ccc(O)cc1)C(=O)O

properties:
- affinity:
    ligand_chain: B
EOF

boltz predict affinity.yaml --use_msa_server
```

## Useful Options

```bash
boltz predict input.yaml \
  --use_msa_server \          # Auto-generate MSA via mmseqs2
  --recycling_steps 5 \       # Refinement iterations (default: 3)
  --diffusion_samples 3 \     # Number of samples (default: 1)
  --output_format pdb         # Output as PDB (default: mmCIF)
```

## Model Weights

Model weights are **automatically downloaded** on first run and cached in `/opt/boltz_cache`.

If weights are pre-downloaded to the shared volume:

```bash
boltz predict input.yaml --use_msa_server --cache /mnt/shared-ro/models/boltz
```

## References

- [Boltz GitHub](https://github.com/jwohlwend/boltz)
- [Boltz prediction docs](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md)
