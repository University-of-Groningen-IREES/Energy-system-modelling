# Course update: real OSM data and PyPSA notebooks

This package adds a real-data continuation to GeoPandas and two executed PyPSA teaching notebooks for Renewable Energy Systems at the University of Groningen. It is an update package, not a replacement for your whole repository.

## Copy the files into the project

Merge `managing-data/` and `pypsa-tutorial/` into the corresponding folders in `Energy-system-modelling`. Preserve the other lessons and images already there. Review the updated GeoPandas lesson before replacing a locally edited copy.

The GeoPandas explanations through **Create illustrative zones** are retained. The opening task now distinguishes synthetic introductory data from the subsequent real OSM extract. The rest of the lesson analyses mapped footprints, not invented real-world demand.

## Update the table of contents

In `_toc.yml`, retain your existing sections. Under its existing PyPSA caption, use:

```yaml
  - caption: PyPSA Tutorial
    chapters:
      - file: pypsa-tutorial/intro
      - file: pypsa-tutorial/installation
      - file: pypsa-tutorial/01-electricity-markets
      - file: pypsa-tutorial/02-investment-and-storage
      - file: pypsa-tutorial/groningen
```

Use this block inside the existing `parts:` list. Do not create a second `parts:` key. Notebook entries omit `.ipynb`, just as Markdown entries omit `.md`. Keep the existing `managing-data/geopandas` entry in the data-library section.

## Display the saved figures when building

In the existing `_config.yml`, set the corresponding values:

```yaml
only_build_toc_files: true

execute:
  execute_notebooks: "off"
```

Merge this into your existing configuration; do not add a second `execute:` key. This tells Jupyter Book 1 to display the saved notebook outputs. Students still run the downloaded notebooks normally. It also prevents a website build from starting solvers or live OSM requests. If you later want build-time execution, use an environment with the notebook dependencies and update the execution settings deliberately.

The notebook download menu is normally available in Jupyter Book 1. If you have disabled it, merge this option into your existing `sphinx.config.html_theme_options` mapping:

```yaml
sphinx:
  config:
    html_theme_options:
      use_download_button: true
```

Preserve your existing title, logo, and other Sphinx options. Source downloads expose notebook code and outputs, which is intended for these two teaching pages.

## Keep personal notebooks ignored; publish the two course notebooks

You previously chose to ignore notebooks. These two files are now intentional course resources, so add the following exceptions **after** your `*.ipynb` rule in `.gitignore`:

```gitignore
*.ipynb
.ipynb_checkpoints/
_build/

# Curated teaching notebooks and their generated download copies
!/pypsa-tutorial/01-electricity-markets.ipynb
!/pypsa-tutorial/02-investment-and-storage.ipynb
!/docs/_sources/pypsa-tutorial/01-electricity-markets.ipynb
!/docs/_sources/pypsa-tutorial/02-investment-and-storage.ipynb

# Download caches and model exports remain local
/pypsa-tutorial/data/*.csv
/pypsa-tutorial/outputs/
```

Do not ignore the OSM GeoJSON: it is an intentional classroom dataset. Do not run the earlier blanket command to remove every `.ipynb` under `docs`; it would remove these two downloadable teaching notebooks too.

## Build and check locally

From the repository root in PowerShell:

```powershell
conda activate managing-data
jupyter-book build . --all
```

Continue only if the build succeeds. Then open:

```powershell
Start-Process ".\_build\html\index.html"
```

Check the new navigation, the GeoPandas maps, both notebooks' figures, and their download menu. Run the notebooks using the separate `pypsa-course` environment described in the installation lesson. The investment notebook needs internet on its first run to obtain the source solar CSV, then uses its local cache. The main GeoPandas exercise works offline using the included extract; its optional fresh OSM query needs internet.

## Refresh GitHub Pages

After the successful build:

```powershell
Copy-Item -Path ".\_build\html\*" -Destination ".\docs" -Recurse -Force
New-Item -ItemType File -Path ".\docs\.nojekyll" -Force

git add .
git diff --cached --stat
git diff --cached --name-only --diff-filter=ACM -- "*.ipynb"
```

The last command should list only the two curated notebooks and their two generated download copies. If another notebook appears, unstage it with `git restore --staged -- "path/to/file.ipynb"` and check your ignore rules. Also review datasets and images in the staged changes before committing.

```powershell
git commit -m "Add real OSM GeoPandas examples and PyPSA teaching notebooks"
git push origin main
```

These commands are for your Windows checkout; this package has not been pushed to your repository. After GitHub's Pages deployment succeeds, refresh the course website.

## What remains pending

The Groningen PyPSA case needs the instructor's datasets. `pypsa-tutorial/groningen.md` lists the required inputs without asserting invented results. The supplied OSM extract serves the GeoPandas lesson only; it is not an energy-demand dataset for the future optimisation case.

See `TEACHING-NOTES.md` for the reasons behind each instructional change and `VALIDATION.md` for the checks performed.
