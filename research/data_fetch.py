import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime


def parse_citibike_xml(xml_content):
    soup = BeautifulSoup(xml_content, "xml")
    contents = soup.find_all("Contents")
    data = []

    for content in contents:
        key = content.find("Key").text

        # Skip non-data files and index.html
        if not key.endswith(".zip") or key == "index.html":
            continue

        # Extract data
        row = {
            "filename": key,
            "last_modified": datetime.strptime(
                content.find("LastModified").text, "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            "size_bytes": int(content.find("Size").text),
            "storage_class": content.find("StorageClass").text,
            "etag": content.find("ETag").text.strip('"'),
        }

        # Calculate size in MB
        row["size_mb"] = round(row["size_bytes"] / (1024 * 1024), 2)

        data.append(row)

    # Create DataFrame
    df = pd.DataFrame(data)

    # Add year-month column for easier analysis
    df["year_month"] = df["filename"].apply(
        lambda x: x.split("-")[0] if "-" in x else None
    )

    # Sort by last_modified date
    df = df.sort_values("last_modified")

    return df


def fetch_and_process_xml(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return parse_citibike_xml(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching XML: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # URL for the XML data
    url = "https://s3.amazonaws.com/tripdata"

    # Process the XML
    df = fetch_and_process_xml(url)

    if df is not None:
        # Display basic information about the dataset
        print("\nDataset Summary:")
        print(f"Total number of files: {len(df)}")
        print(
            f"\nDate range: {df['last_modified'].min()} to {df['last_modified'].max()}"
        )
        print(f"\nTotal data size: {df['size_mb'].sum():,.2f} MB")

        # Display first few rows
        print("\nFirst few rows of the DataFrame:")
        print(df.head())


