Uploading a File:
python script.py upload --bucket-url "https://sukrat-storage.nyc3.digitaloceanspaces.com" --file-path "/path/to/your/file.txt"
Action: upload
Required Arguments:
--bucket-url: URL of the bucket where the file will be uploaded.
--file-path: Path to the file you want to upload.


Listing Files in a Bucket:
python script.py list --bucket-url "https://sukrat-storage.nyc3.digitaloceanspaces.com"
Action: list
Required Arguments:
--bucket-url: URL of the bucket where you want to list the files.


Deleting Files from URLs:
python script.py delete --urls '["https://sukrat-storage.nyc3.digitaloceanspaces.com/test/test2/bio-2.pdf", "https://sukrat-storage.nyc3.digitaloceanspaces.com/test/test2/other-file.txt"]'
Action: delete
Required Arguments:
--urls: JSON-encoded list of URLs of the files you want to delete.


Summary of Actions:
upload: Uploads a file to the specified bucket.
list: Lists all files in the specified bucket.
delete: Deletes files using their URLs.