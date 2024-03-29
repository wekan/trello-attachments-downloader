# Trello Card Attachments Downloader (TCAD)

- Originally from https://github.com/SeyedEhsanHosseini/tcad
- xet7 changed:
  - UI simpler: Only necessary features. Clearer steps.
  - Not require any 3rd party anymore.

### Download all the attachments from a Trello card in a batch.

## Introduction

This Python script downloads all the attachments from a Trello card in a batch, rather than downloading them individually. You can also choose to delete the attachments from the card after downloading them (you can make an exception for the last N attachments).

## How to Use

1. Add `Personal Key` and below it manually created `Token`
2. Click button to select Trello JSON file. Then downloading starts to `attachments` directory.

## How to Contribute

If you want to contribute to this project, you can fork the repository and submit a pull request with your changes.

## Dependencies

This script requires the following dependencies:
- python3.9
- PyQt5
- requests

### pip

```
pip install -r requirements.txt

python3 TCAD.py
```

### Debian

```
sudo apt -y install python3-installer python3-requests python-pyqt5

python3 TCAD.py
```

### Fedora

```
sudo dnf -y install python3-installer python3-requests python3-pyqt5-sip

python3 TCAD.py
```

## License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.
