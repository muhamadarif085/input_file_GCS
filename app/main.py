from google.cloud import storage
import json
import os
import sys
import dotenv
from pydantic import BaseModel
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

# Get environment variables
config = dotenv.dotenv_values()

class Upload(BaseModel):
    file: UploadFile

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
    <head>
        <title>Upload API</title>
    </head>
    <body>
        <h1>API now started...</h1>
    </body>
</html>
    """


@app.post("/upload")
async def upload(file: UploadFile = File()):
    content = await file.read()
    destination_blob_name = file.filename
    input(content, destination_blob_name)

# Upload files to BUCKET
def input (contents, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(config["BUCKET"])
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    print(
        f"{destination_blob_name} uploaded to GCS {config['BUCKET']}"
    )

# def main():
#     uvicorn.run("app:app", host="0.0.0.0",
#                 port=int(config["PORT"]), reload=config["DEVELOPMENT"])


# if __name__ == "__main__":
#     sys.exit(main())