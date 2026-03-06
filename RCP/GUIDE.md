# Getting Started with RunAI on EPFL's RCP — From Zero to Running Jobs


This guide walks you through everything you need to do to successfully run protein design workloads on EPFL's RCP cluster using Runai! We'll cover:
1. Setting up your local environment 
2. Configuring access to the RCP cluster
3. Managing your data
4. Running interactive jobs
5. Managing jobs
6. Developing Code in container with VScode
7. Important notes and troubleshooting tips

<u>**Note**</u>: A lot of online resources in this guide, e.g RCP's wiki, are only accessible if you're connected to the EPFL network (either on campus or via VPN). You also need to be connected to the network to authenticate with RunAI and access the RCP cluster.

<u>**Note on fair distribution of resources**</u>: A limit of 1 A100 GPU per user is directly enforced on RCP. As we are allocated 24 A100 GPUs for the hackathon, this means 2 A100s can be used simultaneously by each team. Please respect this limit by coordinating with your teammates to respect fair distribution. We can track teams' GPU usage.

## Legal Disclaimer

> **By using the container images provided in this repository, you acknowledge and agree to the license terms of each individual software package.** Each tool has its own license — please review them before use. The license files are included in each tool's folder in this repository and are summarized below:
>
> | Tool | License | Commercial Use |
> |------|---------|---------------|
> | [AlphaFold 3](https://github.com/google-deepmind/alphafold3) | CC-BY-NC-SA 4.0 | Non-commercial only |
> | [Boltz](https://github.com/jwohlwend/boltz) | MIT | Yes |
> | [CARBonAra](https://github.com/LBM-EPFL/CARBonAra) | CC-BY-NC-SA 4.0 | Non-commercial only |
> | [Chai-1](https://github.com/chaidiscovery/chai-lab) | Apache 2.0 | Yes |
> | [LigandMPNN](https://github.com/dauparas/LigandMPNN) | MIT | Yes |
> | [RFdiffusion3](https://github.com/RosettaCommons/foundry) | BSD 3-Clause | Yes |
>
> **You are solely responsible for ensuring your use complies with these licenses.**

---

## Prerequisites

- An EPFL Gaspar account
- membership to the a runai department. In your case, you are assigned to a group (e.g., `hackathon-proteindesign-g11`). This automatically makes you a member of the `rcp-runai-hackathon-proteindesign` department. You can verify both memberships on the [EPFL groups application](http://groups.epfl.ch/).

- A local machine with Docker installed ([Docker install guide](https://wiki.rcp.epfl.ch/home/CaaS/FAQ/how-to-prepare-environment))


## Step 1: Setting up your local environment

We had asked you to set up your local environment during Monday's workshop following [RCP's how-to-prepare-environment tutorial](https://wiki.rcp.epfl.ch/home/CaaS/FAQ/how-to-prepare-environment). Here is a recap:

### 1.1 Install Docker

`Linux`: Follow the instructions for your specific distribution (e.g., Ubuntu, CentOS) in Docker's official install guide [on Linux](https://docs.docker.com/engine/install/). Specifically, you can follow the `Install using the apt repository` section. Docker

`Mac`: Follow the instructions in Docker's official install guide [on Mac](https://docs.docker.com/desktop/setup/install/mac-install/).On ARM Mac, ensure you can build `linux/amd64`images.

`Windows`: While installation tutorials for Windows are provided on RCP's guide, we did not test our implementations on native Windows. We strongly recommend you to install WSL2 as mentioned in Monday's workshop and then follow the Linux instructions for your specific distribution (default for WSL is Ubuntu). 

### 1.2 Install kubectl 

```bash
# macOS
brew install kubectl

# Linux / WSL
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
chmod +x kubectl
mkdir -p ~/.local/bin
mv ./kubectl ~/.local/bin/kubectl
#chmod +x kubectl && sudo mv kubectl /usr/local/bin/
```

verify your installation with:

```bash
kubectl version
```

### 1.3 Install the RunAI CLI 

```bash
#Linux / WSL
curl -sLo /tmp/runai https://rcp-caas-prod.rcp.epfl.ch/cli/linux
sudo install /tmp/runai /usr/local/bin/runai

#macOS
curl -sLo /tmp/runai https://rcp-caas-prod.rcp.epfl.ch/cli/darwin
sudo install /tmp/runai /usr/local/bin/runai
```
Verify installation:

```bash
runai version
```


---

## Step 2: Configuring Access to the RCP Cluster

You need a kubeconfig file that tells `kubectl` and `runai` how to reach the RCP cluster.

### 2.1 Get the kubeconfig

Run the following commands to set up configuration for kubectl, allowing it to recognize and connect to the RCP cluster:

```bash
curl https://wiki.rcp.epfl.ch/public/files/kube-config.yaml -o ~/.kube/config && chmod 600 ~/.kube/config
```

The above command downloads a configuration file for RCP. You can also create the file manually and copy/paste the content from the [RCP wiki](https://wiki.rcp.epfl.ch/home/CaaS/FAQ/how-to-use-runai). 

### 2.2 Activate the kubeconfig

```bash
export KUBECONFIG=$HOME/.kube/rcp-caas-prod.yaml
```

> **Tip:** Add this line to your `~/.bashrc` or `~/.zshrc` so it persists across sessions. You can do so with:

```bash
# opens your bash configuration file in a text editor
nano ~/.bashrc
```

Then add the line `export KUBECONFIG=$HOME/.kube/rcp-caas-prod.yaml` at the end of the file, save with `CTRL + X` and exit. The next time you open a terminal, the kubeconfig will be automatically set.


### 2.3 Verify cluster access using kubectl

```bash
kubectl config get-contexts
kubectl config use-context rcp-caas-prod
kubectl get ns
```

You should see namespaces listed (no `localhost:8080` errors).

---

### 2.4 Authenticate with RunAI

You need to authenticate with RunAI to submit jobs. `runai login` will provide a link that you will to open in your browser. After clicking `Login with SSO` and authenticating with your EPFL Gaspar credentials, you will be provided a code to paste back into the terminal.
```bash
# Log in via browser SSO (a browser window will open)
runai login

# List your available projects
runai list projects
```

You should see your project (e.g., `hackathon-proteindesign-<your_gaspar_username>`).

### Set your default project

setting your default project allows you to omit the `-p <project>` flag in future commands. It is especially important if you're part of multiple projects (e.g you have access to RCP through another course or lab). In RunAI, your project refers to your personal namespace within a department (in this case `hackathon-proteindesign`).

```bash
runai config project <your-project-name>
# Example:
runai config project hackathon-proteindesign-<your_gaspar_username>
```

---

## Step 3: Managing Your Data
### 3.1 RCP Storage Overview

You will mainly interact with two folders during the hackathon:
- your own team's scratch folder: `/mnt/hackathon-proteindesign/hackathon-proteindesign-gXX/scratch-gXX/` This is your team's personal storage for intermediate files, results, and anything you want to save. You have read-write access here.
- the shared read-only folder: `/mnt/hackathon-proteindesign/hackathon-proteindesign-shared-ro/` This contains shared datasets and model weights that all teams can access. You have read-only access here.

You can check the contents of these folders and transfer data to/from them using the jumphost. First connect to the jumphost using your EPFL credentials (need to be connected to EPFL network):

```bash
#will ask for your gaspar password
ssh <gaspar_username>@jumphost.rcp.epfl.ch
cd /mnt/hackathon-proteindesign/hackathon-proteindesign-gXX/scratch-gXX/
#create a test file to verify you have write access
touch test_file.txt
ls -l
```

### 3.2 Transferring files to/from RCP

```bash
# Upload to your group's scratch
rsync -av --no-group local_files/ \
  <gaspar>@jumphost.rcp.epfl.ch:/mnt/hackathon-proteindesign/hackathon-proteindesign-gXX/scratch-gXX/

# Download from scratch
rsync -av --no-group \
  <gaspar>@jumphost.rcp.epfl.ch:/mnt/hackathon-proteindesign/hackathon-proteindesign-gXX/scratch-gXX/results/ \
  local_results/
```

**<u>Note</u>**: `rsync` serves a similar goal to the more well-know `scp` command for transfers over ssh. However, `rsync` is more efficient because it only transfers the differences between source and destination, ideal for incremental updates.

## Step 4: Running Interactive Jobs

We are now ready to launch our first interactive job on RCP! Interactive jobs are ideal for development and experimentation, they give you a live terminal inside a container running on the cluster, where you can run commands, test code, and iterate quickly. Two essential parts of any runai job are:
- **<u>The Docker image:</u>** a Docker image is a pre-packaged environment that includes the software and dependencies you need to run a certain job. For the hackathon, we have prepared images for each modelto facilitate your design tasks. You ask runai to launch a _container_ (your particular running instance) based on one of these _images_ (the blueprint for what dependencies and software to include).
- **<u>The persistent volumes:</u>** When running an interactive job, you will tell runai to mount both your group's scratch storage and the shared read-only storage into the container. The first one will allow you to save tour work done during the interactive session (remember that the container filesystem is ephemeral!). The second one will give you access to shared datasets and model weights needed to run the models.

### 4.1 Basic interactive job

In the following examples, we ask for an interactive session with 1 GPU, the image is a very basic one with only the Ubuntu OS, and we mount the two persistent volumes. 
```bash
runai submit <job-name> \
  --project hackathon-proteindesign-<gaspar_username> \
  -i ubuntu \
  --interactive \
  --attach \
  --node-pools default \
  -g 1 \
  --existing-pvc claimname=hackathon-proteindesign-scratch-gXX,path=/mnt/scratch \
  --existing-pvc claimname=hackathon-proteindesign-shared-ro,path=/mnt/shared-ro \
  --command -- /bin/bash
```

| Flag | Purpose |
|------|---------|
| `--project` | Your RunAI project (from `runai list projects`) |
| `-i` | Container image from the RCP or Docker registry |
| `--interactive` | Interactive job (non-preemptible, max 12h) |
| `--attach` | Automatically attach to the pod once running |
| `--node-pools default` | Use A100 GPUs (default pool). Omit for V100. |
| `-g 1` | Request 1 GPU |
| `--existing-pvc` | Mount existing storage volumes, `path` specifies the location inside the container |
| `--command -- /bin/bash` | Start an interactive shell |

A terminal inside the container will open after a few moments. While waiting, you can check the status of your job by running the following commands in another terminal:

```bash
#list all your jobs
runai list jobs

#describe the job to see details and status
runai describe job <job-name>
```
Now inside the container, you can run commands and save outputs to your scratch directory, for example:

```bash
#list all your jobs
cd /mnt/scratch
echo "Hello RCP!" > hello_from_container.txt
```
Disconnect from the interactive session by typing `exit`. You can then connect to the jumphost and check that your file was indeed saved!


After disconnecting, don't forget to delete your interactive job to free up cluster resources:

```bash
runai delete job <job-name>
```

### 4.2 RFD3 interactive job

In this example, we build the container using a pre-built image for RFdiffusion3 that we uploaded to the RCP registry. 

```bash
runai submit rfd3-g11 \
  --project hackathon-proteindesign-<gaspar_username> \
  -i registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1 \
  --interactive \
  --attach \
  --node-pools default \
  -g 1 \
  --existing-pvc claimname=hackathon-proteindesign-scratch-g11,path=/mnt/scratch \
  --existing-pvc claimname=hackathon-proteindesign-shared-ro,path=/mnt/shared-ro \
  --command -- /bin/bash
```

Once inside the container, run:

```bash
rfd3 design \
  out_dir=/mnt/scratch/rfd3/out \
  inputs=/mnt/shared-ro/examples/rfd3/demo.json  \
  ckpt_path=/mnt/shared-ro/weights/rfd3/rfd3_latest.ckpt \
  n_batches=1 \
  diffusion_batch_size=8

```

Ignore `atomworks` warnings and check the output folder in your scratch directory when done. If it contains 8 `.cif.gz` files and 8 `.json` files, congrats on your first successful protein deisgn run on RCP!

### 4.3 Common Mistakes

Two very common mistakes to look out for when running interactive jobs:
1. **Not saving your work to scratch**: Any files, outputs or logs stored on the container's filesystem (outside of /mnt/) will be deleted once the job ends. Always save important files to `/mnt/scratch` to ensure they persist after you disconnect. Interactive jobs also have a 12-hour runtime limit, so save your work frequently if you're working the entire day on the same job!
2. **forgetting to delete interactive jobs**: just because you disconnect from an interactive session using `exit` doesn't mean the job is deleted. It will continue running in the background and occupy the requested GPUs until you explicitly delete it. Always remember to run `runai delete job <job-name>` after you're done. As there is a limit of 1 A100 GPU per user, you will not be able to start new interactive jobs if you have an old one still running.


## Step 5: Managing Jobs

These commands help you manage your jobs effeciently. note that the `-p <project>` can be omitted if you set your default project as shown in step 2.4.

#### List all jobs
```bash
runai list jobs -p <project>
```

#### Check job status
```bash
runai describe job <job-name> -p <project>
```

#### Delete a job
```bash
#specific job
runai delete job <job-name> -p <project>

#all jobs in the project (be careful!)
runai delete job --all -p <project>
```

The `--attach` flag in `runai submit` allowed us to automatically get a terminal inside our container. If you forgot to use it, or if you got disconnected, you can still attach to a running job with the following command. It is thus important between deleting a job (resources are freed and ephemeral storage is deleted) and detaching from a job (resources are still occupied but you can reconnect to the same session later).

#### Attach to a running job (if you disconnected)
```bash
runai attach <job-name> -p <project>
```

---

## Step 6: Switching Between Tools

The same template provided in step 4.2 can be used to launch interactive jobs for any of the models we make available on RCP by simply changing the image with the `-i` flag. The same storage is mounted in each case as weights for all models are stored in `claimname=hackathon-proteindesign-shared-ro`.

For completeness, each subfolder in the `RCP` folder contains the model's license and the Dockerfile used to build the image. **Please note that you do not need to build the images yourself or run any docker commands for that matter. The Dockerfiles are only provided for your curiosity.** We have uploaded pre-built images for each model to the RCP registry so that they can specified using the `-i` flag.

### Available Tools

| Tool | Image | Links |
|------|-------|-------|
| AlphaFold 3 | `registry.rcp.epfl.ch/proteindesign-containers/af3:2026.1` | [GitHub](https://github.com/google-deepmind/alphafold3), [paper](https://doi.org/10.1038/s41586-024-07487-w)
| Boltz | `registry.rcp.epfl.ch/proteindesign-containers/boltz:2026.1` | [GitHub](https://github.com/jwohlwend/boltz), [prediction docs](https://github.com/jwohlwend/boltz/blob/main/docs/prediction.md)
| CARBonAra | `registry.rcp.epfl.ch/proteindesign-containers/carbonara:2026.1` | [GitHub](https://github.com/LBM-EPFL/CARBonAra), [paper](https://www.nature.com/articles/s41467-024-50571-y)
| Chai-1 | `registry.rcp.epfl.ch/proteindesign-containers/chai:2026.1` | [GitHub](https://github.com/chaidiscovery/chai-lab), [paper](https://www.biorxiv.org/content/10.1101/2024.10.10.615955v1)
| LigandMPNN | `registry.rcp.epfl.ch/proteindesign-containers/ligandmpnn:2026.1` | [GitHub](https://github.com/dauparas/LigandMPNN), [paper](https://doi.org/10.1101/2023.12.22.573103)
| RFdiffusion3 | `registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1` | [GitHub](https://github.com/RosettaCommons/foundry), [docs](https://subseq.bio/docs/rfdiffusion3), [Docker Hub](https://hub.docker.com/r/rosettacommons/foundry), [paper](https://www.biorxiv.org/content/10.1101/2025.09.18.676967v1)

To switch tools, just change the `-i` image — all your data on `/mnt/scratch` stays the same.

## Step 6: Developing Code in container with VScode

Using interactive pods, you can also develop code and debug directly on RCP. This tutorial shows use how to use the [Kubernetes extension in VScode to do so](https://wiki.rcp.epfl.ch/home/CaaS/FAQ/how-to-vscode). We have found that on top of the kubernetes extension mentioned in the tutorial, one should also install the "Remote - Containers" extension in VScode for it to work.

Note that this seems to be much harder to set up on WSL. A known fix is to install Kubernetes and runai on the Windows host machine (you'll have one installation on Windows and one on WSL) and then connect to pods from the Windows VScode.

## 7. Important Notes and troubleshooting tips

- **Interactive jobs have a 12-hour maximum runtime.** Save your work frequently.
- **Interactive jobs are non-preemptible** — they won't be interrupted (except for hardware failures).
- **GPU limits**: 1x A100 or 1x V100 per interactive job.
- **The "I have no name" prompt** is cosmetic — it appears when your UID has no matching `/etc/passwd` entry in the container. Everything still works correctly.
- **Containers are ephemeral** — only data on `/mnt/scratch` and `/mnt/shared-ro` persists.


### Troubleshooting

| Problem | Solution |
|---------|----------|
| `localhost:8080 connection refused` | Your kubeconfig is not set. Run `export KUBECONFIG=$HOME/.kube/rcp-caas-prod.yaml` and verify with `kubectl get ns`. |
| `Job name already exists` | Delete the old job first: `runai delete job <name> -p <project>` |
| `ImagePullBackOff` / `401 Unauthorized` | The image path is wrong or doesn't exist in the registry. Check with `docker pull <image>`. The registry project must be `proteindesign-containers`. |
| `/mnt/scratch` is read-only | Contact RCP admins — the PV needs `readOnly: false`. |
| `unknown shorthand flag: 'n'` | Use `--project` instead of `-n` for project/namespace. |
| `unknown parameter 'ro'` or `'accessmode-rwm'` | Use plain `--existing-pvc claimname=...,path=...` without access mode suffixes. |
| Job stuck in `Pending` | Check with `runai describe job <name>` — likely GPU quota or node-pool issue. |