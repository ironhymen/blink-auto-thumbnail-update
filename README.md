# Blink Camera Image Saver

This repository contains a script that saves images from Blink camera devices to a local directory. The script can be set up as a cron job or task schedule to repeat at a set interval (e.g. every 20 minutes).

## Prerequisites

- Blink account credentials in a `cred.json` file (see below for instructions on setting up the file)
- `blinkpy` Python library (can be installed with `pip install blinkpy`)

## Usage

1. Clone the repository and navigate to the project directory.
2. Set up a cron job or task schedule to run the script at your desired interval. On Unix-based systems, you can use the `crontab` command to set up a cron job. On Windows, you can use the Task Scheduler.
3. Images will be saved to a directory named after the current date (e.g. `storage/20221225`) in the project directory, with a subdirectory for each camera. The images will be named after the camera and a counter value, in the format `<camera_name><counter:02>.jpg`.

## Setting up the `cred.json` file

The script requires a `cred.json` file with your Blink account credentials in order to authenticate with the Blink API. The file should have the following structure:

```json
{
    "username": "your-blink-username",
    "password": "your-blink-password",
    "uid": "your-blink-uid",
    "device_id": "your-device-id",
    "token": "your-token",
    "host": "your-host",
    "region_id": "your-region-id",
    "client_id": your-client-id,
    "account_id": your-account-id
}
```


## Acknowledgements

- [Blinkpy library](https://github.com/tchellomello/python-blinkpy) by [tchellomello](https://github.com/tchellomello)