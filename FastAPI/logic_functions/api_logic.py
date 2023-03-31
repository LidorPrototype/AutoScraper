# To understand recursion, see the bottom of this file 
import requests
import io
import os
from datetime import datetime
from fastapi.responses import StreamingResponse

from logic_functions.general_utils import ensure_dir

# Author: Lidor Eliyahu Shelef

def return_file(url_link: str, file_name: str = None):
    # wanted_file_path = tf.keras.utils.get_file(origin=api_link, cache_dir="download_files\\")
    """
        Example url: \n
            http://www.imageprocessingplace.com/downloads_V3/root_downloads/image_databases/standard_test_images.zip
    """

    r = requests.get(url_link, allow_redirects=True)
    today_ = datetime.strftime(datetime.now(), '_%Y_%m_%d.')
    filename = file_name or url_link.split('/')[-1].replace(" ", "_")
    filename = "".join(filename.split('.')[:-1]) + today_ + filename.split('.')[-1]
    print("\n====================================")
    print(filename)
    print("\n====================================")
    wanted_file_path = f"download_files\\{filename}"
    ensure_dir(wanted_file_path.split('\\')[0])
    open(wanted_file_path, 'wb').write(r.content)

    temp_file = None
    with open (wanted_file_path, mode="rb") as _f:
        temp_file = _f.read()
    final_file = io.BytesIO(temp_file)
    os.remove(wanted_file_path)
    return StreamingResponse(final_file)
# To understand recursion, see the top of this file
