def extract_subsequence(fasta_file, output_file, pattern=None, start=None, end=None):
    """
    Extract sequences from a FASTA file based on a header pattern or coordinate range.
    
    Parameters:
      fasta_file: Input FASTA file.
      output_file: Destination FASTA file for extracted sequences.
      pattern: (Optional) Regex pattern to filter headers.
      start: (Optional) Start coordinate (1-indexed, inclusive) for subsequence extraction.
      end: (Optional) End coordinate (1-indexed, inclusive) for subsequence extraction.
    
    Behavior:
      If 'pattern' is provided, only sequences with headers matching the pattern are extracted.
      If 'start' and 'end' are provided, the sequence is trimmed to that region.
    """
    extracted_records = []
    try:
        for record in SeqIO.parse(fasta_file, "fasta"):
            # Filter by header pattern if given
            if pattern and not re.search(pattern, record.description):
                continue
            # Extract subsequence if coordinates provided
            if start is not None and end is not None:
                subseq = record.seq[start-1:end]  # convert to 0-index
                record.seq = subseq
                record.description += f" | subsequence: {start}-{end}"
            extracted_records.append(record)
        
        if not extracted_records:
            print("No sequences matched the criteria.")
            return False

        with open(output_file, "w") as out_handle:
            SeqIO.write(extracted_records, out_handle, "fasta")
        print(f"Extracted {len(extracted_records)} sequences to {output_file}")
        return True
    except Exception as e:
        print(f"Error extracting subsequences: {e}")
        return False
