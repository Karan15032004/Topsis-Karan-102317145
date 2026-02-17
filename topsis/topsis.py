import sys
import pandas as pd
import numpy as np


def main():

    # =========================
    # 1️⃣ Check command-line format
    # =========================
    if len(sys.argv) != 5:
        print("Error: Incorrect number of arguments.")
        print("Usage: topsis <inputfile> <weights> <impacts> <outputfile>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights_input = sys.argv[2]
    impacts_input = sys.argv[3]
    output_file = sys.argv[4]

    # =========================
    # 2️⃣ Read file & handle exception
    # =========================
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print("Error: Input file not found.")
        sys.exit(1)
    # Standardize common missing representations
    df.replace(['NA', 'N/A', 'null', 'NULL', '--', '?', 'None', ''], np.nan, inplace=True)

    # Remove rows with missing criteria values
    df = df.dropna(subset=df.columns[1:])

    # =========================
    # 3️⃣ Check minimum column count
    # =========================
    if df.shape[1] < 3:
        print("Error: Input file must contain at least 3 columns.")
        sys.exit(1)

    # Separate identifier column
    names = df.iloc[:, 0]
    data = df.iloc[:, 1:]

    # =========================
    # Parse weights and impacts
    # =========================
    try:
        weights = list(map(float, weights_input.split(',')))
    except:
        print("Error: Weights must be numeric and comma-separated.")
        sys.exit(1)

    impacts = impacts_input.split(',')

    if not all(i in ['+', '-'] for i in impacts):
        print("Error: Impacts must be '+' or '-'.")
        sys.exit(1)

    if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
        print("Error: Number of weights and impacts must match number of criteria columns.")
        sys.exit(1)

    # =========================
    # 4️⃣ Predefined Ordinal Scales
    # =========================

    ordinal_scales = [

        ["very low", "low", "medium", "high", "very high"],

        ["very bad", "bad", "average", "good", "very good"],

        ["poor", "fair", "good", "very good", "excellent"],

        ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"],

        ["very unlikely", "unlikely", "possible", "likely", "very likely"],

        ["extremely low", "low", "moderate", "high", "extremely high"]
    ]

    max_scale_length = max(len(scale) for scale in ordinal_scales)

    valid_indices = []

    for idx, col in enumerate(data.columns):

        column = data[col]

        # If numeric → keep
        if pd.api.types.is_numeric_dtype(column):
            valid_indices.append(idx)

        # If object → check ordinal possibility
        elif not pd.api.types.is_numeric_dtype(column):

            unique_vals = set(column.astype(str).str.lower().unique())

            if len(unique_vals) <= max_scale_length:

                matched = False

                for scale in ordinal_scales:
                    if unique_vals.issubset(set(scale)):
                        mapping = {val: i+1 for i, val in enumerate(scale)}
                        data[col] = column.astype(str).str.lower().map(mapping)
                        valid_indices.append(idx)
                        matched = True
                        break

                if not matched:
                    print(f"Dropping non-ordinal categorical column: {col}")

            else:
                print(f"Dropping text column: {col}")

        else:
            print(f"Dropping unsupported column type: {col}")

    # Filter data, weights, impacts
    data = data.iloc[:, valid_indices]
    weights = [weights[i] for i in valid_indices]
    impacts = [impacts[i] for i in valid_indices]
   
# =========================
# Remove rows where mapping created NaN
# =========================
    data = data.dropna()
    names = names.loc[data.index]
    
    # Ensure dataset is not empty
    if data.shape[0] == 0:
        print("Error: No valid rows remain after cleaning.")
        sys.exit(1)

# Ensure all columns are numeric
    if not all(pd.api.types.is_numeric_dtype(data[col]) for col in data.columns):
        print("Error: Non-numeric columns remain after preprocessing.")
        sys.exit(1)

    # =========================
    # 5️⃣ Re-check column count
    # =========================
    if data.shape[1] < 2:
        print("Error: Less than 2 criteria columns remain after cleaning.")
        sys.exit(1)

    # =========================
    # TOPSIS STEP 1: Normalization
    # =========================

    norm_data = data / np.sqrt((data**2).sum())

# =========================
#  Weighted Normalized Matrix
# =========================
    weights_array = np.array(weights)
    weighted_data = norm_data * weights_array
# =========================
#  Ideal Best & Worst
# =========================
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
        else:
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

  # =========================
#  Distance Calculation
# =========================
    distance_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

# =========================
#  Closeness Coefficient
# =========================
    topsis_score = distance_worst / (distance_best + distance_worst)

# =========================
#  Ranking
# =========================

# Add Topsis Score to original dataframe
    df['Topsis Score'] = topsis_score.round(2)

# Add Rank (Higher score = better rank)
    df['Rank'] = df['Topsis Score'].rank(method='max', ascending=False).astype(int)

# =========================
#  Save Output
# =========================
    df.to_csv(output_file, index=False)

    print("TOPSIS computation completed successfully.")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
