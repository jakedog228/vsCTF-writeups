from PIL import Image


"""
This is basically just a programming exercise
It's not too hard to solve once you understand the task

I will be referring to the left scanning area as the "canvas", and the right as the "key"
"""


# Extract all the frames in the file
print('Extracting frames...')
scan = Image.open('scan.apng')
for i in range(0, scan.n_frames):
    scan.seek(i)
    scan.save(f'frames/{i}.png')


# top right coordinates of the canvas and first data point in the key
canvas_coord = (20, 60)
key_coord = (567, 63)
canvas_width, canvas_height = 500, 270

orig_image = Image.new('RGB', (canvas_width, canvas_height))
orig_pix = orig_image.load()


# iterates through all 528 frames
print('Reconstructing flag...')
for i in range(0, scan.n_frames):
    frame = Image.open(f'frames/{i}.png').convert('RGB')
    pix = frame.load()

    # read the key data, 64 represents how many key sets per column, reading top-down, then left-right
    # the key-identifiers are arranged in a predictable order, so we can rely on indexes to sort the data
    key_data = [pix[(key_set // 64) * 10 + key_coord[0], (key_set % 64) * 4 + key_coord[1]] for key_set in range(256)]

    # iterate through each pixel in the canvas
    for pixel_index in range(canvas_width * canvas_height):
        x = pixel_index % canvas_width
        y = pixel_index // canvas_width

        # only scan colored pixels
        this_value = pix[canvas_coord[0] + x, canvas_coord[1] + y]
        if this_value == (255, 255, 255):
            continue

        # if pixel has a color value, add its keyed value to the original image
        orig_pix[x, y] = key_data[this_value[1]]


orig_image.show()
