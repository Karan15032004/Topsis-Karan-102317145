<<<<<<< HEAD
# Topsis-Karan-102317145

This is a simple command-line implementation of the TOPSIS method in Python.

TOPSIS stands for Technique for Order Preference by Similarity to Ideal Solution.  
It is a multi-criteria decision-making method used to rank alternatives based on multiple criteria.

# Installation Guide
 
 Install from PyPI using:
 
 ```bash
pip install Topsis-Karan-102317145
```
After installation, you can use the topsis command directly in your terminal.

---
# Command Line Usage

After installation, run:

```bash
topsis <InputDataFile> <Weights> <Impacts> <OutputFile>
```
# Example:

```bash
topsis data.csv "1,1,1,1" "+,+,-,+" output.csv
```
---
## Parameter Explaination

- InputDataFile: CSV file containing alternatives and criteria
- Weights: Comma-separated numeric weights (e.g., "1,1,1,1")
- Impacts: Comma-separated '+' or '-' signs
- OutputFile: Name of the result CSV file

---
## What This Tool Does

1. Cleans the dataset
2. Handles numeric and ordinal data
3. Drops invalid or text-only columns
4. Normalizes the data
5. Applies weights
6. Calculates ideal best and worst
7. Computes TOPSIS score
8. Ranks alternatives
9. Saves result in output CSV

---
## Input File Format

Your CSV file must:

- Have at least 3 columns
- First column = Name / Identifier
- Remaining columns = Criteria
- Criteria must be numeric or ordinal

---

##  Output

The output file will have 2 additional columns than the input file:
1. The Topsis Score
2. The Topsis Rank


Higher score means better rank.

---
## Requirements

This package requires:

- Python >= 3.8
- pandas
- numpy

These dependencies are automatically installed during pip installation.

##  Important Notes

- Number of weights must match number of criteria.
- Number of impacts must match number of criteria.
- Impacts must be only `+` or `-`.
- Missing values are automatically handled.
- Text-only columns are ignored.

---

##  Author

Karan Nigam
Roll No: 102317145  

---
# License

This project is licensed under the MIT License.

---

Thank you for using this package!!
=======
