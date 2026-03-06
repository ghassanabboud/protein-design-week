# Here is a collection of example runs for for each model deployed in RCP.
# Use these first to verify that you can run the models, and then modify them to your needs.

# First, a template for opening a container with the model of your choice. 
# Fill in your gaspar username and job name then choose the correct model iamage.

runai submit <your_job_name> \
    --project hackathon-proteindesign-<gaspar_username> \
    -i registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1 \
    --interactive \
    --attach \
    --node-pools default \
    -g 1 \
    --existing-pvc claimname=hackathon-proteindesign-scratch-g11,path=/mnt/scratch \
    --existing-pvc claimname=hackathon-proteindesign-shared-ro,path=/mnt/shared-ro \
    --command -- /bin/bash

# RFDiffusion3 example: -i registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1
# for more details on configuring runs, see RFDiffusion3 documentation: https://rosettacommons.github.io/foundry/models/rfd3/input.html

rfd3 design \
    out_dir=/mnt/scratch/rfd3-example/ \
    inputs=/mnt/shared-ro/examples/rfd3/demo.json  \
    ckpt_path=/mnt/shared-ro/weights/rfd3/rfd3_latest.ckpt \
    n_batches=1 \
    diffusion_batch_size=8

# LigandMPNN example: -i registry.rcp.epfl.ch/proteindesign-containers/ligandmpnn:2026.1
# for more details on configuring runs, run "python run.py --help" inside the container
# or consult official repository README: https://github.com/dauparas/LigandMPNN/tree/main

python run.py \
    --pdb_path "/mnt/shared-ro/examples/ligandmpnn/1BC8.pdb" \
    --out_folder "/mnt/scratch/ligandmpnn_example/" \
    --model_type "ligand_mpnn" \
    --checkpoint_ligand_mpnn "/mnt/shared-ro/weights/ligandmpnn/ligandmpnn_v_32_005_25.pt" \
    --batch_size 8 \
    --number_of_batches 1

# Carbonara example: -i registry.rcp.epfl.ch/proteindesign-containers/carbonara:2026.1
# for more details on configuring runs, run "carbonara --help" inside the container
# or consult official repository README: https://github.com/LBM-EPFL/CARBonAra/tree/main

carbonara \
    --num_sequences 100 \
    --imprint_ratio 0.5 \
    /mnt/shared-ro/examples/carbonara/2oob.pdb /mnt/scratch/carbonara_example/
#TODO it throws an error idk how to solve

#boltz example: -i registry.rcp.epfl.ch/proteindesign-containers/boltz:2026.1