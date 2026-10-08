# Week 2: git commands

## Set up
```
git --version
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

## Initialise
```
mkdir git-playground
cd git-playground
git init
ls -a
```

## Status
Create `analysis.py` and save.
```
git status
```

## Commit
```
git add analysis.py
git status
git commit -m "Add analysis script"
git status
```

## Commit again
Edit `analysis.py` and save.
```
git status
git add analysis.py
git commit -m "Print a loading message"
```

## Log
```
git log --oneline
```

## Diff
Edit `analysis.py` and save.
```
git diff
git diff --staged
git add analysis.py
git diff
git diff --staged
git commit -m "Say what is being loaded"
```

## Time travel
```
git log --oneline
git checkout <hash>
```
Read the "detached HEAD" message out loud. Then look around:
```
cat analysis.py
git status
git log --oneline
```
The file is back as it was, and the log stops at this commit. Reattach by naming the branch:
```
git switch main
git status
cat analysis.py
```
`git checkout main` does the same. `git switch -` ("the previous branch") only works if you
came straight from a branch: hop between two hashes and it refuses, because the place you came
from was a commit.

## .gitignore
Create `.env` with a fake key, and `data/big.csv`.
```
git status
```
Create `.gitignore`:
```
.env
data/
```
```
git status
git check-ignore -v data/big.csv
git add .gitignore
git commit -m "Ignore secrets and data"
git status --ignored
```
## Your turn
Go to your exercise notebook now. Complete exercises 1-4.

## Branch
```
git branch
git switch -c experiment
git branch
```
Edit `analysis.py` and save.
```
git add analysis.py
git commit -m "Try an extra print"
git switch main
```
Create `notes.md` and save.
```
git add notes.md
git commit -m "Note the data source"
git log --oneline --graph --all
```

## Merge
```
git switch main
git merge experiment
git log --oneline --graph --all
```

## Your turn!
Go to your exercise notebook now. Complete Exercises 5-7.

## Discard a change
Edit `notes.md` and save.
```
git status
git restore notes.md
```

## Unstage
Edit `notes.md` and save.
```
git add notes.md
git restore --staged notes.md
git status
git add notes.md
git commit -m "Add a line to the notes"
```

## Revert
```
git revert HEAD --no-edit
git log --oneline
```

## Your turn!
Go to your exercise notebook now. Complete exercises 8-10

## Remote
Create an empty private repository on GitHub. Copy its URL.
```
git remote -v
git remote add origin <url>
git remote -v
```

## Push
```
git push -u origin main
```

## Your turn
Move to `2.2-git-exercises.md` and complete exercises 1-4.

## Fetch and pull
Edit `notes.md` on GitHub and commit.
```
git fetch
git status
git pull
```

## The loop
```
git pull
```
Edit, save.
```
git add .
git commit -m "Print a summary line"
git push
```
## Your turn
Move to `2.2-git-exercises.md` and complete exercises 5-7.

## What does and does not get pushed
```
git push
```
On GitHub: `.gitignore` is there, `.env` and `data/` are not. They were never committed, so
there is nothing to push.
```
git log --oneline -- .env
```
Their `ds2026` already has a `.gitignore`, written for them. Open it:
```
cat ../ds2026/.gitignore
```

## Clone
```
cd ..
git clone <url> git-playground-clone
cd git-playground-clone
git remote -v
git log --oneline
```
