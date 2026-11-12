# Getting ready for PyPSA

[PyPSA — Python for Power System Analysis](https://pypsa.org/) models energy systems and optimises their operation and investment. Start with the [official installation guide](https://docs.pypsa.org/latest/home/installation/).

## Your task

Install a separate course environment, register its notebook kernel, and solve a very small system before opening the teaching notebooks.

## Learning objectives

- Explain the roles of an installer, a package manager, an environment, and a solver.
- Install PyPSA and launch a notebook with the correct kernel.
- Confirm that an optimisation finishes successfully.

## Can I use Miniconda?

**Yes.** Miniconda and Miniforge install the `conda` package manager. They are not alternatives to the `conda` command: both provide it. You can use either distribution for this course. Miniforge also provides `mamba`. There is no need to reinstall a working distribution.

An environment keeps the PyPSA lesson's packages separate from other projects. We use a new environment named `pypsa-course` so the earlier `managing-data` environment can continue to serve the introductory lessons. See [conda's installation documentation](https://docs.conda.io/projects/conda/en/stable/user-guide/install/).

## Open your terminal

On **Windows**, open Miniforge Prompt, or Anaconda Prompt if you installed Miniconda. On **macOS**, open Terminal after your distribution's shell setup is complete. The commands below are the same on both systems.

Check that the package manager is available:

```bash
conda --version
```

## Install the course environment

Run this as one line, then accept the proposed installation:

```bash
conda create -n pypsa-course --override-channels -c conda-forge python=3.12 pypsa=1.4.0 highspy=1.15.1 pandas matplotlib jupyterlab ipykernel cartopy
```

Here `--override-channels -c conda-forge` asks for packages from conda-forge for this operation. `highspy` is the Python interface to the open-source **HiGHS** optimisation solver. No commercial solver licence is required for these examples. However, depending on the complexity of your problem, you may need to use Gurobi as an optimisation solver for your master's thesis. **Gurobi** is the best optimisation tool, and a free version is available for students.


Then activate your virtual environment:

```bash
conda activate pypsa-course
```

## Register the notebook kernel for pypsa

Remember that an environment contains Python and libraries or pacakges. A notebook kernel is the Python process that executes a notebook's cells. And jupyter is just the interface. So, to see the python environment on Jupyter, you need to register the environment. While have your virtual environment **pypsa-course** activated run on your terminal:

```bash
python -m ipykernel install --user --name pypsa-course --display-name "Python (pypsa-course)"

python -c "import pypsa, highspy; print('PyPSA', pypsa.__version__); print('HiGHS', highspy.Highs().version())"
```

If you want to check, that your kernel is correctly registered, run:

```bash
jupyter kernelspec list
```

Then, launch JupyterLab from your course project folder:

```bash
jupyter lab
```

Keep the terminal open. Open a lesson notebook and select **Python (pypsa-course)** from the kernel selector. If it is missing, stop JupyterLab, repeat kernel registration in the activated environment, and restart JupyterLab. In a notebook, `import sys; print(sys.executable)` should point into `pypsa-course`.

## Continue with the notebooks

Open **Introduction to pypsa: a simple dispatch problem** first, then **Electricity markets** , and finish with **Investment and storage**. Read them online or download their `.ipynb` source from the book's download menu. The displayed figures are saved notebook outputs; the static website does not run a solver when you change a cell. You can download and run the notebook locally in your laptop.