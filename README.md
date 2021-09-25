# PhotoStack Studio - Version 1.0

PhotoStack is a simple image editing software developed for a local business, and was written in Python 3.9 and converted to an executable file using PyInstaller 4.5.1. The business need was to combine images in 3 different configurations, which have been called stacks. The stack layouts are: a vertical stack, a horizontal stack and a two-column stack - all of which were to be resized automatically to fit nicely and reduce file size. Another requirement was have an option to resize a single image manually, by inputting the desired dimensions for height and width. Additional features have been added to improve ease-of-use, and a full list is given below.

<p align="center">
  <img src="https://user-images.githubusercontent.com/39648391/134772365-6148e3b0-4340-435e-a29c-a0ded4e6546e.png" alt="PhotoStack">
</p>

## Main Features:

- Combine images in 3 layouts: vertical, horiztonal, 2-column
- Resize single images to specified dimensions
- Save as JPG and PNG file types
- Browse different photo directories
- Combine images from multiple directories
- Responsive widget resizing
- Full-screen bordless mode
- Warning prompt for overwriting existing file with identical file name
- Error handling for invalid resize dimensions/file name etc

## Gallery:

<table>
<tbody>
  <tr>
    <td><img width="400" src="https://user-images.githubusercontent.com/39648391/134771939-5423bbd7-529f-42d8-a89a-91a77be2f652.png" alt="Vertical"></td>
    <td><img width="400" src="https://user-images.githubusercontent.com/39648391/134772365-6148e3b0-4340-435e-a29c-a0ded4e6546e.png" alt="Horizontal"></td>
  </tr>

  <tr>
    <td><p align="center">Vertical Stack Mode</p></td>
    <td><p align="center">Horizontal Stack Mode</p></td>
  </tr>

  <tr>
    <td><img width="400" src="https://user-images.githubusercontent.com/39648391/134771929-3658d362-c698-43b5-a565-2897f693dca8.png" alt="2 Column"></td>
    <td><img width="400" src="https://user-images.githubusercontent.com/39648391/134771936-7670fda2-87f8-40b4-81c9-0bd303f3b2f4.png" alt="Resize"></td>
  </tr>

  <tr>
    <td><p align="center">2 Column Stack Mode</p></td>
    <td><p align="center">Resize</p></td>
  </tr>

  <tr>
    <td><img src="https://user-images.githubusercontent.com/39648391/134771935-fc5f1815-1bfa-489f-829c-ea28240e8d2a.png" alt="Dropdown Menu"></td>
    <td><img src="https://user-images.githubusercontent.com/39648391/134773211-a1b2a958-973d-4640-a6a4-431daaf536a3.png" alt="File Structure"></td>
  </tr>

  <tr>
    <td><p align="center">Dropdown Menu</p></td>
    <td><p align="center">File Structure</p></td>
  </tr>
</tbody>
</table>


## Installation:

### Windows

To install, clone the repository to your desktop and run the executable:

`git clone https://github.com/BradneySmith/PhotoStack-Studio.git`

### MacOS and Linux

For MacOS and Linux users, make sure you have the PIL module installed. To do this, you can use:

`pip install PIL`

To install, clone the repository to your desktop:

`git clone https://github.com/BradneySmith/PhotoStack-Studio.git`

#### From the terminal:
cd into the PhotoStack Studio directory on your desktop

Run the main.py file:

`python3 main.py`

#### From a GUI:
Open the PhotoStack Studio folder

Run the main.py file

## How to Use PhotoStack Studio
1. Move the PhotoStack folder to your desktop.

2. Open the folder and the PhotoStack Studio.exe.

3. By default, PhotoStack Studio looks for images in the unstacked_images directory, which is in the same directory as the executable. You can drag images into this folder if you want to keep your unedited images in one place.

4. Alternatively, you can use images from other directories on your desktop. To do this, click on the dropdown menu below the 'Photos' label in the top left of the screen. This will give a list of all the folders on your desktop, as well as a folder for images that are saved directly to your desktop. This folder is called 'Desktop'.

5. Choose the stack layout you want (Vertical, Horizontal or 2 Column) using the radio buttons at the bottom of the screen.

6. Click the image thumbnails to add them to the preview area. Images are added in the order they are clicked. To remove an image, simply click its thumbnail button again.

7. To use the resize feature, select the 'Resize' radio button and enter the dimensions in the 'Width' and 'Height' entry boxes under the 'Dimensions' label.

8. To save an image, choose an extension, then enter a file name (these are set to 'jpg' and 'untitled' by default). When you are ready, click 'Export' in the bottom right or go to File > Save.

9. If an image with the given file name already exists, you will be asked if you want to overwrite it. To give a new name, simply type a different file name into the entry box. To overwrite the existing file, click 'Export' again, or go to File > Save.

10. To clear the screen, you can unclick each image thumbnail, or go File > New.

11. To enter Full Screen Borderless mode go to View > Full Screen Borderless. To exit Full Screen mode, go to View > Windowed.
