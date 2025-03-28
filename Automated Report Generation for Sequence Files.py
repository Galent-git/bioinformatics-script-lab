def generate_sequence_report(input_dir, output_report, file_format="fasta"):
    """
    Generate a CSV report summarizing metrics for all sequence files in a directory.
    
    Metrics include:
      - Number of sequences
      - Average read/sequence length
      - Average GC content
      
    Parameters:
      input_dir: Directory containing sequence files.
      output_report: CSV file path for the report.
      file_format: Format of sequence files ("fasta" or "fastq").
    """
    files = glob.glob(os.path.join(input_dir, f"*{file_format}"))
    report_data = []
    
    for file in files:
        try:
            records = list(SeqIO.parse(file, file_format))
            if not records:
                continue
            num_seqs = len(records)
            lengths = [len(rec.seq) for rec in records]
            avg_length = sum(lengths) / num_seqs
            gc_values = [GC(rec.seq) for rec in records]
            avg_gc = sum(gc_values) / num_seqs
            report_data.append({
                "filename": os.path.basename(file),
                "num_sequences": num_seqs,
                "average_length": round(avg_length, 2),
                "average_gc": round(avg_gc, 2)
            })
            print(f"Processed {file}: {num_seqs} sequences, avg_length={avg_length:.2f}, avg_gc={avg_gc:.2f}")
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    try:
        with open(output_report, "w", newline="") as csvfile:
            fieldnames = ["filename", "num_sequences", "average_length", "average_gc"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in report_data:
                writer.writerow(row)
        print(f"Report written to {output_report}")
    except Exception as e:
        print(f"Error writing report: {e}")
