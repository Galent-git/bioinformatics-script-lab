def sort_and_rename_files(input_dir, output_dir, criteria="header", file_extension=None):
    """
    Scan the input directory for FASTA/FASTQ files and rename them based on content.
    
    Parameters:
      input_dir: Directory containing input files.
      output_dir: Destination directory for sorted/renamed files.
      criteria: Renaming rule; "header" uses the first word from the first record's header.
      file_extension: Filter by extension (e.g. ".fasta" or ".fastq"); if None, process all.
    
    Behavior:
      Reads each file, extracts the sample ID (or uses the original name), and copies it 
      to output_dir with the new name.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Set file search pattern
    pattern = os.path.join(input_dir, f"*{file_extension}") if file_extension else os.path.join(input_dir, "*")
    files = glob.glob(pattern)
    
    for file_path in files:
        # Process only FASTA/FASTQ files
        if not (file_path.endswith((".fasta", ".fa", ".fastq", ".fq"))):
            continue
        try:
            # Use "fasta" format if file extension is fasta/fa; else assume fastq
            fmt = "fasta" if file_path.endswith((".fasta", ".fa")) else "fastq"
            records = list(SeqIO.parse(file_path, fmt))
            if not records:
                print(f"No records found in {file_path}. Skipping.")
                continue
            # Use header criteria: first word of the header (strip leading '>')
            if criteria == "header":
                header = records[0].description
                sample_id = header.split()[0].lstrip(">")
            else:
                sample_id = os.path.splitext(os.path.basename(file_path))[0]
            # Create new filename and copy the file
            ext = os.path.splitext(file_path)[1]
            new_filename = f"{sample_id}{ext}"
            new_path = os.path.join(output_dir, new_filename)
            shutil.copy(file_path, new_path)
            print(f"Copied {file_path} -> {new_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
