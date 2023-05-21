# Import necessary libraries
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from tqdm import tqdm  # For progress bar
import argparse
import os


# Function to calculate divisional ranges
def calc_divisional_range(filesize, chunk=8):
    step = filesize // chunk  # Calculate step size
    arr = list(range(0, filesize, step))  # Create list with step size
    result = []  # Store the results
    for i in range(len(arr) - 1):
        s_pos, e_pos = arr[i], arr[i + 1] - 1  # Calculate start and end positions
        result.append([s_pos, e_pos])  # Append to the result
    result[-1][-1] = filesize - 1  # Adjust the last end position
    return result


# Function to create session with retry strategy
def create_session():
    retry_strategy = Retry(
        total=3,  # Total number of retries
        backoff_factor=1,  # Backoff factor for retries
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
        allowed_methods=["HEAD", "GET", "OPTIONS"]  # Allow these methods to be retried
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)  # Create an adapter with the retry strategy
    session = requests.Session()  # Create a session
    session.mount("https://", adapter)  # Use the adapter for https requests
    session.mount("http://", adapter)  # Use the adapter for http requests
    return session


# Function to download a range of bytes
def range_download(session, url, save_name, s_pos, e_pos, pbar=None):
    headers = {"Range": f"bytes={s_pos}-{e_pos}"}  # Set the range header
    try:
        res = session.get(url, headers=headers, stream=True)  # Get the resource
        res.raise_for_status()  # Raise an exception if the status code is not ok
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return
    try:
        with open(save_name, "wb") as f:  # Create the file if it doesn't exist
            pass
        with open(save_name, "rb+") as f:  # Open the file in binary mode for reading and writing
            f.seek(s_pos)  # Go to the start position
            for chunk in res.iter_content(chunk_size=64 * 1024):  # Iterate over the content in chunks
                if chunk:  # If there is a chunk
                    f.write(chunk)  # Write it to the file
                    if pbar is not None:  # If a progress bar is provided
                        pbar.update(len(chunk))  # Update the progress bar
    except IOError as e:
        print(f"File write error: {e}")


# Function to get file size
def get_filesize(session, url):
    filesize = 0
    try:
        res = session.head(url)  # Get the headers of the URL
        res.raise_for_status()  # Raise an exception if the status code is not ok
        filesize = int(res.headers.get('Content-Length', 0))  # Get the file size from the headers
    except requests.exceptions.RequestException:
        try:
            res = session.get(url, stream=True)  # Get the resource, but don't download yet
            res.raise_for_status()  # Raise an exception if the status code is not ok
            filesize = int(res.headers.get('Content-Length', 0))  # Get the file size from the headers
            res.close()  # Close the connection
        except requests.exceptions.RequestException:
            pass
    return filesize


# Main function
def main(url, save_name=None, chunk=8):
    if save_name is None:
        save_name = os.path.basename(url)  # Get the file name from the URL
        if '?' in save_name:
            save_name = save_name[:save_name.index('?')]  # Remove query string from the file name

    session = create_session()  # Create a session

    filesize = get_filesize(session, url)  # Get the file size

    if filesize == 0:  # If the file size is zero
        print("Content-Length header is missing or not an integer.")
        return

    divisional_ranges = calc_divisional_range(filesize, chunk)  # Calculate the divisional ranges

    # Create a progress bar
    with tqdm(total=filesize, unit='B', unit_scale=True, desc=save_name) as pbar:
        with ThreadPoolExecutor() as p:  # Create a ThreadPoolExecutor
            futures = [p.submit(range_download, session, url, save_name, s_pos, e_pos, pbar) for s_pos, e_pos in
                       divisional_ranges]  # Submit the tasks to the executor
            for future in as_completed(futures):  # Iterate over the futures as they complete
                try:
                    future.result()  # Get the result of the future, raising an exception if the task raised one
                except Exception as e:  # If an exception was raised
                    print(f"Download task failed with error: {e}")  # Print the exception


# If this script is being run directly (not imported)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a file in chunks.")
    parser.add_argument("url",
                        help="The URL of the file to download.")
    parser.add_argument("-s", "--save_name", default=None,
                        help="The name of the file to save the download as. Default: extract from the url.")
    parser.add_argument("-c", "--chunk", type=int, default=8,
                        help="The number of chunks to split the download into. Default: 8.")
    args = parser.parse_args()

    main(args.url, args.save_name, args.chunk)
