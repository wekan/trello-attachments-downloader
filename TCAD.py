import json, os, requests, random, string, configparser, time, urllib.parse

from PyQt5.QtWidgets import *

from PyQt5.QtGui import QDesktopServices

from PyQt5.QtCore import QThread, pyqtSignal, QUrl, QSettings

class DownloadThread(QThread):
    """Thread class for downloading attachments"""
    progress_updated = pyqtSignal(int)
    message_updated = pyqtSignal(str)

    def __init__(self, urls, Card_name, api_key, api_token, main_window):
        super().__init__()
        self.urls = urls
        self.Card_name = Card_name
        self.api_key = api_key
        self.api_token = api_token
        self.main_window = main_window  # Store a reference to the MainWindow instance

    def remove_forbidden_chars(self, directory_name):
        # List of forbidden characters for Windows, Linux, and Mac OS
        forbidden_chars = ['/', '\0', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=',
                       '{', '}', '[', ']', ',', ';', "'", '"', '<', '>', '?', '`', '~', '|']

        # Check if any forbidden characters are present in the directory name
        for char in forbidden_chars:
            if char in directory_name:
                # Remove the forbidden character from the directory name
                directory_name = directory_name.replace(char, '')

        return directory_name

    def run(self):
        dir_name = 'attachments'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        
        sub_dir = self.Card_name
        sub_dir = self.remove_forbidden_chars(sub_dir)
        sub_dir_path = os.path.join(dir_name, sub_dir)
        if not os.path.exists(sub_dir_path):
            os.mkdir(sub_dir_path)

        num_urls = len(self.urls)
        keep_count = min(num_urls, self.main_window.num_attachments.value())   # calculate number of URLs to keep
        for i, url in enumerate(self.urls):
            try:
                headers = {
                    "Authorization": f"OAuth oauth_consumer_key=\"{self.api_key}\", oauth_token=\"{self.api_token}\""
                }
                response = requests.get(url, headers=headers)

                filename = os.path.basename(url)

                if filename == urllib.parse.quote(filename, safe=':/'):
                    decoded_filename = urllib.parse.unquote(filename)
                else:
                    decoded_filename = filename

                if len(decoded_filename) > 150:
                    file_extension = os.path.splitext(decoded_filename)[1]
                    enhanced_filename = decoded_filename[:150 - len(file_extension)] + file_extension
                else:
                    enhanced_filename = decoded_filename

                new_filename = f"{sub_dir}_{i+1}_{enhanced_filename}"
                file_path = os.path.join(sub_dir_path, new_filename)
                
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                message = f"Downloaded {url} to {file_path}"
                
                # Save API credentials if checkbox is checked
                if self.main_window.delete_attachments.isChecked():  
                
                    delete_message = ""
                    # Delete the attachment for URLs after the first N
                    if i >= keep_count:

                        # Pause for a short duration before sending the next request
                        time.sleep(0.25)

                        delete_url = url[:url.find('/download')]  # Remove everything after '/download'
                        query = {
                            'key': self.api_key,
                            'token': self.api_token
                        }
                        delete_response = requests.delete(delete_url, params=query)
                        delete_message = f"Deleted {url}"

            except Exception as e:
                message = f"Error downloading {url}: {e}"

            self.message_updated.emit(message)
            
            if self.main_window.delete_attachments.isChecked():  

                self.message_updated.emit(delete_message)

            # Update progress bar
            self.progress_updated.emit(i+1)

        self.message_updated.emit("All attachments downloaded and stored in the 'attachments' directory.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api_key = ''
        self.api_token = ''

        central_widget = QWidget(self)

        # Create layout for main window
        main_layout = QVBoxLayout()

        #label = QLabel("1) From https://trello.com/app-key 'Personal Key':")
        #main_layout.addWidget(label)

        # Create hyperlink button and add to layout
        #button_layout = QHBoxLayout()
        #button = QPushButton("Don't have a token? Click here to get one.")
        #button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&key=0d15c286960fdaa9fec3df41c0abb6f5")))
        #button_layout.addWidget(button)
        #main_layout.addLayout(button_layout)

        # Create input field for API key
        api_key_layout = QVBoxLayout()
        api_key_layout.addWidget(QLabel("1) Personal Key, from https://trello.com/app-key"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        api_key_layout.addWidget(self.api_key_input)
        main_layout.addLayout(api_key_layout)

        # Create input field for API token
        api_token_layout = QVBoxLayout()
        api_token_layout.addWidget(QLabel("2) Personal Token, from https://trello.com/app-key, below Personal Key, you can manually generate a 'Token' <= Click"))
        self.api_token_input = QLineEdit()
        self.api_token_input.setEchoMode(QLineEdit.Password)
        api_token_layout.addWidget(self.api_token_input)
        main_layout.addLayout(api_token_layout)

        # Create save checkbox
        #self.save_checkbox = QCheckBox("Save API credentials")
        #main_layout.addWidget(self.save_checkbox)

        # Delete Attachments checkbox
        #self.delete_attachments = QCheckBox("Delete all attachments from card after download. (Except last")
        #self.num_attachments = QSpinBox()
        #self.num_attachments.setEnabled(False)
        #self.num_attachments.setFixedWidth(45)

        # Connect the checkbox and the spinbox
        #self.delete_attachments.stateChanged.connect(lambda state: self.num_attachments.setEnabled(state))
        
        #num_attachments_layout = QHBoxLayout()

        #num_attachments_layout.addWidget(self.delete_attachments)
        #num_attachments_layout.addWidget(self.num_attachments)
        #num_attachments_layout.addWidget(QLabel("attachments.)"))
        #num_attachments_layout.addStretch()  # Add a stretch to the right
  
        #main_layout.insertLayout(main_layout.indexOf(self.num_attachments), num_attachments_layout)

        # Create a Choose button and add to layout
        button = QPushButton("3) Choose a Trello JSON file, then downloading to attachments directory starts")
        button.clicked.connect(self.download_attachments)
        main_layout.addWidget(button)

        # Create progress bar to show progress
        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        # Create text box to show output
        self.output_textbox = QTextEdit()
        self.output_textbox.setReadOnly(True)

        # Create layout for output text box
        output_layout = QVBoxLayout()
        output_layout.addWidget(QLabel("Output:"))
        output_layout.addWidget(self.output_textbox)

        # Combine main and output layouts into a single layout
        combined_layout = QVBoxLayout()
        combined_layout.addLayout(main_layout)
        combined_layout.addLayout(output_layout)

        central_widget.setLayout(combined_layout)
        self.setCentralWidget(central_widget)

        # Set maximum width of central widget equal to screen width
        screen_size = QDesktopWidget().screenGeometry(-1)
        central_widget.setMaximumWidth(int(screen_size.width() / 2))
        central_widget.setMinimumWidth(int(screen_size.width() / 2))

       
        # Load saved credentials from QSettings
        #settings = QSettings("Trello-PowerUps", "TCAD")
        #self.api_token = settings.value('api_token')
        #if self.api_token:
        #    self.api_token_input.setText(self.api_token)
        #
        #self.show()

    def __del__(self):
        self.download_thread.quit()
        self.download_thread.wait()
            
    def download_attachments(self):
        # Save API credentials in QSettings if checkbox is checked
        #if self.save_checkbox.isChecked():
        #    settings = QSettings("Trello-PowerUps", "TCAD")
        #    settings.setValue('api_token', self.api_token_input.text())

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)", options=options)

        if file_name:
            # Update button label
            button = self.sender()
            button.setText("Download started. Please wait...")

            with open(file_name, encoding="utf8") as f:
                json_data = json.load(f)

            urls = extract_urls_from_json(json_data)
            Card_name = json_data['name']

            total_urls = len(urls)

            api_key = self.api_key
            api_token = self.api_token_input.text()

            self.progress_bar.setMaximum(100)
            self.progress_bar.setValue(0)

            self.download_thread = DownloadThread(urls, Card_name, api_key, api_token, self)
            self.download_thread.progress_updated.connect(lambda d: self.progress_bar.setValue(int((d / total_urls) * 100)))
            self.download_thread.message_updated.connect(self.output_textbox.append)
            self.download_thread.finished.connect(lambda: button.setText("Done!"))
            self.download_thread.start()
            
def extract_urls_from_json(json_data):
    urls = []
    for item in json_data['actions']:
        attachment = item['data'].get('attachment')
        if attachment and 'url' in attachment:
            urls.append(attachment['url'])

    return urls  # Return the list of URLs


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
