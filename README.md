# Protein Design Week - Official Repo 2026
Official Repository of the first edition of Protein Design Week @ EPFL, March 2026. This repository contains code snippets, tutorials and survival guides to get you started!

<img width="1233" height="692" alt="image" src="https://github.com/user-attachments/assets/0b0c2b6e-bb17-4420-84d6-40a686cbe71a" />

## Intro

Welcome Hackers! This repo is your go-to guide throughout the week-end Hackathon. It gathers a collection of protein design tools that you learned about during the workshop, and that you can use with confidence throughout the weekend to generate awesome predictions! The repo also contains some specific helpers on more complicated tools like RFD3, as well as your go-to functions for pdb pre-processing and predictions analyses (like MSA or RMSD).

If you have any specific questions about tools or de-bug, coaches are around! But, before bothering us... remember the learner drill:

    1.   Google it, 
    2.   Ask your favourite AI agent,
    3.   Ask the Coaches

So get grinding, and don't forget to have fun!

## 1. Fantastic tools and where to find them

You will be glad to know that we have created some Docker Containers on Hugging Face for you to interact with the more complex protein design tools! To be able to use these tools, you'll just neet to join hugging-science with your account. See https://huggingface.co/hugging-science .

You can find the following on Hugging Face (with a refresher of what they do):


  - RFD3 (RFdiffusion3): All-atom generative diffusion model for designing protein binders, enzymes, symmetric assemblies, and structures with small molecules/metals. Available at: https://huggingface.co/spaces/hugging-science/RFdiffusion3
  -     Input: Protein structures (PDB), JSON or YAML file with contig specifications for constraints (e.g., fixed regions, hotspots).
  -     Output: Novel protein backbones (PDB).
​

  - LigandMPNN: Deep learning sequence design that models non-protein components like ligands in biomolecular systems. Use it for re-designing your sequences after _de novo_ prediction. Available at : https://huggingface.co/spaces/hugging-science/LigandMPNN
  -     Input: Protein-ligand structures (PDB with atoms).
  -     Output: Optimized amino acid sequences (FASTA).
​

  - BoltzGen: Generative model for inverse design of protein/peptide binders to targets, using diffusion on structures with rich specifications (e.g., secondary structure, binding       sites). Available at : https://huggingface.co/spaces/hugging-science/BoltzGen_Demo
  -     Input: Target specs, binding mode info (SMILES/CCD).
  -     Output: Binder structures/sequences.

Other tools that are available directly online (either on CoLab folders or servers, or both) are:

  - **AF3** (AlphaFold3):  Structure prediction for protein-ligand/DNA/RNA, excels in static interactions but limited on big conform changes.  Server available at : https://alphafoldserver.com
  -     Input: Sequences/SMILES.
  -     Output: Complexes (PDB).​

  - **PeSTo**: Transformer for protein interface prediction (with DNA/lipids/ligands/ions), handles MD ensembles. Docker/web at : pesto.epfl.ch.
  -     Input: PDB/UniProt.
  -     Output: Interface PDBs.

  - **ESM2**: sequence-only protein language model used mainly for embeddings, fitness prediction, mutational scans, zero-shot structure prediction via ESMFold. Docker available on Hugging Face at https://huggingface.co/spaces/hugging-science/ESM2.
  **Zero-Shot Variant Design**
  -     Input: FASTA file with your WT scaffold sequence
  -     Method: Iteratively mask each position → ESM-2 predicts top substitutions     →rank by log-probability→rank by log-probability
  -     Output: Variant library (FASTA), probability heatmaps
  -     Use case: Stability optimization, natural-like redesign

  - **ESM3**: Multimodal model for sequence/structure/function design via bidirectional transformers. Classic ESMFold CoLab folder available at : https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/ESMFold.ipynbscrollTo=boFQEwsNQ4Qt . For the veterans, more advanced jupiter notebook CoLab available at : https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/beta/ESMFold_advanced.ipynb
  -     Input: Partial sequence/structure/function prompts.
  -     Output: Proteins matching your input specs   (e.g., pTM >0.8)

  - **BioEmu**: Generates structural ensembles to capture protein dynamics/flexibility for function prediction. CoLab folder at : https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/BioEmu.ipynb . BioEmu jupyter notebook available at : https://github.com/sokrypton/ColabFold/blob/main/BioEmu.ipynb
  -     Input: Protein sequences/structures.
  -     Output: Diverse conformations (thousands), free energies (~1 kcal/mol accuracy).

  - **BindCraft**: Automated pipeline for de novo miniprotein binders via AF2 hallucination, MPNN optimization, and scoring.  CoLab notebook available at : https://colab.research.google.com/github/martinpacesa/BindCraft/blob/main/notebooks/BindCraft.ipynb
  -         Input: Target protein structure (PDB).
  -         Output: Binder backbones/sequences (65-150 AA, PDB/FASTA).

  - **BoltzDesign1**: Inverted model of Boltz - 1  (open source reproduction of AlphaFold3), to enable the design of protein binders for diverse molecular targets without requiring model finetuning. This one is pretty cool cause you can actually change the models' parameters on the CoLab folder (for the more daring hackers ihih). Available on CoLab at : https://colab.research.google.com/github/yehlincho/BoltzDesign1/blob/main/Boltzdesign1.ipynb#scrollTo=lP-SR0lM3jr4
  -         Input: Normally a YAML file, but on CoLab folder you generate the YAML with an interface.
  -         Output: YOur predicted CIF/PDB file or in FASTA format (to pass through AF3 afterwards)

If - as a good veteran of protein design - you know other tools to use for the hackathon, feel free to do so! We look forward to see your designs on Sunday. 


## 2. Useful Protein Designer ToolKit

In the tool-kit folder on the repo you can find a notebook with useful functions and pipelines for (1) preparing your input files that you will feed your favourite design model, and (2) analysing how good your predictions are after your runs. Here you'll find pieplines for things like RMSD, structural analysis, PDB parsing and handling, and more. Have fun! 




Good luck, and may the best design win!


Made, with love, by Alexia, Ghassan, and Emma


