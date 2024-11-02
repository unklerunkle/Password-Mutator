#!/usr/bin/env python3

import argparse
import re

# Function to generate mutated passwords
def mutate_password(password, prepend_list, append_list):
    mutations = []
    
    # Generate mutations with prepend and append options
    for prepend in prepend_list:
        for append in append_list:
            mutated_password = f"{prepend}{password}{append}"
            mutations.append(mutated_password)
    
    return mutations

# Function to generate a list of numbers based on a specified range
def generate_number_range(range_str):
    # Match ranges like "0-99" and "10-50"
    match = re.match(r"(\d+)-(\d+)", range_str)
    if match:
        start = int(match.group(1))
        end = int(match.group(2))
        return [str(i) for i in range(start, end + 1)]
    else:
        raise ValueError(f"Invalid range format: {range_str}")

# Read the input file and process each password
def process_password_file(input_file, output_file, prepend_list, append_list):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            # Strip any whitespace (e.g., newline characters)
            password = line.strip()
            
            # Generate all mutated versions of the current password
            mutated_passwords = mutate_password(password, prepend_list, append_list)
            
            # Write each mutated password to the output file
            for mutated_password in mutated_passwords:
                outfile.write(mutated_password + "\n")
    
    print(f"Mutated passwords saved to {output_file}")

# Main function to handle argument parsing
def main():
    parser = argparse.ArgumentParser(description="Mutate a password wordlist by prepending and/or appending special characters or numbers.")
    
    parser.add_argument("input_file", help="The input file containing the original passwords.")
    parser.add_argument("-o", "--output_file", default="mutated.lst", help="The output file to save the mutated passwords (default: mutated.lst).")
    
    # Options for prepending (-p) and appending (-a) characters or numbers
    parser.add_argument("-p", "--prepend", choices=['special', 'number'], help="Prepend either special characters or numbers.")
    parser.add_argument("-a", "--append", choices=['special', 'number'], help="Append either special characters or numbers.")
    
    # Option for number range if 'number' is chosen for prepend or append
    parser.add_argument("--prepend_range", help="Range of numbers for prepend (e.g., 0-99).")
    parser.add_argument("--append_range", help="Range of numbers for append (e.g., 0-99).")
    
    args = parser.parse_args()

    # Default special characters
    special_characters = ['!', '@', '#', '$', '%', '^', '&', '*']

    # Process prepend option
    if args.prepend == 'special':
        prepend_list = special_characters
    elif args.prepend == 'number' and args.prepend_range:
        prepend_list = generate_number_range(args.prepend_range)
    else:
        prepend_list = ['']  # No prepend if not specified

    # Process append option
    if args.append == 'special':
        append_list = special_characters
    elif args.append == 'number' and args.append_range:
        append_list = generate_number_range(args.append_range)
    else:
        append_list = ['']  # No append if not specified

    # Process the input file and save the mutated passwords
    process_password_file(args.input_file, args.output_file, prepend_list, append_list)

if __name__ == "__main__":
    main()
