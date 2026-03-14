# Protein Design Week - Official Repo 2026

Through a collaboration between the EPFL student association [SV industry](https://www.linkedin.com/company/sv-industry/posts/?feedView=all) and MAKE project [Designing Life with AI (DLAI)](https://designinglifewithai.ch/), this first edition of Protein Design Week @ EPFL helps students discover the world of computational protein design through lab visits, conferences and a 2-day hackathon!

<img width="6912" height="3456" alt="Ai-Panel-PDW-banner-landscape" src="https://github.com/user-attachments/assets/9a982a99-5fd8-41f2-a4f9-47260e427436" />

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

You'll also find [Monday's workshop slides](protein-design-basics.pdf) and a tutorial to [using Pymol](survival-guides/PDW-Pymol-tutorial-2026.pdf). Speaking of Pymol, check out the [VScode Protein Viewer](https://marketplace.visualstudio.com/items?itemName=ArianJamasb.protein-viewer) extension for design visualization in your IDE!

Hopefully these docs will help you navigate the world of protein engineering a bit better!

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

  - **[BoltzGen](https://huggingface.co/spaces/hugging-science/BoltzGen)**: Generative model that designs both sequence and structure of protein/peptide binders together. It uses diffusion on structures with rich specifications (e.g., secondary structure, binding sites). Substitutes the entire RFD3+LigandMPNN+RF3/AF3 pipeline with a single model but needs long runtimes for complex designs.<u> **Because of BoltzGen's long runtimes, we do not recommend using this space as your sole design strategy for the hackathon.**</u> We still provide the Space for pedagogical purposes but it was not as tested as the other Spaces and less support will be provided for it during the hackathon. 
    -     Input: Target specs, binding mode info (SMILES/CCD).
          Output: Binder structures/sequences.

To make it easier to pipeline different Spaces and to avoid losing your jobs by accidentally closing the tab, you can also interact with the Spaces through their APIs! More details are provided in the [example notebook](hf-api/example_hf_api.ipynb)

### b) EPFL's Research Computing Platform (RCP) 🖥️ 

While HF Spaces are great for rapid prototyping and easy access, they have limitations in terms of computational resources and runtime, especially for more complex design tasks. This is where our second computing sponsorship comes in with the incredible [EPFL Research Computing Platform (RCP)](https://www.epfl.ch/research/facilities/rcp/), which provides access to high-performance computing clusters with powerful GPUs (A100, V100) and CPUs. We'll provide [Docker images](https://www.docker.com/) to provide an easy setup of the protein design models on the cluster. RCP uses [RunAI](https://www.run.ai/) as its job scheduling platform — you submit containerized jobs via the `runai` CLI, and the platform handles GPU allocation and scheduling for you.

Our [Getting Started with RCP](RCP/GUIDE.md) guide walks you through the full setup, covering:
1. **Local environment setup** — installing Docker, `kubectl`, and the RunAI CLI
2. **Cluster access** — configuring `kubeconfig` and authenticating via EPFL SSO
3. **Data management** — using the jumphost and `rsync` to transfer files to/from your team's scratch storage
4. **Running interactive jobs** — launching GPU-powered containers with pre-built images for each tool (RFD3, LigandMPNN, AF3, Boltz, Chai, CARBonAra) and mounting persistent storage for your inputs/outputs
5. **Developing in-container with VSCode** — attaching to running pods for live debugging

An overview will be presented during the Saturday morning session! The RCP folder also contains:
- **[EXAMPLE.md](RCP/EXAMPLE.md)** — A full end-to-end pipeline walkthrough: scaffold generation (RFD3) → sequence design (LigandMPNN / CARBonAra) → structure prediction (AF3 / Chai / Boltz) → local parsing & ranking, with copy-paste commands for every step.
- **[analysis.ipynb](RCP/analysis.ipynb)** — A Jupyter notebook for parsing, ranking, and visualizing pipeline outputs. Ships with sample data so you can explore results immediately.

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


## 4. Further learning resources

Do you want to learn more about computational protein design after the hackathon? Here's a list of resources to keep you busy:

- [**RosettaCommons Youtube Channel**](https://www.youtube.com/@RosettaCommons): Lectures, tutorials, model deep dives and workflow explanations from Rosetta Commons, a community of researchers created by Nobel laureate David Baker whose goal is to advance open-source protein structure prediction and design. 
- [**DL4Proteins**](https://github.com/Graylab/DL4Proteins-notebooks): Collection of Jupyter notebooks from the Gray Lab at Johns Hopkins University (who have proposed one of the hackathon projects!). This series is perfect for people who want to dive further into the architecture of these models rather than just their use cases. What is a transformer and why is it suitable for sequence representation? How do diffusion networks create diverse structures? All questions you'll find answers to in this amazing resource.
- [**Proteinbase**](http://proteinbase.com/): Platform that hosts the results of [Adaptyv Bio's](https://www.adaptyvbio.com/) famed protein design challenges (another one of our project sponsors!). Use this to explore how different design strategies have worked out in real use-cases.
- [**Pyrosetta notebooks**](https://rosettacommons.github.io/PyRosetta.notebooks/): Before deep learning entered the game, physics-based modeling was the go-to approach to explore the conformational space of proteins. PyRosetta remains crucial for protein visualization, structure refinement and energetic analysis and is integrated in many hybrid AI-physics pipelines.  

These are some of many resources. For a more extensive list, Adrian Jasinski's at Ardigen has compiled [this list.](https://docs.google.com/document/d/1gGcNGDDszT2zWFNT5icj5L4o3OsonTTs1KifXpztUdM/edit?tab=t.0) Are you bored of scrolling through resources and want to jump straight into the action? Then you might just consider joining the MAKE project [Designing Life with AI (DLAI) @ EPFL](https://designinglifewithai.ch/) ;)

Good luck, and may the best design win!


Made with love, by Alexia, Ghassan, Emma, Cris, Benedikt and Asia, with the help of our amazing coaches and partners!


