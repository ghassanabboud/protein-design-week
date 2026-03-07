from gradio_client import Client, file
import os
from pathlib import Path
import time

def call_rfdiffusion3_space(
    config_file: str,
    scaffold_pdb: str = None,
    num_batches: int = 2,
    num_designs_per_batch: int = 8,
    extra_args: str = "",
    max_duration: int = 300,
    hf_token: str = None,
    output_dir: str = "./results_rfd3_api_call",
):
    """
    Call the RFdiffusion3 Space API from a local machine.
    
    Args:
        config_file: Path to RFD3 configuration file (.yaml or .json)
        scaffold_pdb: Path to target/scaffold PDB file for conditional generation (optional)
        num_batches: Number of batches to generate (default: 2)
        num_designs_per_batch: Number of designs per batch (default: 8)
        extra_args: Additional CLI arguments for RFD3 (e.g., "inference_sampler.step_scale=3")
        max_duration: Maximum duration in seconds (default: 300)
        hf_token: HuggingFace API token for private spaces (optional)
        output_dir: Directory to save downloaded results (default: "./results_rfd3_api_call")
    
    Returns:
        tuple: (status_message, results, output_zip_file)
    """
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = Client("hugging-science/RFdiffusion3", token=hf_token, download_files=output_dir)
    
    # Prepare the config file for upload
    if not os.path.exists(config_file):
        raise ValueError(f"Config file not found: {config_file}")
    
    config_file_obj = file(config_file)
    print(f"Added config file: {config_file}")
    
    # Prepare the scaffold PDB file if provided
    scaffold_file_obj = None
    if scaffold_pdb:
        if os.path.exists(scaffold_pdb):
            scaffold_file_obj = file(scaffold_pdb)
            print(f"Added scaffold file: {scaffold_pdb}")
        else:
            print(f"Warning: Scaffold file not found: {scaffold_pdb}")
    
    
    print(f"Submitting job with {num_batches} batches of {num_designs_per_batch} designs...")
    
    job = client.submit(
        input_file=config_file_obj,
        pdb_file=scaffold_file_obj,
        num_batches=num_batches,
        num_designs_per_batch=num_designs_per_batch,
        extra_args=extra_args,
        max_duration=max_duration,
        api_name="/generation_with_input_config"
    )
    
    print("Waiting for job to complete...")
    while not job.done():
        time.sleep(1)

    # Get outputs
    status_message, output_zip = job.outputs()[0]
    
    return status_message, output_zip

def call_ligandmpnn_space(
    pdb_files: list,
    num_batches: int = 5,
    num_designs_per_batch: int = 2,
    chains_to_design: str = "",
    temperature: float = 0.3,
    extra_args: str = "",
    max_duration: int = 300,
    hf_token: str = None,
    output_dir: str = "./results_ligandmpnn_api_call"
):
    """
    Call the LigandMPNN Space API from a local machine.
    
    Args:
        pdb_files: List of paths to PDB files to process
        num_batches: Number of batches (default: 5)
        num_designs_per_batch: Number of designs per batch (default: 2)
        chains_to_design: Comma-separated chains to design (default: all chains)
        temperature: Temperature for sampling (default: 0.3)
        extra_args: Additional CLI arguments (default: "")
        max_duration: Maximum duration in seconds (default: 3600)
        hf_token: HuggingFace API token for private spaces (optional)
        output_dir: Local directory to save results (optional)
    
    Returns:
        tuple: (status_message, output_directory)
    """

    client = Client("hugging-science/LigandMPNN", token=hf_token, download_files=output_dir)
    
    # Prepare the list of file objects for upload
    file_list = []
    for pdb_path in pdb_files:
        if os.path.exists(pdb_path):
            file_list.append(file(pdb_path))
            print(f"Added file: {pdb_path}")
        else:
            print(f"Warning: File not found: {pdb_path}")
    
    if not file_list:
        raise ValueError("No valid PDB files provided")
    
    job = client.submit(
        pdb_folder=file_list,
        num_batches=num_batches,
        num_designs_per_batch=num_designs_per_batch,
        chains_to_design=chains_to_design,
        temperature=temperature,
        extra_args=extra_args,
        max_duration=max_duration,
        api_name="/run_generation_folder"
    )
    
    print("Waiting for job to complete...")
    while not job.done():
        time.sleep(1)

    status_message, output_directory = job.outputs()[0]
    
    print("Status:", status_message)
    print("Output Directory:", output_directory)
    
    return status_message, output_directory

def call_rosettafold3_space(
    job_files: list,
    support_files: list = None,
    num_predictions: int = 5,
    early_stopping: float = 0.5,
    diffusion_steps: int = 200,
    max_duration: int = 300,
    hf_token: str = None,
    output_dir: str = "./results_rf3_api_call",
):
    """
    Call the RosettaFold3 Space API from a local machine.
    
    Args:
        job_files: List of paths to job files (.json, .pdb, or .cif files)
        support_files: List of paths to support files (.pdb, .cif, or .gz files) for templating/MSA (optional)
        num_predictions: Number of structure predictions per job (default: 5)
        early_stopping: pLDDT threshold for early stopping, 0 to disable (default: 0.5)
        diffusion_steps: Number of diffusion steps (default: 200)
        max_duration: Maximum duration in seconds (default: 500)
        hf_token: HuggingFace API token for private spaces (optional)
        output_dir: Directory to save downloaded results (default: "./results_rf3_api_call")
    
    Returns:
        tuple: (status_message, output_zip_file)
    """
    

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    client = Client("hugging-science/RosettaFold3", token=hf_token, download_files=output_dir)
    
    # Prepare the list of job file objects for upload
    job_file_list = []
    for job_path in job_files:
        if os.path.exists(job_path):
            job_file_list.append(file(job_path))
            print(f"Added job file: {job_path}")
        else:
            print(f"Warning: Job file not found: {job_path}")
    
    if not job_file_list:
        raise ValueError("No valid job files provided")
    
    # Prepare the list of support file objects for upload (optional)
    support_file_list = []
    if support_files:
        for support_path in support_files:
            if os.path.exists(support_path):
                support_file_list.append(file(support_path))
                print(f"Added support file: {support_path}")
            else:
                print(f"Warning: Support file not found: {support_path}")
    
    
    job = client.submit(
        job_files=job_file_list,
        support_files=support_file_list if support_file_list else None,
        num_predictions=num_predictions,
        early_stopping=early_stopping,
        diffusion_steps=diffusion_steps,
        max_duration=max_duration,
        api_name="/fold_all_jobs"
    )

    print("Waiting for job to complete...")
    while not job.done():
        time.sleep(1)

    status_message, output_zip = job.outputs()[0]

    
    print("Status:", status_message)
    print("Output Zip File:", output_zip)
    
    return status_message, output_zip