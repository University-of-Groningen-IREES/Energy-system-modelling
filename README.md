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
