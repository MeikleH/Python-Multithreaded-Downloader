# Python Multithreaded Downloader

The Python Multithreaded Downloader is a powerful, versatile script written in Python that facilitates the efficient download of large files from the internet. It optimizes the process by dividing the file into chunks and downloading them simultaneously, drastically reducing the total download time. This tool is particularly effective for downloading large files across slow or unstable networks.

## Key Features

- **Multithreaded Downloading:** Leverages the power of concurrent processing to download file segments.
- **Chunked Downloads:** Breaks down files into manageable pieces, enhancing speed and reliability.
- **Robust Error Handling:** Features a retry mechanism to handle and recover from failures.
- **Real-Time Progress Updates:** Progress bar for each download provides live feedback.
- **Customizable Chunk Sizes:** Allows users to define the number of download segments according to their needs.

## Installation

This script requires Python 3.7 or higher. Python can be downloaded from the [official website](https://www.python.org/downloads/).

After installing Python, the necessary libraries can be installed with the following command:

```bash
pip install requests tqdm
```

## Usage

First, clone the repository:

```bash
git clone https://github.com/MeikleH/Python-Multithreaded-Downloader.git
```

Navigate to the cloned repository:

```bash
cd Python-Multithreaded-Downloader
```

The script can be run from the command line as follows:

```bash
python multithreaded_downloader.py <url> [-s <save_name>] [-c <chunk>]
```

Where:
- `<url>`: The URL of the file to download.
- `<save_name>` (optional): The name under which to save the downloaded file. If not specified, the file name will be extracted from the URL.
- `<chunk>` (optional): The number of chunks to split the download into. The default is 8.

Example:

```bash
python multithreaded_downloader.py https://example.com/largefile.zip -s downloaded_file.zip -c 10
```

## How it Works

- The script first determines the size of the target file and calculates the range for each chunk.
- It then initiates a separate thread for each chunk.
- Each thread is responsible for downloading its respective file segment, with built-in retries to handle failures.
- The progress of each chunk download is represented via a dynamic progress bar.

## Contributing

We welcome pull requests! For major changes, please open an issue first to discuss the proposed modification.
