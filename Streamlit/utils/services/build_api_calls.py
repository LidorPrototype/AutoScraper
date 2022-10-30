import streamlit as st
import tensorflow as tf
import sys
import time
import os

sys.path.append('./utils')
import general_utils as g_utils


#  <<<<<<<<<<<<<<<<<<<<<<<<< Download file based on API call the user provide >>>>>>>>>>>>>>>>>>>>>>>>>         
def api_calls():
    """
        Goal:
            Creating a screen for the user to download data from an API call that 
            the user provide url link to it, the user does not have to know about 
            network or API calls in general, but he can
    """
    custom_headers = {}
    file_options = ['Default', 'json', 'csv', 'txt', 'html', 'doc', 'docx', 'pdf', 'zip', 'rar', 'tar', 'xml', 'ppt', 'pptx', 'xlsx', 'png', 'jpeg', 'bin']
    target_dir = 'Results/API_call/'
    api_link = st.text_input("Please enter wanted API link")
    file_name_flag = False
    if api_link != "":
        default_name = api_link.split('//')[1].split('/')[0].split('.')[1]
    else:
        default_name = ""
    api_cols = st.columns([2, 1])
    with api_cols[0]:
        placeholder = st.empty()
        file_name = placeholder.text_input("Do you know the file name?", key='file_name_input')
        if file_name != "":
            file_name_flag = True
        st.caption("Leave empty if not")
    with api_cols[1]:
        file_format = st.selectbox('File format', file_options, key='file_format')
        if file_format == "Default":
            file_name = placeholder.text_input("Do you know the file name?", key='file_name_input_disabled', value="", help="With Default option the name will be set to the default value as well")
    g_utils.put_line_break()
    make_api_call = st.checkbox("Get file")
    if make_api_call:
        loading_gif = st.image('utils/media/gifs/api_calls1.gif')
        time.sleep(5.0)    
        if api_link != "":
            got_file = False
            local_file_path = ""
            try:       
                local_file_path, got_file, file_name=activate_api_logic(api_link, file_name, file_format, target_dir, file_name_flag)

                loading_gif.empty()
            except Exception as e:
#                 st.code(e)
                example_headers = """
                    Headers should be in the following format, each row should be a different field and value, as follows:\n
                    field_name_1:value_1                                                                            
                    field_name_2:value_2\n
                    Please keep this format, no extra spaces, no ',' and the only thing between the field and the value is the ':' sign.
                """
                st.write("We couldn't process your API request, if you would like to try again,")
                user_headers = st.text_area("Please provide us with headers to try with:", help=example_headers)
                if user_headers != "":
                    new_headers, correct_format = g_utils.parse_headers(user_headers, False)
                    if not correct_format:
                        st.write("Please see the '?' icon for the correct format")
                    elif correct_format:
                        st.write("Your headers will be:")
                        st.write(new_headers)
                        apply_headers = st.checkbox("Apply My Headers!")
                        if apply_headers:
                            st.write("Need to Apply User Headers")
            if got_file:
                try:
                    with open(local_file_path.replace("/", "\\")) as f:
                        download_file = st.download_button(label="download?", data=f, file_name=file_name)
                except:
                    with open(local_file_path.replace("/", "\\"), "rb") as f:
                        download_file = st.download_button(label="download?", data=f, file_name=file_name)
                g_utils.create_process()
        else:
            st.caption("Please fill all of the fields correctly \U0001F607")
    else:
        local_file_path = ""
#  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


def activate_api_logic(_api, _name, _format, dump_directory, _name_flag):
    """
        Goal:
            Get the user the desired file from his / her API call
        Parameters:
            :param _api: The api link from the user
            :param _name: The name of the desired file - defaults to None
            :param _format: Type of format for the file - defaults to bin
            :param dump_directory: Where the file should be downloaded to
            :param _name_flag: Boolean flag to indicate if the file name is known or not
        Returns:
            :return wanted_file_path: The path to the desired file
            :return True: Boolean flag indicates that there were no problems
            :return result_file_name: Name of the file, for the download mechanism
    """
    if _format == "Default":
        _format = ""
        _name = None
    else:
        _format = ("." + _format)
        _name += _format
    wanted_file_path = tf.keras.utils.get_file(origin=_api, fname=_name, cache_dir=dump_directory)
    _name = wanted_file_path.split('\\')[-1]
    return wanted_file_path, True, _name # 'True' is for later, to show that I got the file and that there is no exception
