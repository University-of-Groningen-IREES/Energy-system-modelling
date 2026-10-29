# Jupyter Basics

In this lesson, we create a notebook and practise calculations,
variables, and comparisons in Python.

Before starting, complete [Getting Ready: Miniforge](miniforge.md).
Your course environment and JupyterLab should already be installed.

## Open JupyterLab

If JupyterLab is already running, continue to the next section.

Otherwise, open **Miniforge Prompt on Windows** or **Terminal on macOS**
and run:

```bash
conda activate managing-data
```

Then launch JupyterLab:

```bash
jupyter lab
```

Keep the terminal open while you work.

If you are using Google Colab, open
[Colab](https://colab.research.google.com/) and select **New notebook**.

## Create a new notebook

In JupyterLab:

1. Navigate to the folder where you want to save your notebook.
2. Click **File → New Launcher**, or click the **+** button.
3. Under **Notebook**, select **Python 3**. The label may also include
   the kernel name, such as `ipykernel`.
4. Right-click the notebook's tab and select **Rename Notebook**.
5. Name it `01-python-basics.ipynb`.

The `.ipynb` extension identifies a Jupyter notebook.

## Understand notebook cells

A notebook combines two main types of cells:

- **Code cells** contain Python instructions that you can execute.
- **Markdown cells** contain explanations, headings, lists, and equations.

You can change a selected cell's type using the dropdown menu in
the notebook toolbar.

### Run your first code cell

In a code cell, enter:

```python
print("Hello, energy modellers!")
```

Press **Shift + Enter**.

The output appears below the cell:

```text
Hello, energy modellers!
```

**Shift + Enter** runs the selected cell and moves to the next one.
**Ctrl + Enter** runs it while keeping the same cell selected.

### Add a Markdown cell

Select an empty cell and change its type from **Code** to **Markdown**.

Enter:

```markdown
## My first calculation

In this notebook, I will calculate energy consumption using Python.
```

Press **Shift + Enter** to display the formatted text.

### Save your notebook

Use **File → Save Notebook**, or press:

- **Ctrl + S** on Windows.
- **Command + S** on macOS.