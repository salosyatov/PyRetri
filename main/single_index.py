# -*- coding: utf-8 -*-

import argparse
import os
from pathlib import Path

from PIL import Image
import numpy as np
from dotenv import load_dotenv

from main_module.config import get_defaults_cfg, setup_cfg
from main_module.datasets import build_transformers
from main_module.models import build_model
from main_module.extract import build_extract_helper
from main_module.index import build_index_helper, feature_loader


load_dotenv("bot/.env")

default_config_file = os.getenv("CONFIG_YAML", '')


def parse_args():
    parser = argparse.ArgumentParser(description='A tool box for deep learning-based image retrieval')
    parser.add_argument('opts', default=None, nargs=argparse.REMAINDER)
    parser.add_argument('--config_file', default=default_config_file, metavar='FILE', type=str, help='path to config file') # TODO:
    args = parser.parse_args()
    return args


def main(img: np.ndarray, topk = 5):

    # init args
    args = parse_args()
    assert args.config_file != "", 'a config file must be provided!'
    assert os.path.exists(args.config_file), 'the config file must be existed!'

    # init and load retrieval pipeline settings
    cfg = get_defaults_cfg()
    cfg = setup_cfg(cfg, args.config_file, args.opts)

    # build transformers
    transformers = build_transformers(cfg.datasets.transformers)

    # build model
    model = build_model(cfg.model)

    # read image and convert it to tensor

    img_tensor = transformers(img)

    # build helper and extract feature for single image
    extract_helper = build_extract_helper(model, cfg.extract)
    img_fea_info = extract_helper.do_single_extract(img_tensor)
    stacked_feature = list()
    for name in cfg.index.feature_names:
        assert name in img_fea_info[0], "invalid feature name: {} not in {}!".format(name, img_fea_info[0].keys())
        stacked_feature.append(img_fea_info[0][name].cpu())
    img_fea = np.concatenate(stacked_feature, axis=1)

    # load gallery features
    gallery_fea, gallery_info, _ = feature_loader.load(cfg.index.gallery_fea_dir, cfg.index.feature_names)

    # build helper and single index feature
    index_helper = build_index_helper(cfg.index)
    index_result_info, query_fea, gallery_fea = index_helper.do_index(img_fea, img_fea_info, gallery_fea)
    save = False
    if save:
        index_helper.save_topk_retrieved_images('retrieved_images/', index_result_info[0], topk, gallery_info)

    query_idx = index_result_info[0]["ranked_neighbors_idx"]

    query_topk_idx = query_idx[:topk]
    paths = [str(Path(gallery_info[idx]["path"])) for idx in query_topk_idx]
    labels = [gallery_info[idx]["label"] for idx in query_topk_idx]

    print('single index have done!')
    return paths, labels


class Recognizer:

    def __int__(self):
        pass

    def find_similar(self, image: np.ndarray, k: int):
        paths, labels = main(image, topk=k)
        return paths, labels


if __name__ == '__main__':
    path = 'data/query/32.jpg'
    img = Image.open(path).convert("RGB")
    # img = Image.fromarray(array)
    main(img)
