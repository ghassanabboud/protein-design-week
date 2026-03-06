# Here is a collection of example runs for for each model deployed in RCP.
# Use these first to verify that you can run the models, and then modify them to your needs.

# First, a template for opening a container with the model of your choice. 
# Fill in your gaspar username and job name then choose the correct model image before running the corresponding test command from the examples below.

runai submit <your_job_name> \
    --project hackathon-proteindesign-<gaspar_username> \
    -i registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1 \
    --interactive \
    --attach \
    --node-pools default \
    -g 1 \
    --existing-pvc claimname=hackathon-proteindesign-scratch-gXX,path=/mnt/scratch \
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

#boltz example: -i registry.rcp.epfl.ch/proteindesign-containers/boltz:2026.1
# for more details on configuring runs, run "boltz predict --help" inside the container
# or consult official repository guide with example configs: https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md

boltz predict /mnt/shared-ro/examples/boltz/prot_no_msa.yaml --out_dir /mnt/scratch/boltz_example/

#chai example: -i registry.rcp.epfl.ch/proteindesign-containers/chai:2026.1
# for more details on configuring runs, run "chai-lab --help" inside the container
# or consult official repository README: https://github.com/chaidiscovery/chai-lab
# with chai installed you can also run jobs from a python script like in the repo's examples: https://github.com/chaidiscovery/chai-lab/tree/main/examples

chai-lab fold /mnt/shared-ro/examples/chai/8cyo.fasta /mnt/scratch/example-ghassan-chai --constraint-path /mnt/shared-ro/examples/chai/8cyo.restraints 

#af3 example: -i registry.rcp.epfl.ch/proteindesign-containers/af3:2026.1
