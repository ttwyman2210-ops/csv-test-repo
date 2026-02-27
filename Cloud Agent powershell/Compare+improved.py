import pandas as pd
import os

# Block 1: Function to compare datasets and display/export results
def compare_columns_by_position(file_path, export_to_csv=False):
    # Check file existence
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    # Load CSV and extract pairs (drop rows with missing values)
    df = pd.read_csv(file_path)
    try:
        set_1 = set(tuple(row) for row in df.iloc[:, [0, 1]].dropna().values)
        set_2 = set(tuple(row) for row in df.iloc[:, [3, 4]].dropna().values)
    except IndexError:
        print("Error: CSV needs at least 5 columns (A, B, C, D, E)")
        return

    # Compute uniques and commons
    unique_left = set_1 - set_2
    unique_right = set_2 - set_1
    common_both = set_1 & set_2

    # Create DataFrames with section labels for display/export
    sections = {
        'Unique_Dataset1': pd.DataFrame(list(unique_left), columns=['IP', 'Hostname']),
        'Unique_Dataset2': pd.DataFrame(list(unique_right), columns=['IP', 'Hostname']),
        'Common_Both': pd.DataFrame(list(common_both), columns=['IP', 'Hostname'])
    }

    # Block 2: Display results in formatted tables
    def display_section(title, df_section):
        print("\n" + "╔" + "═" * 48 + "╗")
        print(f"║ {title.ljust(46)} ║")
        print("╚" + "═" * 48 + "╝")
        if not df_section.empty:
            print(df_section.to_string(index=False))
        else:
            print("No combinations found.")

    display_section("UNIQUE IN Dataset 1 (Not in Dataset 2)", sections['Unique_Dataset1'])
    display_section("UNIQUE IN Dataset 2 (Not in Dataset 1)", sections['Unique_Dataset2'])
    display_section("COMMON IN BOTH Datasets 1 and 2", sections['Common_Both'])

    # Block 3: Optional combined CSV export to Downloads folder
    if export_to_csv:
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(downloads_folder):
            print(f"Error: Downloads folder not found at {downloads_folder}")
            return

        # Add 'Section' column and concatenate
        for key, df_sec in sections.items():
            df_sec['Section'] = key
        df_combined = pd.concat(sections.values(), ignore_index=True)[['Section', 'IP', 'Hostname']]

        # Export
        export_path = os.path.join(downloads_folder, 'comparison_results.csv')
        df_combined.to_csv(export_path, index=False)
        print(f"\nCombined CSV exported to: {export_path}")


if __name__ == "__main__":
    # Define file path and run (set export_to_csv=True to enable export)
    target_file = r'C:\Users\Username\Documents\Compare_Py.csv'  # Adjust path
    compare_columns_by_position(target_file, export_to_csv=True)
