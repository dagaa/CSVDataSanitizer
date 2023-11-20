import pandas as pd
import hashlib
import inquirer

def anonymize(value):
    """Anonymize a string using a hash function."""
    return hashlib.sha256(value.encode()).hexdigest()[:10]

def select_columns(df):
    """Prompt user to select columns to anonymize."""
    questions = [
        inquirer.Checkbox('columns',
                          message="Select columns to anonymize",
                          choices=list(df.columns),
                          ),
    ]
    answers = inquirer.prompt(questions)
    return answers['columns']

# Prompt for input and output file names
input_file = input("Enter the name of the input CSV file: ")
output_file = input("Enter the name of the output CSV file: ")

# Load the CSV data with a different encoding
try:
    df = pd.read_csv(input_file, delimiter=';', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(input_file, delimiter=';', encoding='ISO-8859-1')

# Let the user select columns to anonymize
columns_to_anonymize = select_columns(df)

# Anonymize selected columns
for column in columns_to_anonymize:
    df[column] = df[column].apply(anonymize)

# Save the modified data back to a new CSV file
df.to_csv(output_file, sep=';', index=False)

print(f"Anonymization complete. Data saved to '{output_file}'")
