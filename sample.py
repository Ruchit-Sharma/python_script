import os
import base64
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from docx import Document  

ES_URL = "http://localhost:9200"
INDEX_NAME = "index1"
PIPELINE_ID = "cisco_pdf"

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            self.process_pdf(event.src_path)
        elif event.src_path.endswith(".docx"):
            self.process_word(event.src_path)

    def process_pdf(self, pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read()).decode('utf-8')
            document = {
                "data": encoded_string
            }
            doc_id = os.path.basename(pdf_path).split('.')[0]
            response = requests.put(
                f"{ES_URL}/{INDEX_NAME}/_doc/{doc_id}?pipeline={PIPELINE_ID}",
                json=document
            )
            if response.status_code == 201:
                print(f"Successfully indexed {pdf_path}")
            else:
                print(f"Failed to index {pdf_path}: {response.text}")

    def process_word(self, word_path):
        with open(word_path, "rb") as word_file:
            encoded_string = base64.b64encode(word_file.read()).decode('utf-8')
            document = {
                "data": encoded_string
            }
            doc_id = os.path.basename(word_path).split('.')[0]
            response = requests.put(
                f"{ES_URL}/{INDEX_NAME}/_doc/{doc_id}?pipeline={PIPELINE_ID}",
                json=document
            )
            if response.status_code == 201:
                print(f"Successfully indexed {word_path}")
            else:
                print(f"Failed to index {word_path}: {response.text}")

if __name__ == "__main__":
    path = "C:/Users/yogya/OneDrive/Desktop/PDFs"
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"Monitoring {path} for new files...")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
