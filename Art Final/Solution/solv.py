from mt19937predictor import MT19937Predictor
from PIL import Image
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


"""
The vulnerability of this challenge is its usage of python's "random" function
"random" is not a cryptographically secure function, and should not be used as such
"random" uses the Mersenne Twister (MT19937) as a method of generating pseudo-random numbers
Using libraries like "mersenne-twister-predictor", we can begin to predict "random" values after enough analysis

LIBRARY USED: https://pypi.org/project/mersenne-twister-predictor/
MORE ON MT19937: https://www.sciencedirect.com/topics/computer-science/mersenne-twister
"""


spicy = Image.open('ENHANCED_Final_2022.png', 'r').convert('RGBA')
spicy_pix = spicy.load()

boring = Image.open('Art_Final_2022.png', 'r').convert('RGBA')
boring_pix = boring.load()

width, height = boring.size[0], boring.size[1]
total_pixels = width * height

predictor = MT19937Predictor()


# We only need the last 624 numbers to get the rest of the data
for i in range(total_pixels - 624, total_pixels):
    x = i % spicy.size[0]
    y = i // spicy.size[0]

    # XOR the matching image pixels to find the number originally generated by MT19937
    rgba = tuple([spice ^ bore for spice, bore in zip(spicy_pix[x, y], boring_pix[x, y])])
    original_value = int.from_bytes(bytes(rgba), 'little')

    # Add the value to the predictor
    predictor.setrandbits(original_value, 32)


# Generate the AES key based on the predictor's guess of what the next 16 byes would be
key = bytes(predictor.sample(predictor.randbytes(AES.block_size), AES.block_size))

# Standard AES CBC decoding
out = b64decode('Tl5nK8L2KYZRCJCqLF7TbgKLgy1vIkH+KIAJv5/ILFoC+llemcmoLmCQYkiOrJ/orOOV+lwX+cVh+pwE5mtx6w==')
ciphertext = out[AES.block_size:]
iv = out[:AES.block_size]
dec = AES.new(key, AES.MODE_CBC, iv)
flag = unpad(dec.decrypt(ciphertext), AES.block_size).decode()

print(flag)