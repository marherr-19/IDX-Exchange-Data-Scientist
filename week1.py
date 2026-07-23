import pandas as pd
import os

# Config
DATA_FOLDER = "california"
START_YEAR = 2024
START_MONTH = 1
END_YEAR = 2026
END_MONTH = 6
OUTPUT_CLEAN = "cleaned_single_family_sales.csv"
OUTPUT_COLUMNS = "column_dictionary.csv"


# Find files
files = []
for year in range(START_YEAR, END_YEAR + 1):
    for month in range(1, 13):

        if year == START_YEAR and month < START_MONTH:
            continue

        if year == END_YEAR and month > END_MONTH:
            continue

        filename = f"CRMLSSold{year}{month:02d}.csv"
        filepath = os.path.join(DATA_FOLDER, filename)

        if os.path.exists(filepath):
            files.append(filepath)

print(f"Found {len(files)} files")


# Load files
all_data = []
for file in files:

    print(f"Loading {file}")

    try:
        df = pd.read_csv(
            file,
            low_memory=False
        )

        df["SourceFile"] = os.path.basename(file)

        all_data.append(df)

    except Exception as e:
        print(f"Error reading {file}: {e}")

if len(all_data) == 0:
    raise Exception("No CSV files were found in the california folder")


# Combine data
combined = pd.concat(
    all_data,
    ignore_index=True
)

print("Rows before filtering:", len(combined))


# Filter data
cleaned = combined[
    (combined["PropertyType"] == "Residential") &
    (
        combined["PropertySubType"]
        == "SingleFamilyResidence"
    )
].copy()

print("Rows after filtering:", len(cleaned))


# Save clean data
cleaned.to_csv(
    OUTPUT_CLEAN,
    index=False
)

print(f"Saved: {OUTPUT_CLEAN}")


# Find column info
summary = []

for col in cleaned.columns:

    missing = round(
        cleaned[col].isna().mean() * 100,
        2
    )

    example = ""

    non_null = cleaned[col].dropna()

    if len(non_null) > 0:
        example = str(non_null.iloc[0])

    summary.append({
        "Column": col,
        "DataType": str(cleaned[col].dtype),
        "MissingPercent": missing,
        "ExampleValue": example
    })

column_df = pd.DataFrame(summary)

column_df.to_csv(
    OUTPUT_COLUMNS,
    index=False
)

print("\nColumns:")
print(cleaned.columns.tolist())
