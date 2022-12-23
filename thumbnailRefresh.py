import asyncio
import os
from datetime import datetime
from pathlib import Path
from blinkpy.auth import Auth
from blinkpy.blinkpy import Blink
from blinkpy.helpers.util import json_load

# Set up the Blink and Auth objects
blink = Blink()
auth = Auth(json_load("cred.json"))
blink.auth = auth
blink.start()

counter_file = "count.txt"


async def update_image(camera):
    camera.snap_picture()
    print("Image updated")


async def save_image(camera, image_path):
    camera.image_to_file(image_path)
    print("Image saved to file")


async def main():
    global counter  # Make the counter variable global
    counter = 0

    # Load the counter value from the file, if it exists
    if os.path.exists(counter_file):
        with open(counter_file, "r") as f:
            counter = int(f.read())
        print(f"Loaded counter value from file: {counter}")

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
        image_path = camera_dir / f"{name}{counter:02}.jpg"
        await save_image(camera, image_path)
        print(
            f"Saved image to {image_path} at {today.strftime('%Y/%m/%d %H:%M:%S')}"
        )
        # Wait 5 seconds before moving on to the next camera
        await asyncio.sleep(5)

    # Increment the counter and save it to the file
    counter += 1
    with open(counter_file, "w") as f:
        f.write(str(counter))
    print(f"Saved counter value to file: {counter}")

# Run the main function
asyncio.run(main())
