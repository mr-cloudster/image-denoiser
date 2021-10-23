import numpy as np
import os
from numpy.lib.ufunclike import fix
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage import img_as_float, img_as_ubyte
from skimage import io

def remove_noise(path, filename):
    full_path = os.path.join(path, filename)
    image = img_as_float(io.imread(full_path)).astype(np.float32)

    #Estimate the noise standard deviation from the noisy image
    sigma_est = np.mean(estimate_sigma(image, multichannel=True))
    print("estimated noise standard deviation = {}".format(sigma_est))

    #Define a dictionary for the input parameter to NLM algorithm
    patch_kw = dict(patch_size=10,
                    patch_distance=3,
                    multichannel=True)

    denoise_img = denoise_nl_means(image, h=1.15 * sigma_est, 
                                fast_mode=False, **patch_kw) 

    #The denoise image is float 64 type, so we need to convert to 8 byte
    #for desktop viewing.

    denoise_img_as_8byte = img_as_ubyte(denoise_img)
    fixed_image = "denoised-"+filename
    denoisy_path = os.path.join(path, fixed_image)
    #Save the output file to current directory
    io.imsave(denoisy_path, denoise_img_as_8byte)
    return denoisy_path 