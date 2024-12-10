import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load data from the JSON file produced by crawler.py
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Analyze DNSMPI link patterns
def analyze_dnsmpi_patterns(data):
    dnsmpi_patterns = []

    for site in data:
        # Safely get dnsmpi_links or use an empty list if None
        dnsmpi_links = site.get('dnsmpi_links', [])
        if dnsmpi_links is None:  # Additional safeguard
            dnsmpi_links = []

        for link in dnsmpi_links:
            # Extract the 'text' field safely
            link_text = link.get('text', None)
            if link_text:
                dnsmpi_patterns.append(link_text.lower())  # Normalize to lowercase for consistency

    # Count the occurrences of each pattern
    pattern_counts = Counter(dnsmpi_patterns)

    # Convert to DataFrame for easier analysis and reset index
    pattern_df = pd.DataFrame(pattern_counts.items(), columns=['Pattern', 'Frequency'])
    pattern_df.sort_values(by='Frequency', ascending=False, inplace=True)
    pattern_df.reset_index(drop=True, inplace=True)  # Reset index for proper ranking

    return pattern_df

# Save the summary table to a plain text file
def save_summary_to_txt(pattern_df, output_file="RQ1_dnsmpi_patterns_summary.txt"):
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"{'Rank':<6}{'Pattern':<60}{'Frequency':>10}\n")
        f.write("=" * 80 + "\n")
        
        # Write rows
        for idx, row in pattern_df.iterrows():
            pattern = row['Pattern'][:57] + "..." if len(row['Pattern']) > 57 else row['Pattern']
            f.write(f"{idx + 1:<6}{pattern:<60}{row['Frequency']:>10}\n")
        
    print(f"Summary saved to {output_file}")

# Visualize and save the results
def visualize_and_save_patterns(pattern_df, output_file="RQ1_dnsmpi_patterns_chart.png"):
    top_patterns = pattern_df.head(10)
    plt.barh(top_patterns['Pattern'], top_patterns['Frequency'])
    plt.xlabel('Frequency')
    plt.ylabel('DNSMPI Tag Pattern')
    plt.title('Top 10 DNSMPI Tag Patterns')
    plt.gca().invert_yaxis()  # Reverse order for readability
    plt.tight_layout()
    plt.savefig(output_file)  # Save the plot as an image file
    print(f"Chart saved to {output_file}")
    plt.show()

# Main function
def main():
    input_file = 'scraped_data.json'  # Replace with your JSON file
    data = load_data(input_file)
    pattern_df = analyze_dnsmpi_patterns(data)

    # Save table and visualize results
    save_summary_to_txt(pattern_df, "RQ1_dnsmpi_patterns_summary.txt")
    visualize_and_save_patterns(pattern_df, "RQ1_dnsmpi_patterns_chart.png")

if __name__ == "__main__":
    main()

