import pandas as pd
import os


def compare_columns_by_position(file_path, export_to_csv=False):
    # Check if the file exists locally
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    # Load the CSV
    # header=None if your CSV starts immediately with data, otherwise leave default
    df = pd.read_csv(file_path)

    # Group Column A (index 0) and B (index 1) as Dataset 1
    # Group Column D (index 3) and E (index 4) as Dataset 2
    # We use .iloc to select by numeric position
    try:
        # Extract pairs and drop rows where either value in the pair is missing
        set_1 = set(filter(all, zip(df.iloc[:, 0], df.iloc[:, 1])))
        set_2 = set(filter(all, zip(df.iloc[:, 3], df.iloc[:, 4])))
    except IndexError:
        print("Error: The CSV does not have enough columns (Need at least 5 columns: A, B, C, D, E)")
        return

    # Identify unique combinations
    # Found in A+B but not in D+E
    unique_to_left = set_1 - set_2
    # Found in D+E but not in A+B
    unique_to_right = set_2 - set_1

    # NEW: Identify common combinations found in both datasets
    common_in_both = set_1 & set_2

    # Convert results to DataFrames for a clean table view
    df_left = pd.DataFrame(list(unique_to_left), columns=['IP', 'Hostname'])
    df_right = pd.DataFrame(list(unique_to_right), columns=['IP', 'Hostname'])
    df_common = pd.DataFrame(list(common_in_both), columns=['IP', 'Hostname'])

    # Display results
    print("\n" + "╔" + "═" * 48 + "╗")
    print("║ UNIQUE IN Dataset 1 (Not found in Dataset 2)   ║")
    print("╚" + "═" * 48 + "╝")
    if not df_left.empty:
        print(df_left.to_string(index=False))
    else:
        print("No unique combinations found.")

    print("\n" + "╔" + "═" * 48 + "╗")
    print("║ UNIQUE IN Dataset 2 (Not found in Dataset 1)   ║")
    print("╚" + "═" * 48 + "╝")
    if not df_right.empty:
        print(df_right.to_string(index=False))
    else:
        print("No unique combinations found.")

    # NEW: Display common results
    print("\n" + "╔" + "═" * 48 + "╗")
    print("║ COMMON IN BOTH Datasets 1 and 2                ║")
    print("╚" + "═" * 48 + "╝")
    if not df_common.empty:
        print(df_common.to_string(index=False))
    else:
        print("No common combinations found.")

    # NEW: Optional CSV export to local Downloads folder
    if export_to_csv:
        # Get user's Downloads folder path dynamically
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # Ensure the folder exists
        if not os.path.exists(downloads_folder):
            print(f"Error: Downloads folder not found at {downloads_folder}")
            return

        # Export each DataFrame to CSV
        df_left.to_csv(os.path.join(downloads_folder, 'unique_dataset1.csv'), index=False)
        df_right.to_csv(os.path.join(downloads_folder, 'unique_dataset2.csv'), index=False)
        df_common.to_csv(os.path.join(downloads_folder, 'common_both_datasets.csv'), index=False)

        print(f"\nCSVs exported to: {downloads_folder}")


if __name__ == "__main__":
    # Define the Windows file path
    target_file = r'C:\Users\Username\Documents\Compare_Py.csv'  # Adjust to your actual path

    # Run the comparison with CSV export enabled (set to False if you don't want export)
    compare_columns_by_position(target_file, export_to_csv=True)
