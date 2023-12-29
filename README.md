# 2millionpuzzle.hydra
Piece tagging and profiling companion for the Two Million Dollar Puzzle.

## Setup

```bash
virtualenv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
```
