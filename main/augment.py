# -*- coding: utf-8 -*-
import argparse
import PIL
import numpy as np
import os
from pathlib import Path
from tqdm import tqdm
import albumentations as A
import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', '-f', default=None, type=str, help="path for the dataset.")

    args = parser.parse_args()

    return args


def main():
    # init args
    args = parse_args()
    assert args.folder is not None, 'the folder for augmentation  must be provided!'

    transform_dict = {
        "rain": A.Compose(
            [A.RandomRain(brightness_coefficient=0.9, drop_width=1, blur_value=5, p=1)]
        ),
        "snow": A.Compose(
            [
                A.RandomSnow(
                    brightness_coeff=2.5, snow_point_lower=0.3, snow_point_upper=0.5, p=1
                )
            ]
        ),
        "sun_flare": A.Compose(
            [A.RandomSunFlare(flare_roi=(0, 0, 1, 0.5), angle_lower=0.5, p=1)],
        ),
        "fog": A.Compose(
            [A.RandomFog(fog_coef_lower=0.2, fog_coef_upper=0.2, alpha_coef=0.4, p=1)],
        ),
        "rain_night": A.Compose(
            [
                A.RandomRain(brightness_coefficient=0.9, drop_width=1, blur_value=5, p=1),
                A.augmentations.transforms.ColorJitter(brightness=(0.1, 0.1)),
            ]
        ),
        "snow_night": A.Compose(
            [
                A.RandomSnow(
                    brightness_coeff=2.5, snow_point_lower=0.3, snow_point_upper=0.5, p=1
                ),
                A.augmentations.transforms.ColorJitter(brightness=(0.1, 0.1)),
            ]
        ),
        "fog_night": A.Compose(
            [
                A.RandomFog(fog_coef_lower=0.2, fog_coef_upper=0.2, alpha_coef=0.4, p=1),
                A.augmentations.transforms.ColorJitter(brightness=(0.1, 0.1)),
            ],
        ),
    }

    paths = []
    for path, subdirs, files in os.walk(args.folder):
        for name in files:
            paths.append(os.path.join(path, name))

    t0 = time.time()
    for path in tqdm(paths):
        try:
            if path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                image = np.asarray(PIL.Image.open(path))

                for name, transform in transform_dict.items():
                    p = Path(path)
                    new_path = str(p.parent / (name + '_' + p.name))
                    if not os.path.exists(new_path):
                        transformed_image = transform(image=image)['image']
                        im = PIL.Image.fromarray(transformed_image)
                        im.save(new_path)
        except Exception as exc:
            print(path, str(exc))

    print("Augmentation is done.")
    t1 = time.time()
    print(f"It took {float(t1-t0)} seconds")


if __name__ == '__main__':
    main()
