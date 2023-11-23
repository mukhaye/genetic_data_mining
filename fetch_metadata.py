from Bio import Entrez

def fetch_metadata(accession_numbers):
    Entrez.email = "euginemukhaye17@gemail.com"  # Replace with your email address
    try:
        handle = Entrez.efetch(db="nucleotide", id=accession_numbers, retmode="xml")
        records = Entrez.read(handle)
        return records
    except Exception as e:
        print(f"Error fetching metadata for accession numbers {accession_numbers}: {e}")
        return []

def extract_metadata(record):
    try:
        versioned_accession = record["GBSeq_accession-version"]
        organism = record["GBSeq_organism"]
        description = record["GBSeq_definition"]
        
        # Check if 'GBSeq_source-country' field exists before extracting its value
        features = record.get("GBSeq_feature-table", [])
        country = "N/A"

        for feature in features:
            if feature.get("GBFeature_key") == "source":
                qualifiers = feature.get("GBFeature_quals", [])
                for qualifier in qualifiers:
                    if qualifier.get("GBQualifier_name") == "country":
                        country = qualifier.get("GBQualifier_value", "N/A")
        date = record["GBSeq_create-date"]
        
        # Add more fields as needed

        return f"{versioned_accession} {description}\t{country} {date}"  # Return the desired metadata format
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None

def main():
    # Replace 'full/path/to/accession_numbers.txt' with the actual path to your file
    file_path = '/mnt/c/Users/SA/OneDrive/Desktop/CCHFV/Bioinfor_analysis/accession_numbers.txt'

    with open(file_path, "r") as file:
        accession_numbers = [line.strip() for line in file]

    metadata_table = []

    for accession_number in accession_numbers:
        try:
            records = fetch_metadata(accession_number)
            for record in records:
                metadata = extract_metadata(record)
                if metadata:
                    metadata_table.append(metadata)
        except Exception as e:
            print(f"Error processing accession number {accession_number}: {e}")

    # Print or save the metadata table as needed
    with open('metadata_output.txt', 'w') as output_file:
        for metadata in metadata_table:
            output_file.write(metadata + "\n")

if __name__ == "__main__":
    main()
