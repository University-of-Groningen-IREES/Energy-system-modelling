# Getting Ready: Miniforge

To follow the course on your computer, we first need to install Python,
the required packages, and JupyterLab.

We use Miniforge to manage this setup. Miniforge includes Conda and Mamba:
tools for creating environments and installing software packages.

If you cannot install software on your computer, you can use the
browser-based option described at the end of this page.

## Why use an environment?

An environment is an isolated workspace containing Python and the
packages required for a project.

Different projects may require different versions of the same package.
Separate environments help prevent conflicts and make it easier to
reproduce a project on another computer.

We will create an environment called `managing-data` for this course.

## Install Miniforge on Windows

### 1. Check whether Miniforge is already installed

Search for **Miniforge Prompt** in the Windows Start menu.

If you find it, open it and run:

```bash
mamba --version
conda --version
```

If both commands display version numbers, continue to
**Create the course environment** below.

### 2. Download and install Miniforge

Open the [official Miniforge download page](https://conda-forge.org/download/).

Choose the Windows installer appropriate for your computer.
For most Windows computers with Intel or AMD processors, this is
the **Windows x86_64** installer.

Run the installer:

1. Select **Just Me**.
2. Keep the default installation options.
3. Complete the installation.

### 3. Open Miniforge Prompt

Search for **Miniforge Prompt** in the Start menu and open it.

Check the installation:

```bash
mamba --version
conda --version
```

Use **Miniforge Prompt** for the remaining commands on Windows.
An ordinary PowerShell window may require additional configuration
before it recognises these commands.

## Install Miniforge on macOS

### 1. Check whether Miniforge is already installed

Open **Terminal**, which you can find using Spotlight:
press **Command + Space**, type `Terminal`, and press Enter.

Run:

```bash
mamba --version
conda --version
```

If both commands display version numbers, continue to
**Create the course environment** below.

### 2. Identify your Mac's processor

Open the **Apple menu → About This Mac**.

- If you see an Apple chip, such as M1, M2, M3, or M4, choose
  the **macOS arm64 / Apple Silicon** installer.
- If you see an Intel processor, choose the **macOS x86_64 / Intel**
  installer.

### 3. Download and install Miniforge

Open the [official Miniforge download page](https://conda-forge.org/download/)
and download the installer for your processor.

For the shell installer (`.sh` file), open Terminal and go to Downloads:

```bash
cd ~/Downloads
```

For an Apple Silicon Mac, run:

```bash
bash Miniforge3-MacOSX-arm64.sh
```

For an Intel Mac, run:

```bash
bash Miniforge3-MacOSX-x86_64.sh
```

Run only the command matching the file you downloaded.
If its name includes a version number, use that complete filename.

Follow the prompts:

1. Review and accept the licence.
2. Accept the default installation location.
3. Answer `yes` when asked to initialise Conda.

Close Terminal and open a new Terminal window.

### 4. Check the installation

Run:

```bash
mamba --version
conda --version
```

Both commands should display version numbers.

## Create the course environment

The following commands are the same on Windows and macOS.

Use **Miniforge Prompt on Windows** or **Terminal on macOS**.

Copy only the commands below. Do not include terminal prompts or
output from previous commands.

### 1. Create the environment

Run:

```bash
mamba create -n managing-data python=3.12 pandas numpy matplotlib jupyterlab -c conda-forge
```

When asked to proceed, type `y` and press Enter.

This installs:

| Package | Purpose |
|---|---|
| Python | Run our code |
| pandas | Read, organise, and analyse tabular data |
| NumPy | Work with numerical arrays |
| Matplotlib | Create plots |
| JupyterLab | Create and run notebooks |

Create this environment only once. If `managing-data` already exists,
skip this step.

### 2. Activate the environment

Run:

```bash
conda activate managing-data
```

The terminal prompt should now begin with `(managing-data)`.

Activate the environment whenever you open a new terminal to work
on this course.

### 3. Launch JupyterLab

Run:

```bash
jupyter lab
```

JupyterLab should open in your browser.

Although it appears in a browser, JupyterLab runs on your computer.
Keep its terminal window open while you work.

You are now ready to continue to **Python and Jupyter Basics**.

## If you cannot install software

You can complete the introductory Python exercises using
[Google Colab](https://colab.research.google.com/).

Colab runs notebooks in a hosted environment, so you do not need to
install Miniforge or create an environment locally.

1. Open Google Colab.
2. Sign in with a Google account.
3. Select **New notebook**.
4. Continue with the notebook exercises on the next page.

Save your notebook in Google Drive or download it as an `.ipynb` file.
Files and variables stored in the running session are temporary.

If your institution also restricts access to Colab, ask your instructor
which notebook platform to use.