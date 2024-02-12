import argparse
import collections.abc as collections
from pathlib import Path
from typing import Optional, Union, List

from . import logger
from .utils.parsers import parse_image_lists
from .utils.io import list_h5_names


''' pefroms sequential matching between x frame images in the same sequence'''
def stereo_main(
        output: Path,
        image_list: Optional[Union[Path, List[str]]] = None,
        features: Optional[Path] = None,
        ref_list: Optional[Union[Path, List[str]]] = None,
        ref_features: Optional[Path] = None):

    if image_list is not None:
        if isinstance(image_list, (str, Path)):
            names_q = parse_image_lists(image_list)
        elif isinstance(image_list, collections.Iterable):
            names_q = list(image_list)
        else:
            raise ValueError(f'Unknown type for image list: {image_list}')
    elif features is not None:
        names_q = list_h5_names(features)
    else:
        raise ValueError('Provide either a list of images or a feature file.')

    self_matching = False
    if ref_list is not None:
        if isinstance(ref_list, (str, Path)):
            names_ref = parse_image_lists(ref_list)
        elif isinstance(image_list, collections.Iterable):
            names_ref = list(ref_list)
        else:
            raise ValueError(
                f'Unknown type for reference image list: {ref_list}')
    elif ref_features is not None:
        names_ref = list_h5_names(ref_features)
    else:
        self_matching = True
        names_ref = names_q

    pairs = []
    '''pairing 2 sequential images'''
    en = len(names_q)
    for i in range(en - 1, 0, -1):
        for j in range (i - 1, max(i - 5, -1), -1):
            #logger.info(f"{i},{j}")
            pairs.append((names_q[i], names_q[j]))
            #logger.info(f"({i}: {names_q[i]},{names_q[j]})")
            #logger.info(f"{i}:{names_q[i]} {j}:{names_q[j]}")
    logger.info(f'Found {len(pairs)} pairs.')
    with open(output, 'w') as f:
        f.write('\n'.join(' '.join([i, j]) for i, j in pairs))



def main(
        output: Path,
        image_list: Optional[Union[Path, List[str]]] = None,
        features: Optional[Path] = None,
        ref_list: Optional[Union[Path, List[str]]] = None,
        ref_features: Optional[Path] = None):

    if image_list is not None:
        if isinstance(image_list, (str, Path)):
            names_q = parse_image_lists(image_list)
        elif isinstance(image_list, collections.Iterable):
            names_q = list(image_list)
        else:
            raise ValueError(f'Unknown type for image list: {image_list}')
    elif features is not None:
        names_q = list_h5_names(features)
    else:
        raise ValueError('Provide either a list of images or a feature file.')

    self_matching = False
    if ref_list is not None:
        if isinstance(ref_list, (str, Path)):
            names_ref = parse_image_lists(ref_list)
        elif isinstance(image_list, collections.Iterable):
            names_ref = list(ref_list)
        else:
            raise ValueError(
                f'Unknown type for reference image list: {ref_list}')
    elif ref_features is not None:
        names_ref = list_h5_names(ref_features)
    else:
        self_matching = True
        names_ref = names_q

    pairs = []
    for i, n1 in enumerate(names_q):
        for j, n2 in enumerate(names_ref):
            if self_matching and j <= i:
                continue
            pairs.append((n1, n2))

    logger.info(f'Found {len(pairs)} pairs.')
    with open(output, 'w') as f:
        f.write('\n'.join(' '.join([i, j]) for i, j in pairs))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--image_list', type=Path)
    parser.add_argument('--features', type=Path)
    parser.add_argument('--ref_list', type=Path)
    parser.add_argument('--ref_features', type=Path)
    args = parser.parse_args()
    main(**args.__dict__)
