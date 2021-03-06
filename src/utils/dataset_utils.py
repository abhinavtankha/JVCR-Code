import requests
import tarfile

#file_id = 'TAKE ID FROM SHAREABLE LINK'
#destination = 'DESTINATION FILE ON YOUR DISK'
def download_file_from_google_drive(id, destination):
    URL = 'https://docs.google.com/uc?export=download'

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    print('downloading dataset..')
    save_response_content(response, destination)   
    print('download complete')

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def extract_tar_file(path, outputdir):
    print('extracting dataset file..')
    tf = tarfile.open(path)
    tf.extractall(path=outputdir)
    print('extraction of dataset complete.')