# QE Foundations

A Python utility library for reusable quality-engineering helpers and data validation workflows.

## Project 1 milestone - Week 2, Monday

The initial project structure is in place, including the qe_foundations package, the utils sub-package, dependency files, documentation, and placeholders for upcoming work

Planned development for the rest of the week:

* **Tuesday:** Add data ingestion components under qe_foundations/ingestion/.
* **Wednesday:** Add logging and unit tests under tests/.
* **Thursday:** Add SQL validation queries under sql/.
* **Friday:** Add join validation and integration wor

## Setup

1. Create a virtual environment

   python -m venv .venv
2. Activate the environment

   Windows PowerShell:

   .venv\Scripts\Activate.ps1

   bash / Git Bash:

   source .venv/bin/activate
3. Install dependencies

   python -m pip install -r requirements.txt

   For development tools:

   python -m pip install -r requirements-dev.txt
4. Verify the installation

   python smoke_utils.py

   The smoke script should finish with 7/7 checks passed.

## Usage Example

```python
from qe_foundations.utils import slugify, mask_email

print(slugify("  Hello World  "))
print(mask_email("tester@example.com"))
```

Expected output:

```text
hello-world
t***@example.com
```
