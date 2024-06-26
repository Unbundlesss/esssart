from multiprocessing import Pool
from PIL import Image, ImageOps


def crop_to_square(args):
    image_path, output_path, name, url = args
    size = (800, 800)
    with Image.open(image_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        ImageOps.fit(img, size).save(output_path, 'JPEG')
        print(f'resized to {output_path}')


def process_images(image_paths, output_paths):
    print('processing')
    with Pool() as pool:
        pool.map(crop_to_square, zip(image_paths, output_paths))

# Example usage:
# image_paths = ["image1.png", "image2.png", "image3.png"]
# output_paths = ["output1.png", "output2.png", "output3.png"]
# process_images(image_paths, output_paths)
