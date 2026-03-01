# Protein Design Week - Official Repo 2026

Through a collaboration between the EPFL student association [SV industry](https://www.linkedin.com/company/sv-industry/posts/?feedView=all) and MAKE project [Designing Life with AI (DLAI)](https://designinglifewithai.ch/), this first edition of Protein Design Week @ EPFL helps students discover the world of computational protein design through lab visits, conferences and a 2-day hackathon!

<img width="1233" height="692" alt="image" src="https://github.com/user-attachments/assets/0b0c2b6e-bb17-4420-84d6-40a686cbe71a" />

## Intro

Welcome Hackers! This repo is your go-to guide throughout the week-end Hackathon. It gathers code snippets, tutorials and survival guides to get you started! It also provides a centralized reference for protein design tools you learned about during the workshop so that you can use them with confidence throughout the weekend to generate awesome new proteins! More specifically, it containes specific guides for more complicated tools like RFD3, as well as your go-to functions for PDB pre-processing and predictions analyses (like MSA or RMSD).

If you have any specific questions about tools or or need help debugging, coaches are around! But, before bothering us... remember the learner drill:

    1.   Google it, 
    2.   Ask your favourite AI agent,
    3.   Ask the Coaches

So get grinding, and don't forget to have fun!

## 1. The (clueless) protein engineer's survival guides

The awesome thing about you guys is that you all come from different academic backgrounds - from ML to computer science, to pure wet-lab biology, and who knows what else. For this specific reason, - besides being a protein nerd otherwise you wouldn't be here - you might find the topic of protein design a little bit complicated. 

But fear not you brave bio-soldier! We made some basics survival guides for you to rely on when things seem not to make any sense. In the repo folder `./survival-guides`, you can find two documents: 

- One survival guide [for pure wet-lab biologists](survival-guides/ML-survival-guide-for-biologists.pdf) approaching 🧬💻 computational protein design
- One survival guide [for ML and computer people](survival-guides/coder-survival-guide-to-biology.pdf) starting to get into the world of ✨biology✨ 

(sorry for the emojis, i'm a fan tho)

So, hopefully these docs will help you navigate the world of protein engineering a bit better!

## 2. Fantastic tools and where to find them

### a) HuggingFace Spaces 🤗


Through our incredible partnership with [Hugging Face](https://huggingface.co/) for this event, we've deployed some pretty neat HF Spaces for you to easily interact with your favorite protein design tools! HF Spaces is simply a hosting platform that allows users to easily share machine learning applications through interactive demos on the web. It provides different tiers of computing infrastructure, from CPU-only options to H200 GPUs! To use these tools, you'll simply need to create an account on Hugging Face and join the [hugging-science organization](https://huggingface.co/hugging-science). Specifically, HF Spaces will be the principal design tool for our non-EPFL participants, but feel free to use it if you are an EPFL student as well!


The advantage of HF Spaces is that they abstract away the need for setting up job configuration files through their extensive and intuitive interfaces. However, we choose to keep the input and output formats of the models as close as possible to the models' command-line interface so that you can learn how to set up protein design jobs independent of the computing infrastructure (or because we were lazy, who knows). That means you'll need to create your YAML/JSON job files, analyze the outputs in Python, etc.


Here is a list of the available models on HF (with a refresher of what they do):


  - **[RFD3 (RFdiffusion3)](https://huggingface.co/spaces/hugging-science/RFdiffusion3)**: All-atom generative diffusion model for designing protein binders, enzymes, symmetric assemblies, and structures with small molecules/metals.
    -     Input: Protein structures (PDB), JSON or YAML file with contig specifications for constraints (e.g., fixed regions, hotspots).
          Output: Novel protein backbones (PDB).
​

  - **[LigandMPNN](https://huggingface.co/spaces/hugging-science/LigandMPNN)**: Deep learning sequence design takes into account non-protein components like small ligands and nucleic acids in biomolecular complexes. Use it for re-designing your sequences after _de novo_ backbone generation.
    -     Input: Protein Backbone-ligand structures (PDB with atoms).
          Output: Optimized amino acid sequences (FASTA).

  - **[RosettaFold3](https://huggingface.co/spaces/hugging-science/RosettaFold3)**:  All-atom structure prediction, including complexes with ligands, nucleic acids, and metals. Use it for validating your designs or for structure prediction of your target.
    -     Input: Protein sequences (FASTA) or partial structures (PDB).
          Output: Predicted 3D structures (PDB).

  - **[ESM-2](https://huggingface.co/spaces/hugging-science/ESM2)**: Sequence-only protein language model that create information-rich embeddings of sequences. Use its embeddings for downstream prediction tasks, to compare to existing proteins, or calculate Pseudo-Perplexity scores to filter designed sequences.
    -     Input: Protein sequences (FASTA).
          Output: Embeddings (numpy arrays) and Pseudo-Perplexity scores. use np.load(...) to access embeddings.

  - **[BoltzGen](https://huggingface.co/spaces/hugging-science/BoltzGen_Demo)**: Generative model that designs both sequence and structure of protein/peptide binders together. It uses diffusion on structures with rich specifications (e.g., secondary structure, binding sites). Substitutes the entire RFD3+LigandMPNN+RF3/AF3 pipeline with a single model but needs long runtimes for complex designs.
    -     Input: Target specs, binding mode info (SMILES/CCD).
          Output: Binder structures/sequences.


### b) EPFL's Research Computing Platform (RCP) 🖥️ 

While HF Spaces are great for rapid prototyping and easy access, they have limitations in terms of computational resources and runtime, especially for more complex design tasks. This is where our second computing sponsorship comes in with the incredible [EPFL Research Computing Platform (RCP)](https://www.epfl.ch/research/facilities/rcp/), which provides access to high-performance computing clusters with powerful GPUs and CPUs. We'll use [Docker](https://www.docker.com/) to provide an easy setup of the protein design models on the cluster. More details on how to access and use RCP will be provided during the Saturday morning session!

### c) External Tools 🌴


The world of computational protein design is rapidly growing and democratizing, so there are many tools available online that you can use for your design projects! Here is a list of other tools that are available directly online (either on CoLab folders or servers, or both). Note that the typical limitations of such tools are the hardware available (e.g only T4 on Colab without purchasing credits) and rate limits imposed by servers (e.g. 30 jobs/day on AF3).

  - [**AF3 (AlphaFold3)**](https://alphafoldserver.com): State-of-the-art structure prediction for protein-ligand/DNA/RNA, excels in static interactions but limited on big conformational changes.
    -     Input: Sequences/SMILES.
          Output: Complexes (PDB).

  - [**PeSTo**](https://pesto.epfl.ch): Transformer for protein interface prediction (with DNA/lipids/ligands/ions), handles MD ensembles. Docker/web available.
    -     Input: PDB/UniProt.
          Output: Interface PDBs.

  - [**ESMFold on Colab**](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/ESMFold.ipynb?scrollTo=boFQEwsNQ4Qt): Structure prediction from sequence using ESM-2 embeddings without MSA, faster than AF2 but less accurate. [Advanced notebook](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/beta/ESMFold_advanced.ipynb) also available.
    -     Input: Protein Sequences (FASTA).
          Output: Predicted 3D structures (PDB).

  - [**ESM3**](https://forge.evolutionaryscale.ai/): Multimodal model that extends ESM-2 to include structure via geometric transformers. Can be used for fitness prediction, folding or even generation!
    -     Input: Partial sequence/structure/function prompts for generation tasks
          Output: sequence + structure for generation tasks.

  - [**BioEmu on CoLab**](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/BioEmu.ipynb): Generates structural ensembles to capture protein dynamics/flexibility for function prediction. [Jupyter notebook](https://github.com/sokrypton/ColabFold/blob/main/BioEmu.ipynb) also available.
    -     Input: Protein sequences/structures.
          Output: Diverse conformations (thousands), free energies (~1 kcal/mol accuracy).

  - [**BindCraft on CoLab**](https://colab.research.google.com/github/martinpacesa/BindCraft/blob/main/notebooks/BindCraft.ipynb): Automated all-in-one pipeline for de novo miniprotein binders via AF2 hallucination, MPNN optimization, and scoring.
    -     Input: Target protein structure (PDB). 
          Output: Binder backbones/sequences (65-150 AA, PDB/FASTA).

  - [**BoltzDesign1 on CoLab**](https://colab.research.google.com/github/yehlincho/BoltzDesign1/blob/main/Boltzdesign1.ipynb?scrollTo=lP-SR0lM3jr4): Inverted model of Boltz-1 (open source reproduction of AlphaFold3), enables design of protein binders for diverse molecular targets without model finetuning. You can change model parameters in the CoLab folder.
    -     Input: YAML file (generated via interface in CoLab). 
          Output: Predicted CIF/PDB file or FASTA format (to pass through AF3 afterwards).


If - as a good veteran of protein design - you know other tools to use for the hackathon, feel free to do so, also open a PR to add to this list! We look forward to see your designs on Sunday. 


## 2. Useful Protein Designer ToolKit

In the tool-kit folder on the repo you can find a notebook with useful functions and pipelines for (1) preparing your input files that you will feed your favourite design model, and (2) analysing how good your predictions are after your runs. Here you'll find pieplines for things like RMSD, structural analysis, PDB parsing and handling, and more. Have fun! 




Good luck, and may the best design win!


Made with love, by Alexia, Ghassan, Emma, Cris and Asia, with the help of our amazing coaches and partners!


