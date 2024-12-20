import json
import pandas as pd
import matplotlib.pyplot as plt

# Load data from the JSON file
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Analyze the presence of Privacy Policy and DNSMPI links
def analyze_link_presence(data):
    total_sites = len(data)
    privacy_policy_count = sum(1 for site in data if site.get('privacy_policy'))
    dnsmpi_count = sum(1 for site in data if site.get('dnsmpi_links') and site['dnsmpi_links'] is not None)

    # Calculate percentages
    privacy_policy_percentage = (privacy_policy_count / total_sites) * 100
    dnsmpi_percentage = (dnsmpi_count / total_sites) * 100
    both_count = sum(1 for site in data if site.get('privacy_policy') and site.get('dnsmpi_links') and site['dnsmpi_links'] is not None)
    both_percentage = (both_count / total_sites) * 100

    # Create a summary DataFrame
    summary = pd.DataFrame({
        'Category': ['Privacy Policy', 'DNSMPI Link', 'Both'],
        'Count': [privacy_policy_count, dnsmpi_count, both_count],
        'Percentage': [privacy_policy_percentage, dnsmpi_percentage, both_percentage]
    })

    return summary, total_sites

# Save the summary to a text file
def save_summary_to_txt(summary, total_sites, output_file="RQ2_link_presence_summary.txt"):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Total Websites Analyzed: {total_sites}\n")
        f.write("=" * 50 + "\n")
        f.write(f"{'Category':<20}{'Count':<10}{'Percentage':>10}\n")
        f.write("=" * 50 + "\n")
        for _, row in summary.iterrows():
            f.write(f"{row['Category']:<20}{row['Count']:<10}{row['Percentage']:>9.2f}%\n")
    print(f"Summary saved to {output_file}")

# Visualize and save the results
def visualize_and_save_results(summary, output_file="RQ2_link_presence_chart.png"):
    plt.bar(summary['Category'], summary['Percentage'], color=['blue', 'orange', 'green'])
    plt.title('Percentage of Websites with Privacy Policy and DNSMPI Links')
    plt.ylabel('Percentage')
    plt.xlabel('Link Type')
    plt.tight_layout()
    plt.savefig(output_file)  # Save the plot as an image file
    print(f"Chart saved to {output_file}")
    plt.show()

# Main function
def main():
    input_file = 'scraped_data.json'  # Replace with your JSON file
    data = load_data(input_file)
    summary, total_sites = analyze_link_presence(data)

    # Save summary and visualize results
    save_summary_to_txt(summary, total_sites, "RQ2_link_presence_summary.txt")
    visualize_and_save_results(summary, "RQ2_link_presence_chart.png")

if __name__ == "__main__":
    main()

