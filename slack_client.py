import os
from slack import WebClient
from slack.errors import SlackApiError
from secrets import workspace_file_path, workspace_logging_path
import logging
import constants

# -------------------------------------- LOGGER-Config -------------------------------------------
FORMAT = constants.LOGGER_FORMAT
logging.basicConfig(
    format=FORMAT,
    level=logging.NOTSET,
    filename=workspace_logging_path,
    filemode='a'
)
# -------------------------------------- LOGGER-Config -------------------------------------------

client_lt = WebClient(token=os.environ['SLACK_API_TOKEN_LT'])
client_rm = WebClient(token=os.environ['SLACK_API_TOKEN_RM'])
client_zs = WebClient(token=os.environ['SLACK_API_TOKEN_ZS'])
client_bk = WebClient(token=os.environ['SLACK_API_TOKEN_BK'])
client_sk = WebClient(token=os.environ['SLACK_API_TOKEN_SK'])

try:
    filepath = workspace_file_path
    for client in [client_lt, client_rm, client_zs, client_bk, client_sk]:
        response = client.files_upload(
            channels='#coronavirus-updates',
            file=filepath)
        logging.info("File Uploaded successfully")
        assert response["file"]  # the uploaded file

except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    logging.info("Script Failed!!!")
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")
