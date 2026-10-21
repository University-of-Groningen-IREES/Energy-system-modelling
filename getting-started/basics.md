# Python and Jupyter Basics

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

## Simple operators

Python can be used as a calculator.

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | Addition | `5 + 2` | `7` |
| `-` | Subtraction | `5 - 2` | `3` |
| `*` | Multiplication | `5 * 2` | `10` |
| `/` | Division | `5 / 2` | `2.5` |
| `//` | Floor division | `5 // 2` | `2` |
| `%` | Remainder | `5 % 2` | `1` |
| `**` | Power | `5 ** 2` | `25` |

Try each expression in a separate code cell:

```python
10 + 5
```

```python
20 / 4
```

```python
2 ** 3
```

Python displays the result of the last expression in a code cell.
Use `print()` when you want to display several results:

```python
print(10 + 5)
print(20 / 4)
print(2 ** 3)
```

### Order of operations

Multiplication and division are evaluated before addition and subtraction:

```python
2 + 3 * 4
```

The result is `14`.

Use parentheses to change the order:

```python
(2 + 3) * 4
```

The result is `20`.

## Store values in variables

A variable gives a name to a value. Use `=` to assign that value:

```python
power_kw = 2
duration_hours = 3
```

We can then use these variables in a calculation:

```python
energy_kwh = power_kw * duration_hours

print(energy_kwh)
```

The result is `6`: operating at a constant power of 2 kW for 3 hours
uses 6 kWh of energy.

Python does not automatically check physical units. Use consistent
units and choose variable names that explain what the values represent.

### Variable names

Variable names:

- Can contain letters, numbers, and underscores.
- Cannot start with a number.
- Cannot contain spaces.
- Are case-sensitive: `power_kw` and `Power_kw` are different names.

For example:

```python
electricity_price_eur_per_kwh = 0.30

cost_eur = energy_kwh * electricity_price_eur_per_kwh

print(cost_eur)
```

Decimal numbers use a point, such as `0.30`, rather than a comma.

## Add comments

Comments explain your code. Python ignores text following `#`
on the same line:

```python
# Calculate consumption at constant power
energy_kwh = power_kw * duration_hours

print(energy_kwh)
```

## Compare values

Comparisons return one of two Boolean values: `True` or `False`.

| Operator | Meaning |
|---|---|
| `==` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

For example:

```python
energy_kwh > 5
```

The result is `True`.

```python
energy_kwh == 10
```

The result is `False`.

Remember: `=` assigns a value, while `==` compares values.

## Run cells in order

A notebook's kernel is the process that executes your Python code
and holds variables in memory.

Run cells from top to bottom. A variable must be defined before a
later cell can use it.

For example, this calculation requires `power_kw` and `duration_hours`
to have been defined:

```python
energy_kwh = power_kw * duration_hours
```

If you change an input value, run the calculation again to update
the result.

Restarting the kernel clears variables from memory. Your saved code
remains in the notebook, but you must run it again.

In JupyterLab, use **Kernel → Restart Kernel and Run All Cells**
to check that your notebook works from beginning to end.

## Practice

An appliance operates at a constant power of **1.5 kW** for **4 hours**.
Electricity costs **0.30 EUR/kWh**.

In a new code cell:

1. Store the power, operating time, and electricity price in variables.
2. Calculate the energy consumption in kWh.
3. Calculate the electricity cost in euros.
4. Check whether consumption exceeds 5 kWh.
5. Display your results using `print()`.

Save your notebook when you finish.