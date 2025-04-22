# [ Script ] Create File : Different ( Before VS After )

import csv

input_file1_path = ""
input_file2_path = ""

output_file_path = f"different_{input_file1_path}_{input_file2_path}.csv"

def create_file_different(input_file1_path, input_file2_path) :

    with open(input_file1_path, 'r', encoding='utf-8') as f1 :
        lines1 = set(line.strip() for line in f1 if line.strip())

    with open(input_file2_path, 'r', encoding='utf-8') as f2 :
        lines2 = set(line.strip() for line in f2 if line.strip())

    only_in_file1 = sorted(lines1 - lines2)
    only_in_file2 = sorted(lines2 - lines1)

    with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file :
        writer = csv.writer(output_file)
        writer.writerow(["Where", "What"])

        for value in only_in_file1 :
            writer.writerow([f"In - Input File #1", value])

        for value in only_in_file2 :
            writer.writerow([f"IN - Input File #2", value])

    print(f"[ DEBUG ] Path : {output_file_path}")

create_file_different(input_file1_path, input_file2_path)
