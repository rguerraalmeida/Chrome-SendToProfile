# Pull Request Troubleshooting

If PR creation fails, run this first:

```bash
./scripts/pr-preflight.sh
```

## Common failures and fixes

### 1) `No origin remote configured`
Add your GitHub repository remote:

```bash
git remote add origin <https-or-ssh-repo-url>
```

### 2) `Remote branch origin/<branch> not found`
Push the local branch first:

```bash
git push -u origin <branch>
```

### 3) `gh: command not found`
Install GitHub CLI or open a PR through the GitHub web UI.

### 4) `gh` installed but auth missing
Authenticate once:

```bash
gh auth login
```

### 5) Working tree has uncommitted changes
Commit changes before PR creation:

```bash
git add .
git commit -m "<message>"
```

## Recommended sequence

```bash
./scripts/pr-preflight.sh
git push -u origin $(git branch --show-current)
gh pr create --fill
```
