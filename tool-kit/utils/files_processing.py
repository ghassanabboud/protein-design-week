import os
import glob
from pathlib import Path
from Bio.PDB import PDBParser, MMCIFParser, Select
from Bio.PDB import PDBIO
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import biotite
import numpy as np
import biotite.structure.io.pdb as pdb
import biotite.structure.io.pdbx as pdbx
import warnings
from Bio.PDB.PDBExceptions import PDBConstructionWarning

# ======================================================
# Tools for file handling and structure processing
# ======================================================
def find_structure_files(input_dir: str, extensions: list[str] = [".pdb", ".cif"], recursive: bool = True):
    """Finds structure files in the specified directory with given extensions.
        Input:
            - input_dir: The directory to search for structure files.
            - extensions: A list of file extensions to look for (default: [".pdb", ".cif"]).
            - recursive: Whether to search subdirectories recursively (default: True).
        Output:
            - A list of file paths matching the specified extensions.
    """    
    input_path = Path(input_dir)
    if recursive:
        files = [str(f) for f in input_path.rglob("*") if f.suffix.lower() in extensions]
    else:
        files = [str(f) for f in input_path.glob("*") if f.suffix.lower() in extensions]
    return files

def rename_chains(structure):
    """Renames chains in the structure to ensure all chain IDs are single characters.
        If a chain ID is already a single character, it is left unchanged. For multi-character
        chain IDs, the first character is used if it is not already taken; otherwise, a new
        unique single-character ID is assigned.
        Input:
            - structure: A Biopython Structure object containing the chains to be renamed.
        Output:
            - A dictionary mapping original chain IDs to their new single-character IDs.
    """
    chainmap = {c.id: c.id for c in structure.get_chains() if len(c.id) == 1}
    next_chain = 0
    for chain in structure.get_chains():
        if len(chain.id) != 1:
            if chain.id[0] not in chainmap:
                chainmap[chain.id[0]] = chain.id
                chain.id = chain.id[0]
            else:
                while True:
                    c = chr(ord('A') + (next_chain % 26)) if next_chain < 26 else \
                        str(next_chain - 26) if next_chain < 36 else \
                        chr(ord('a') + next_chain - 36)
                    next_chain += 1
                    if c not in chainmap:
                        chainmap[c] = chain.id
                        chain.id = c
                        break
    return chainmap

def three_to_one_letter_code(resname):
    code3to1 = {
        'ALA':'A', 'CYS':'C', 'ASP':'D', 'GLU':'E', 'PHE':'F', 'GLY':'G',
        'HIS':'H', 'ILE':'I', 'LYS':'K', 'LEU':'L', 'MET':'M', 'ASN':'N',
        'PRO':'P', 'GLN':'Q', 'ARG':'R', 'SER':'S', 'THR':'T', 'VAL':'V',
        'TRP':'W', 'TYR':'Y'
    }
    return code3to1.get(resname, 'X')

class ProteinOnly(Select):
    """Only accept protein residues (skip ligands)"""
    def accept_residue(self, residue):
        return residue.get_id()[0] == ' '  # Standard AA only

def get_chain_sequence(structure):
    """Extract sequences from ALL chains safely"""
    records = []
    for model in structure:
        for chain_id, chain in model.child_dict.items():
            seq_list = []
            for residue in chain:
                if ProteinOnly().accept_residue(residue):
                    resname = residue.get_resname()
                    seq_list.append(three_to_one_letter_code(resname))
            seq = ''.join(seq_list)
            if len(seq) > 0:
                records.append(SeqRecord(Seq(seq), id=f"{structure.id}:{chain_id}", 
                                       description=""))
    return records

# ======================================================
# 1. Convert CIF files to PDB format
# ======================================================
def convert_cif_to_pdb(cif_file: str, output_folder: str):
    """
    Converts a single CIF file to PDB format and saves it in the specified output folder.
    The function handles chain renaming to ensure all chain IDs are single characters.
    Inputs:
        - cif_file: Path to the input CIF file.
        - output_folder: Path to the output folder where the PDB file will be saved.
    Output (no return value):
        - Saves the converted PDB file in the output folder with the same base name as the CIF file.
    """
    try:
        strucid = os.path.basename(cif_file)[:4]
        parser = MMCIFParser()
        structure = parser.get_structure(strucid, cif_file)
        rename_chains(structure)
        
        # New saving logic: create subfolder and compute output path
        cif_dir = Path(cif_file).parent
        output_dir = cif_dir / output_folder
        output_dir.mkdir(exist_ok=True)  # Creates if missing
        pdb_filename = Path(cif_file).stem + ".pdb"
        pdbfile = output_dir / pdb_filename
        
        io = PDBIO()
        io.set_structure(structure)
        io.save(str(pdbfile))  # Use str() for Path compatibility
        print(f"Success: {cif_file} -> {pdbfile}")
    except Exception as e:
        print(f"Error with {cif_file}: {e}")

def batch_convert_cif_to_pdb(input_dir: str, output_folder: str, recursive: bool = True):
    """
    Batch converts all CIF files in the specified input directory (and optionally subdirectories) to PDB format.
    Each converted PDB file is saved in the specified output folder with the same base name as the original CIF file.
    Inputs:
        - input_dir: Path to the directory containing CIF files to be converted.
        - output_folder: Path to the output folder where converted PDB files will be saved.
        - recursive: Whether to search for CIF files in subdirectories (default: True).
    Output (no return value):
        - Saves all converted PDB files in the output folder.
    """
    cif_files = find_structure_files(input_dir, extensions=[".cif"], recursive=recursive)
    for cif_file in cif_files:
        convert_cif_to_pdb(cif_file, output_folder)

# ======================================================
# 2. Convert PDB files to CIF format
# ======================================================
def convert_pdb_to_cif(pdb_file: str, output_folder: str):
    """
    Converts a single PDB file to CIF format and saves it in the specified output folder.
    Inputs:
        - pdb_file: Path to the input PDB file.
        - output_folder: Path to the output folder where the CIF file will be saved.
    Output (no return value):
        - Saves the converted CIF file in the output folder with the same base name as the PDB file.
    """
    try:
        cif_dir = Path(pdb_file).parent
        output_dir = cif_dir / output_folder
        output_dir.mkdir(exist_ok=True)  # Creates if missing
        cif_filename = Path(pdb_file).stem + ".cif"
        ciffile = output_dir / cif_filename
        
        structure = pdb.PDBFile.read(pdb_file).get_structure()
        cif_file = pdbx.CIFFile()
        pdbx.set_structure(cif_file, structure)
        cif_file.write(ciffile)
        
        print(f"Success: {pdb_file} -> {ciffile}")
    except Exception as e:
        print(f"Error with {pdb_file}: {e}")

def batch_convert_pdb_to_cif(input_dir: str, output_folder: str, recursive: bool = True):
    """
    Batch converts all PDB files in the specified input directory (and optionally subdirectories) to CIF format.
    Each converted CIF file is saved in the specified output folder with the same base name as the original PDB file.
    Inputs:
        - input_dir: Path to the directory containing PDB files to be converted.
        - output_folder: Path to the output folder where converted CIF files will be saved.
        - recursive: Whether to search for PDB files in subdirectories (default: True).
    Output (no return value):
        - Saves all converted CIF files in the output folder.
    """
    pdb_files = find_structure_files(input_dir, extensions=[".pdb"], recursive=recursive)
    for pdb_file in pdb_files:
        convert_pdb_to_cif(pdb_file, output_folder)

# ======================================================
# 3. Convert PDB files to FASTA format - useful for AF3
# ======================================================
# Suppress warnings
warnings.simplefilter('ignore', PDBConstructionWarning)
warnings.filterwarnings('ignore', category=UserWarning)

def batch_structures_to_fasta(input_dir: str | Path, output_dir: str | Path, merged_output: bool = False, recursive: bool = True):
    """
    Batch converts structure files (PDB/CIF) in the specified input directory to FASTA format.
    Each chain in the structure files is extracted as a separate FASTA record. The output can be either individual FASTA files for each structure or a single merged FASTA file containing all chains.
    Inputs:
        - input_dir: Path to the directory containing structure files (PDB/CIF) to be converted.
        - output_dir: Path to the directory where the FASTA files will be saved.
        - merged_output: If True, all chains will be saved in a single FASTA file named "all_sequences.fasta". If False, each structure will be saved as a separate FASTA file (default: False).
        - recursive: Whether to search for structure files in subdirectories (default: True).
    Output (no return value):
        - Saves the extracted sequences in FASTA format in the specified output directory, either as individual files or a single merged file depending on the merged_output flag.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if merged_output:
        merged_path = output_dir / "all_sequences.fasta"
        merged_path.unlink(missing_ok=True)

    total_chains = 0
    structure_files = find_structure_files(input_dir, extensions=[".pdb", ".cif"], recursive=recursive)
    
    for path in structure_files:
        if isinstance(path, str):
            path = Path(path)
        
        records = []
        
        # Try multiple parsers in order of reliability
        parsers = ["pdb-atom"]  # Most robust for both formats
        
        if path.suffix.lower() == '.pdb':
            parsers.insert(0, "pdb-seqres")  # PDBs might have full sequences
            
        for fmt in parsers:
            try:
                records = list(SeqIO.parse(path, fmt))
                if records:
                    print(f"Processed {path.name} ({fmt}): {len(records)} chains")
                    break
            except Exception:
                continue
        
        if not records:
            print(f"Skipped {path.name}: no valid records")
            continue

        # Clean IDs
        for rec in records:
            rec.description = ""
            if '????' in rec.id:
                rec.id = f"{path.stem}:{rec.id.split(':')[-1] if ':' in rec.id else rec.id}"

        total_chains += len(records)
        if merged_output:
            for rec in records:
                rec.id = f"{path.stem}|{rec.id}"
            with open(merged_path, "a") as handle:
                SeqIO.write(records, handle, "fasta")
        else:
            out_path = output_dir / f"{path.stem}.fasta"
            SeqIO.write(records, out_path, "fasta")

    print(f"Total: {total_chains} chains processed")