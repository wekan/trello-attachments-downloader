# Trello Card Attachments Downloader (TCAD)

<img src="https://github.com/wekan/trello-attachments-downloader/blob/main/assets/screenshot-win3.png?raw=true" width="100%" alt="Screenshot" />

## Introduction

This Python script downloads all the attachments from a Trello board in a batch, rather than downloading them individually.

Issue about importing from Trello to WeKan: https://github.com/wekan/wekan/issues/4877#issuecomment-2026572349

- Originally from https://github.com/SeyedEhsanHosseini/tcad
- xet7 changed:
  - UI simpler: Only necessary features. Clearer steps.
  - Not require any 3rd party anymore.
  - Added install info for various operating systems.

## How to Use

1. Add `Personal Key` and below it manually created `Token`
2. Click button to select Trello JSON file. Then downloading starts to `attachments` directory.
3. For additional Trello JSON files, click DONE button, and load next Trello JSON files. Then downloading attachments of that board starts.

## How to Contribute

If you want to contribute to this project, you can fork the repository and submit a pull request with your changes.

## Dependencies

This script requires the following dependencies:
- python3.9
- PyQt5
- requests

### Windows

```
choco install python3 git

git clone https://github.com/wekan/trello-attachments-downloader

cd trello-attachments-downloader

pip install requests pyinstaller PyQt5

python TCAD.py
```

### Debian/Ubuntu/Mint

```
sudo apt -y install python3-installer python3-requests python-pyqt5 git

git clone https://github.com/wekan/trello-attachments-downloader

cd trello-attachments-downloader

python3 TCAD.py
```

### Fedora

```
sudo dnf -y install python3-installer python3-requests python3-pyqt5-sip git

git clone https://github.com/wekan/trello-attachments-downloader

cd trello-attachments-downloader

python3 TCAD.py
```

### Mac

```
brew install python-idna python-requests pyqt@5

git clone https://github.com/wekan/trello-attachments-downloader

cd trello-attachments-downloader

python3 TCAD.py
```

## License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.
