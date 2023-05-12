# Python Multithreaded Downloader

Python Multithreaded Downloader is a utility script written in Python for downloading large files from the internet. It splits the file into chunks and downloads them concurrently, significantly reducing the overall download time. This tool is suitable for downloading large files over slow or unreliable networks.

## Features

- Multithreaded downloading.
- Downloading files in chunks.
- Retries on failure.
- Progress bar for each download.
- Adjustable number of download chunks.

## Installation

To use the script, you need Python 3.7 or above. You can download Python from [here](https://www.python.org/downloads/).

After installing Python, you also need to install the required libraries. You can do this by running the following command:

```bash
pip install requests tqdm
```

## Usage

Clone the repository:

```
git clone https://github.com/MeikleH/Python-Multithreaded-Downloader.git
```

Navigate to the cloned repository:

```
cd Python-Multithreaded-Downloader
```

You can run the script from the command line as follows:

```bash
python multithreaded_downloader.py <url> [-s <save_name>] [-c <chunk>]
```

Where:
- `<url>` is the URL of the file to download.
- `<save_name>` (optional) is the name of the file to save the download as. If not provided, the file name will be extracted from the URL.
- `<chunk>` (optional) is the number of chunks to split the download into. The default is 8.

Example:

```bash
python multithreaded_downloader.py https://example.com/largefile.zip -s downloaded_file.zip -c 10
```

## Functionality

- The script first calculates the size of the file to be downloaded and the ranges for each chunk.
- It then creates a separate thread for each chunk.
- Each thread downloads its respective chunk of the file, retrying on failure.
- The progress of each chunk is shown in a progress bar.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
