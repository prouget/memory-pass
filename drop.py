import dropbox
import Const


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mode=dropbox.files.WriteMode.overwrite)

    def download_File(self):
        
        dbx = dropbox.Dropbox(self.access_token)

        with open(Const.FILE_FROM, "wb") as f:
            metadata, res = dbx.files_download(path=Const.FILE_TO)
            f.write(res.content)

def main():
    
    transferData = TransferData(Const.ACCESS)

    file_from = Const.FILE_FROM
    file_to = Const.FILE_TO # The full path to upload the file to, including the file name

    # API v2
    # transferData.upload_file(file_from, file_to)
    transferData.download_File()

if __name__ == '__main__':
    main()