# Trello Card Attachments Downloader (TCAD)

<p align="center">
  <img src="https://github.com/SeyedEhsanHosseini/tcad/blob/main/assets/TCAD.png">
</p>

### Download all the attachments from a Trello card in a batch.

## Introduction

This Python script downloads all the attachments from a Trello card in a batch, rather than downloading them individually. You can also choose to delete the attachments from the card after downloading them (you can make an exception for the last N attachments).

## How to Use

1. Fill in the API Token field and start the download process by choosing a JSON file.
2. Choose a JSON file that contains the Trello card data. Make sure that the file is in the correct format (JSON).
3. The progress bar shows the progress of the download process, and the output box displays messages about the status of each download.
4. Once the download is completed, you will find all the downloaded attachments stored in the 'attachments' directory.

## How to Contribute

If you want to contribute to this project, you can fork the repository and submit a pull request with your changes.

## Dependencies

This script requires the following dependencies:
- python3.9
- PyQt5
- requests


You can install these dependencies using pip:

```
pip install -r requirements.txt
```

## License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.
