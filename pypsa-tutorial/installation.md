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
conda create -n pypsa-course --override-channels -c conda-forge python=3.12 pypsa=1.4.0 highspy=1.15.1 pandas matplotlib jupyterlab ipykernel
conda activate pypsa-course
```

With Miniforge you may replace `conda create` with `mamba create`. Use one command, not both. The version pins match the environment used to check this teaching package. Later PyPSA releases may require checking their release notes before upgrading.

`--override-channels -c conda-forge` asks for packages from conda-forge for this operation. `highspy` is the Python interface to the open-source **HiGHS** optimisation solver. No commercial solver licence is needed for these examples.

Alternatively, from the repository root, use the included environment file:

```bash
conda env create -f pypsa-tutorial/environment.yml
conda activate pypsa-course
```

The environment file and the direct create command are alternatives. If `pypsa-course` already exists, activate and inspect it instead of trying to create it again.

## Register a notebook kernel

An environment contains Python and packages. A notebook kernel is the Python process that executes a notebook's cells. Register the environment so Jupyter can offer it:

```bash
python -m ipykernel install --user --name pypsa-course --display-name "Python (pypsa-course)"
python -c "import pypsa, highspy; print('PyPSA', pypsa.__version__); print('HiGHS', highspy.Highs().version())"
jupyter kernelspec list
```

Launch JupyterLab from your course project folder:

```bash
jupyter lab
```

Keep the terminal open. Open a lesson notebook and select **Python (pypsa-course)** from the kernel selector. If it is missing, stop JupyterLab, repeat kernel registration in the activated environment, and restart JupyterLab. In a notebook, `import sys; print(sys.executable)` should point into `pypsa-course`.

## Test a small optimisation

Create a new notebook and run:

```python
import pypsa

n = pypsa.Network()
n.add("Carrier", "electricity")
n.add("Bus", "Site", carrier="electricity")
n.add("Load", "Demand", bus="Site", p_set=1.0)
n.add("Generator", "Supply", bus="Site", carrier="electricity",
      p_nom=2.0, marginal_cost=50.0)
status, condition = n.optimize(
    solver_name="highs", io_api="direct", log_to_console=False,
    include_objective_constant=False,
)
print("Status:", status)
print("Termination:", condition)
if status != "ok" or condition != "optimal":
    raise RuntimeError("The installation test did not solve successfully.")
print(n.generators_t.p)
```

Expect status `ok`, termination `optimal`, and supply of 1 MW. The solver meets a 1 MW load using the available 2 MW generator. Some informational messages about shadow prices are normal; the termination condition is what establishes whether this test solved.

## Continue with the notebooks

Open **Electricity markets** first, then **Investment and storage**. Read them online or download their `.ipynb` source from the book's download menu. The displayed figures are saved notebook outputs; the static website does not run a solver when you change a cell. Download and run the notebook locally for an experiment.

## Record your installation

From the activated environment:

```bash
conda env export --no-builds > pypsa-course-resolved.yml
```

This records installed versions for reproducibility; it is more specific than the starter environment file. Package builds and operating systems can still differ. Share your operating system and these versions when reporting an installation problem.
