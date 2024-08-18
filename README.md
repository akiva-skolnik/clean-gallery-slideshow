# Gallery Slideshow Project

## Description

This guide will help you set up a slideshow of your gallery on a Raspberry Pi.  
It also includes a script to clean the gallery by removing bad images.

## Table of Contents

* [Prerequisites](#prerequisites)
* [Cleaning the gallery](#cleaning-the-gallery)
* [Preparing the Raspberry Pi](#preparing-the-raspberry-pi)
* [Final steps](#final-steps)
* [Notes](#notes)

## Prerequisites

- Raspberry Pi (Wi-Fi is optional but makes installing packages easier)
- SD card
- USB keyboard
- Necessary adapters and cables (HDMI, USB, etc.)
- Monitor with HDMI input

## Cleaning the gallery

To remove "bad" images from the gallery, you'll first need to define what "bad" means.  
Initially, I tried removing blurry or dark images, but the results were unsatisfactory.  
Eventually, I decided to remove images without faces. To improve accuracy, I used two different models for face
detection.  
However, since I don’t fully trust these models, I manually checked the images.
The images are sorted by how bad they are according to the models, so we can easily delete the bad ones.
(Note that you can skip the last step if you don't want to clean the original gallery and just copy the clean images)

Then, I run a script that deletes the original images for the deleted images copy in the temporary folder.
I added most of the functions I tried in `clean_gallery/`, so you can combine them as you wish.

Steps to clean your gallery:

1. Run `python clean_gallery/detect_faces.py` to detect faces in the images and copy them to the temporary folder.
2. Manually review the images in the temporary folder and delete the bad ones.
3. Run `python helper_scripts/remove_bad_images.py` to delete the original images corresponding to the deleted images in the temporary
   folder.
4. Run `python helper_scripts/copy_images.py` to copy the clean images to the USB drive.
   (again, you can skip steps 2-3 if you don't want to clean the original gallery. Some adjustments may be needed in the
   script)

## Preparing the Raspberry Pi

I spent a lot of time trying to connect the Raspberry Pi to the internet through my computer (SSH) but without
success.  
I suggest using a Raspberry Pi with Wi-Fi for easier setup.

Steps to prepare your Raspberry Pi:

1. Use [Raspberry Pi Imager](https://www.raspberrypi.org/software/) to install Raspberry Pi OS Lite on the SD card (
   without desktop).
2. We will use `fbi` to display the images. Since you might not have internet access on the Pi,
   download `fbi` and its dependencies on another computer. Here are some useful links:
    - [fbi_2.10-4+b1_armhf.deb](https://ftp.debian.org/debian/pool/main/f/fbi/fbi_2.10-4+b1_armhf.deb)
    - [libcups2_2.4.2-3+deb12u4_armhf.deb](http://raspbian.raspberrypi.org/raspbian/pool/main/c/cups/libcups2_2.4.2-3+deb12u4_armhf.deb)
    - [ghostscript_10.0.0~dfsg-11+deb12u2_armhf.deb](http://raspbian.raspberrypi.org/raspbian/pool/main/g/ghostscript/ghostscript_10.0.0~dfsg-11+deb12u2_armhf.deb)
    - [libgs10_10.0.0~dfsg-11+deb12u2_armhf.deb](http://raspbian.raspberrypi.org/raspbian/pool/main/g/ghostscript/libgs10_10.0.0~dfsg-11+deb12u2_armhf.deb)
    - [libgs10-common_10.0.0~dfsg-11+deb12u2_all.deb](http://raspbian.raspberrypi.org/raspbian/pool/main/g/ghostscript/libgs10-common_10.0.0~dfsg-11+deb12u2_all.deb)
    - [libgs-common_10.0.0~dfsg-11+deb12u2_all.deb](http://raspbian.raspberrypi.org/raspbian/pool/main/g/ghostscript/libgs-common_10.0.0~dfsg-11+deb12u2_all.deb)
    - [Download `fbi` package](https://packages.debian.org/bullseye/armhf/fbi/download)
      You may also need `libgif7`.
3. Save the downloaded files on the SD card along with the `display.sh` script and insert the SD card into the Raspberry
   Pi.
4. Remember to mount and unmount the USB drive each time you connect/disconnect it to the Raspberry
   Pi: `sudo mount /dev/sda1 /mnt/usb` and `sudo umount /mnt/usb`.
5. Connect the Raspberry Pi to the power source, monitor, keyboard, and USB drive.
6. Log in with the default credentials (username: pi, password: raspberry) and enable auto-login
   using `sudo raspi-config`.
7. Install the downloaded `.deb` files with `sudo dpkg -i /home/pi/*.deb` (you should first move them to the SD card
   partition using another Linux machine).

## Final steps

1. Make the `display.sh` script executable with `chmod +x /home/pi/display.sh`.
2. Test the script by running `/home/pi/display.sh` (press Esc or Ctrl+C to exit).
3. To run the script automatically on startup, edit the `rc.local` file: `sudo nano /etc/rc.local` and add the following
   line before `exit 0`: `sudo /home/pi/display.sh &`.
   Alternatively, you can use Linux services to run the script at startup.

## Notes

The script will display the images in the USB drive in a random order.  
This is achieved by splitting the image names into text files (`generate_random_lists.py`) and then sending them
to `fbi` in a loop (`display.sh`).
