# Push this scaffold to GitHub

The repository `akiroussama/PrivIMU` currently exists but is empty. To push this scaffold:

```bash
# Option A: from an empty clone
git clone https://github.com/akiroussama/PrivIMU.git
cd PrivIMU
cp -a /path/to/PrivIMU_scaffold/. .
git add .
git commit -m "feat: initialize reproducible PrivIMU lab"
git push origin main
```

Or from inside the scaffold folder:

```bash
git init
git branch -M main
git remote add origin https://github.com/akiroussama/PrivIMU.git
git add .
git commit -m "feat: initialize reproducible PrivIMU lab"
git push -u origin main
```

Recommended commit footer:

```text
Verified-By: pytest -q
Refs: PRIVIMU_BRIEF.md
```
