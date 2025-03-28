def merge_or_split_files(input_files, output_dir, mode="merge", split_count=1000, file_format="fasta"):
    """
    Merge multiple sequence files into one, or split a large file into smaller ones.
    
    Parameters:
      input_files: For "merge" mode, a list of file paths; for "split" mode, a single file path.
      output_dir: Directory to save the merged or split files.
      mode: "merge" or "split".
      split_count: Number of sequences per file (for split mode).
      file_format: Format of sequence files ("fasta" or "fastq").
    """
    os.makedirs(output_dir, exist_ok=True)
    if mode == "merge":
        merged_records = []
        for file in input_files:
            try:
                records = list(SeqIO.parse(file, file_format))
                merged_records.extend(records)
                print(f"Added {len(records)} records from {file}")
            except Exception as e:
                print(f"Error reading {file}: {e}")
        merged_file = os.path.join(output_dir, f"merged.{file_format}")
        with open(merged_file, "w") as out_handle:
            SeqIO.write(merged_records, out_handle, file_format)
        print(f"Merged {len(merged_records)} sequences into {merged_file}")
    elif mode == "split":
        # If input_files is a list, take the first element.
        file = input_files if isinstance(input_files, str) else input_files[0]
        records = list(SeqIO.parse(file, file_format))
        total_records = len(records)
        print(f"Total records in {file}: {total_records}")
        num_files = (total_records // split_count) + (1 if total_records % split_count != 0 else 0)
        for i in range(num_files):
            split_records = records[i*split_count : (i+1)*split_count]
            split_file = os.path.join(output_dir, f"split_{i+1}.{file_format}")
            with open(split_file, "w") as out_handle:
                SeqIO.write(split_records, out_handle, file_format)
            print(f"Wrote {len(split_records)} records to {split_file}")
