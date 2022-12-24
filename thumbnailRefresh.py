import asyncio
from datetime import datetime
from pathlib import Path
from blinkpy.auth import Auth
from blinkpy.blinkpy import Blink
from blinkpy.helpers.util import json_load
import cv2

# Set up the Blink and Auth objects
blink = Blink()
auth = Auth(json_load("cred.json"))
blink.auth = auth
blink.start()

# Define a function to add a timestamp to an image


def add_timestamp(image, timestamp_text):
    # Get the size of the image
    image_height, image_width, _ = image.shape

    # Set the font and scale of the timestamp text
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 2  # Increase the scale to make the text larger
    thickness = 1

    # Get the size of the text
    text_size = cv2.getTextSize(timestamp_text, font, scale, thickness)[0]

    # Set the bottom-left corner of the text
    text_x = image_width - text_size[0] - 10
    text_y = image_height - 10

    # Add the timestamp text to the image
    cv2.putText(image, timestamp_text, (text_x, text_y), font,
                scale, (255, 255, 255), thickness, cv2.LINE_AA)


async def update_image(camera):
    camera.snap_picture()
    print("Image updated")


async def save_image(camera, image_path):
    # Save the image to file using the camera.image_to_file method
    camera.image_to_file(image_path)

    # Load the saved image
    image = cv2.imread(str(image_path))

    # Get the current timestamp
    now = datetime.now()
    timestamp_text = now.strftime("%Y/%m/%d %H:%M")

    # Add the timestamp to the image
    add_timestamp(image, timestamp_text)

    # Save the image with the timestamp to file
    cv2.imwrite(str(image_path), image)
    print(f"Image saved to file: {image_path}")


async def main():
    # Get the current date and create the directory for storing images
    today = datetime.now()
    image_dir = Path("storage") / today.strftime("%Y%m%d")
    image_dir.mkdir(parents=True, exist_ok=True)

    # Refresh the sync module and cameras
    blink.refresh()
    print(
        f"Sync module and cameras refreshed at {today.strftime('%Y/%m/%d %H:%M:%S')}"
    )

    # Iterate through the cameras and save an image for each one
    for name, camera in blink.cameras.items():
        # Create a directory for the current camera, if it doesn't already exist
        camera_dir = image_dir / name
        camera_dir.mkdir(exist_ok=True)

        # Update the image for the current camera
        await update_image(camera)
        await asyncio.sleep(10)  # Wait 10 seconds before saving the image

        # Save the image to the appropriate directory
        image_path = camera_dir / f"{name}_{today.strftime('%m%d%H%M')}.jpg"
        await save_image(camera, image_path)
        print(
            f"Saved image to {image_path} at {today.strftime('%Y/%m/%d %H:%M:%S')}"
        )
        # Wait 5 seconds before moving on to the next camera
        await asyncio.sleep(5)

# Run the main function
asyncio.run(main())
