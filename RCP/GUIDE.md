# Getting Started with RunAI on EPFL's RCP — From Zero to Running Jobs


This guide walks you through everything you need to do to successfully run protein design workloads on EPFL's RCP cluster using Runai! We'll cover:
1. Setting up your local environment 
2. Configuring access to the RCP cluster
3. Managing your data
4. Running interactive jobs
5. Managing jobs
6. Code development with VScode

<u>**Note**</u>: A lot of online resources in this guide, e.g RCP's wiki, are only accessible if you're connected to the EPFL network (either on campus or via VPN). You also need to be connected to the network to authenticate with RunAI and access the RCP cluster.



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

The above command downloads a file should look like this. You can also create the file manually and copy/paste the content from the [RCP wiki](https://wiki.rcp.epfl.ch/home/CaaS/FAQ/how-to-use-runai). Content looks something like this:

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: <base64-cert>
    server: https://caas-prod.rcp.epfl.ch:443
  name: caas-prod.rcp.epfl.ch
contexts:
- context:
    cluster: caas-prod.rcp.epfl.ch
    user: runai-rcp-authenticated-user
  name: rcp-caas-prod
current-context: rcp-caas-prod
kind: Config
users:
- name: runai-rcp-authenticated-user
  user:
    auth-provider:
      name: oidc
      config:
        airgapped: "true"
        auth-flow: remote-browser
        client-id: runai-cli
        idp-issuer-url: https://app.run.ai/auth/realms/rcpepfl
        realm: rcpepfl
        redirect-uri: https://rcpepfl.run.ai/oauth-code
```

### 2.2 Activate the kubeconfig

```bash
export KUBECONFIG=$HOME/.kube/rcp-caas-prod.yaml
```

> **Tip:** Add this line to your `~/.bashrc` or `~/.zshrc` so it persists across sessions.

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

We are now ready to launch our first interactive job on RCP! Interactive jobs are ideal for development and experimentation — they give you a live terminal inside a container running on the cluster, where you can run commands, test code, and iterate quickly. Two essential parts of any runai job are:
- _The container image:_ a container image is a pre-packaged environment that includes the software and dependencies you need to run a certain job. For the hackathon, we have prepared container images for each model.
- _The persistent volumes:_ When running an interactive job, you will tell runai to mount both your group's scratch storage and the shared read-only storage into the container. The first one will allow you to save tour work done during the interactive session (remember that the container filesystem is ephemeral!) while the second one will give you access to shared datasets and model weights needed to run the models.

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
  --run-as-user \
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
| `--run-as-user` | Map your EPFL UID/GID into the container |
| `--existing-pvc` | Mount existing storage volumes, `path` specifies the location inside the container |
| `--command -- /bin/bash` | Start an interactive shell |
Example for group 11:

A terminal inside the container will open after a few moments. While waiting, you can check the status of your job by running in another terminal:

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

```bash
runai submit rfd3-g11 \
  --project hackathon-proteindesign-singer \
  -i registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1 \
  --interactive \
  --attach \
  --node-pools default \
  -g 1 \
  --run-as-user \
  --existing-pvc claimname=hackathon-proteindesign-scratch-g11,path=/mnt/scratch \
  --existing-pvc claimname=hackathon-proteindesign-shared-ro,path=/mnt/shared-ro \
  --command -- /bin/bash
```

After disconnecting, don't forget to delete your interactive job to free up cluster resources:

```bash
runai delete job <job-name>
```

### 4.2 RFD3 interactive job
### 5.2 What the flags mean

| Flag | Purpose |
|------|---------|
| `--project` | Your RunAI project (from `runai list projects`) |
| `-i` | Container image from the RCP registry |
| `--interactive` | Interactive job (non-preemptible, max 12h) |
| `--attach` | Automatically attach to the pod once running, aka open a terminal inside the container |
| `--node-pools default` | Use A100 GPUs (default pool). Omit for V100. |
| `-g 1` | Request 1 GPU |
| `--run-as-user` | Map your EPFL UID/GID into the container |
| `--existing-pvc` | Mount existing storage volumes |
| `--command -- /bin/bash` | Start an interactive shell |

### 5.3 Storage inside the pod

| Path | Description | Access |
|------|-------------|--------|
| `/mnt/scratch` | Your group's persistent scratch storage | Read-Write |
| `/mnt/shared-ro` | Shared datasets and model weights | Read-Only |

> **Always save your work to `/mnt/scratch`!** The container filesystem is ephemeral — anything not on a mounted volume is lost when the job ends.

---

## Step 6: Managing Jobs

### Check job status
```bash
runai describe job <job-name> -p <project>
```

### List all jobs
```bash
runai list jobs -p <project>
```

### Attach to a running job (if you disconnected)
```bash
runai attach <job-name> -p <project>
```

### Delete a job
```bash
runai delete job <job-name> -p <project>
```

---

## Step 7: Switching Between Tools

The same storage volumes work with any container image. Simply change the `-i` flag:

```bash
# RFdiffusion3
-i registry.rcp.epfl.ch/proteindesign-containers/rfd3:2026.1

# AlphaFold 3
-i registry.rcp.epfl.ch/proteindesign-containers/af3:2026.1

# Boltz
-i registry.rcp.epfl.ch/proteindesign-containers/boltz:2026.1

# Chai-1
-i registry.rcp.epfl.ch/proteindesign-containers/chai:2026.1

# CARBonAra
-i registry.rcp.epfl.ch/proteindesign-containers/carbonara:2026.1

# LigandMPNN
-i registry.rcp.epfl.ch/proteindesign-containers/ligandmpnn:2026.1
```

All containers mount the same PVCs, so your data on `/mnt/scratch` persists across tools.

---

## Transferring Files to/from RCP

Use the jumphost to transfer files:

```bash
# Upload to your group's scratch
rsync -av --no-group local_files/ \
  <gaspar>@jumphost.rcp.epfl.ch:/mnt/hackathon-proteindesign/hackathon-proteindesign-gXX/scratch-gXX/

# Download from scratch
rsync -av --no-group \
  <gaspar>@jumphost.rcp.epfl.ch:/mnt/hackathon-proteindesign/hackathon-proteindesign-gXX/scratch-gXX/results/ \
  local_results/
```

---

## Important Notes

- **Interactive jobs have a 12-hour maximum runtime.** Save your work frequently.
- **Interactive jobs are non-preemptible** — they won't be interrupted (except for hardware failures).
- **GPU limits**: 1x A100 or 1x V100 per interactive job.
- **H100/H200 GPUs are not available for interactive jobs** — only for training workloads.
- **The "I have no name" prompt** is cosmetic — it appears because `--run-as-user` maps your UID into the container without a matching `/etc/passwd` entry. Everything still works correctly.
- **Containers are ephemeral** — only data on `/mnt/scratch` and `/mnt/shared-ro` persists.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `localhost:8080 connection refused` | Your kubeconfig is not set. Run `export KUBECONFIG=$HOME/.kube/rcp-caas-prod.yaml` and verify with `kubectl get ns`. |
| `Job name already exists` | Delete the old job first: `runai delete job <name> -p <project>` |
| `ImagePullBackOff` / `401 Unauthorized` | The image path is wrong or doesn't exist in the registry. Check with `docker pull <image>`. The registry project must be `proteindesign-containers`. |
| `/mnt/scratch` is read-only | Contact RCP admins — the PV needs `readOnly: false`. |
| `unknown shorthand flag: 'n'` | Use `--project` instead of `-n` for project/namespace. |
| `unknown parameter 'ro'` or `'accessmode-rwm'` | Use plain `--existing-pvc claimname=...,path=...` without access mode suffixes. |
| Job stuck in `Pending` | Check with `runai describe job <name>` — likely GPU quota or node-pool issue. |
