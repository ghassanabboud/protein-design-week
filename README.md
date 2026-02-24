# Protein Design Week - Official Repo 2026
Official Repository of the first edition of Protein Design Week @ EPFL, March 2026. This repository contains code snippets, tutorials and survival guides to get you started!

## Intro

Welcome Hackers! This repo is your go-to guide throughout the week-end Hackathon. It gathers a collection of protein design tools that you learned about during the workshop, and that you can use with confidence throughout the weekend to generate awesome predictions! The repo also contains some specific helpers on more complicated tools like RFD3, as well as your go-to functions for pdb pre-processing and predictions analyses (like MSA or RMSD).

If you have any specific questions about tools or de-bug, coaches are around! But, before bothering us... remember the learner drill:

    1.   Google it, 
    2.   Ask your favourite AI agent,
    3.   Ask the Coaches

So get grinding, and don't forget to have fun!

## 1. Fantastic tools and where to find them

You will be glad to know that we have created some Doker Containers on Hugging Face for you to interact with the more complex protein design tools! To be able to use these tools, you'll just neet to join hugging-science with your account. See https://huggingface.co/hugging-science .

You can find the following on Hugging Face (with a refresher of what they do):


  - RFD3 (RFdiffusion3): All-atom generative diffusion model for designing protein binders, enzymes, symmetric assemblies, and structures with small molecules/metals. Available at: https://huggingface.co/spaces/hugging-science/RFdiffusion3
  -     Input: Protein structures (PDB), contig specifications for constraints (e.g., fixed regions, hotspots).
  -     Output: Novel protein backbones (PDB).
​

  - ####LigandMPNN:#### Deep learning sequence design that models non-protein components like ligands in biomolecular systems. Available at : https://huggingface.co/spaces/hugging-science/LigandMPNN
  -     Input: Protein-ligand structures (PDB with atoms).
  -     Output: Optimized amino acid sequences (FASTA).
​

  - ####BoltzGen:#### Generative model for inverse design of protein/peptide binders to targets, using diffusion on structures with rich specifications (e.g., secondary structure, binding       sites). ####Available at#### : https://huggingface.co/spaces/hugging-science/BoltzGen_Demo
  -     Input: Target specs, binding mode info (SMILES/CCD).
  -     Output: Binder structures/sequences.

Other tools that are available directly online (either on CoLab folders or servers, or both) are:

  - ####AF3 (AlphaFold3): #### Structure prediction for protein-ligand/DNA/RNA, excels in static interactions but limited on big conform changes. #### Server available at ####: https://alphafoldserver.com
  -     Input: Sequences/SMILES.
  -     Output: Complexes (PDB).​

  - ####PeSTo:#### Transformer for protein interface prediction (with DNA/lipids/ligands/ions), handles MD ensembles. ####Docker/web at#### : pesto.epfl.ch.
  -     Input: PDB/UniProt.
  -     Output: Interface PDBs.

  - ####ESM3:#### Multimodal model for sequence/structure/function design via bidirectional transformers. ####Classic ESMFold CoLab folder available at#### : https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/ESMFold.ipynb#scrollTo=boFQEwsNQ4Qt . ####For the veterans, more advanced jupiter notebook CoLab available at#### : https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/beta/ESMFold_advanced.ipynb
  -     Input: Partial sequence/structure/function prompts.
  -     Output: Proteins matching your input specs   (e.g., pTM >0.8)

  - ####BioEmu:#### Generates structural ensembles to capture protein dynamics/flexibility for function prediction. ####CoLab folder at#### : https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/BioEmu.ipynb . ####BioEmu jupyter notebook#### available at : https://github.com/sokrypton/ColabFold/blob/main/BioEmu.ipynb
  -     Input: Protein sequences/structures.
  -     Output: Diverse conformations (thousands), free energies (~1 kcal/mol accuracy).


