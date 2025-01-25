import toml
import subprocess
import logging
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.popup import Popup
import threading

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

config = toml.load("config.toml")
REMOTE = config["paths"]["remote"]
LOCAL = config["paths"]["local"]

def execute_rsync_download(remote, local):
    if not remote.endswith('/'):
        remote += '/'
    logging.debug(f"Executing rsync download from {remote} to {local}")
    rsync_command = [
            "rsync",
            "-avz",
            remote,
            local
        ]
    process = subprocess.Popen(rsync_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def execute_rsync_upload(local, remote):
    if not local.endswith('/'):
        local += '/'
    logging.debug(f"Executing rsync upload from {local} to {remote}")
    rsync_upload_command = [
            "rsync",
            "-avz",
            "--update", # Only copy files that are newer on the source
            local,
            remote
        ]
    process = subprocess.Popen(rsync_upload_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

class SyncApp(App):
    def build(self):
        self.output = TextInput(size_hint_y=None, height=400, readonly=True) # Text output
        layout = BoxLayout(orientation='vertical')
        
        download_button = Button(
            text="Download Saves", # Button text 
            size_hint_y=None, # Height is fixed
            height=50, # Height is 50 pixels
            size_hint_x=None, 
            width=400
            )
        download_button.bind(on_press=self.on_download_button_press)
        layout.add_widget(download_button)
        
        upload_button = Button(text="Upload Saves", size_hint_y=None, height=50)
        upload_button.bind(on_press=self.on_upload_button_press)
        layout.add_widget(upload_button)
        
        sync_button = Button(text="Sync All", size_hint_y=None, height=50)
        sync_button.bind(on_press=self.on_sync_button_press)
        layout.add_widget(sync_button)
        
        scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        scroll_view.add_widget(self.output)
        layout.add_widget(scroll_view)
        
        return layout

    def on_download_button_press(self, instance):
        logging.debug("Download button pressed")
        threading.Thread(target=self.run_download_saves).start()

    def on_upload_button_press(self, instance):
        logging.debug("Upload button pressed")
        threading.Thread(target=self.run_upload_saves).start()

    def on_sync_button_press(self, instance):
        logging.debug("Sync button pressed")
        threading.Thread(target=self.run_sync_saves).start()

    def run_download_saves(self):
        self.update_output("Starting download...\n")
        try:
            process = execute_rsync_download(REMOTE, LOCAL)
            for line in process.stdout:
                self.update_output(line)
                logging.debug(line.strip())
            process.wait()
            if process.returncode == 0:
                self.update_output("Download completed successfully.\n")
                logging.debug("Download completed successfully")
            else:
                self.update_output("Download failed.\n")
                logging.error("Download failed")
        except Exception as e:
            self.update_output(f"Error: {e}\n")
            logging.error(f"Error: {e}")

    def run_upload_saves(self):
        self.update_output("Starting upload...\n")
        try:
            process = execute_rsync_upload(LOCAL, REMOTE)
            for line in process.stdout:
                self.update_output(line)
                logging.debug(line.strip())
            process.wait()
            if process.returncode == 0:
                self.update_output("Upload completed successfully.\n")
                logging.debug("Upload completed successfully")
            else:
                self.update_output("Upload failed.\n")
                logging.error("Upload failed")
        except Exception as e:
            self.update_output(f"Error: {e}\n")
            logging.error(f"Error: {e}")

    def run_sync_saves(self):
        self.update_output("Starting sync...\n")
        logging.debug("Starting sync")
        self.run_download_saves()
        self.run_upload_saves()
        self.update_output("Sync completed.\n")
        logging.debug("Sync completed")

    def update_output(self, text):
        Clock.schedule_once(lambda dt: self.output.insert_text(text))

if __name__ == "__main__":
    SyncApp().run()

