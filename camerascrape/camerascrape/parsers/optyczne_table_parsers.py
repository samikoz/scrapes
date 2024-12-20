import re

from functools import wraps
from typing import List, Tuple, Callable, Any, NewType
from camerascrape.exceptions import OptyczneSubparserException


RowParser = NewType('RowParser', Callable[[str], Any])


aspect_ratio_pattern: re.Pattern = re.compile(r'\[\d{1,2}:\d{1,2}]')
resolution_pattern: re.Pattern = re.compile(r'\d{4} x \d{4}')
matrix_pattern: re.Pattern = re.compile(r'\d+\.\d x \d+\.\d')
iso_range_pattern: re.Pattern = re.compile(r'\d+-\d+')
shutter_speed_pattern: re.Pattern = re.compile(r'1/(\d+)')
frame_frequency_pattern: re.Pattern = re.compile(r'(\d+) kl/s')
weight_pattern: re.Pattern = re.compile(r'\d+')


def exc_raiser(parsee: str) -> Callable[[RowParser], RowParser]:
    def wrapping_decorator(f: RowParser) -> RowParser:
        @wraps(f)
        def wrapped_f(row: str) -> Any:
            try:
                return f(row)
            except:
                raise OptyczneSubparserException(parsee)
        return wrapped_f
    return wrapping_decorator


@exc_raiser('pixels')
def pixels_parser(row: str) -> float:
    return float(row[:-5])


@exc_raiser('aspect_ratios')
def parse_aspect_ratios(row: str) -> List[str]:
    return [aspect_ratio_pattern.search(part).group() for part in row.split('\r\n')]


@exc_raiser('resolutions')
def parse_resolution(row: str) -> List[str]:
        return [max(
            *[tuple(int(resol_part) for resol_part in resol.split('x')) for resol in re.findall(resolution_pattern, part)],
            key=lambda resol_pair: resol_pair[0] * resol_pair[1]
        ) for part in row.split('\r\n')]


@exc_raiser('matrix_size')
def parse_matrix_size(row: str) -> Tuple[float, float]:
    return tuple(float(dim) for dim in matrix_pattern.search(row).group().split(' x '))


@exc_raiser('iso_range')
def parse_iso(row: str) -> Tuple[float, float]:
    return tuple(float(iso) for iso in re.search(iso_range_pattern, row.split('\r\n')[0]).group().split('-'))


@exc_raiser('mechanical_shutter')
def parse_mechanical_shutter(row: str) -> int:
    return int(re.search(shutter_speed_pattern, list(filter(lambda s: 'mechaniczna' in s, row.split('\r\n')))[0]).group(1))


@exc_raiser('electronic_shutter')
def parse_electronic_shutter(row: str) -> int:
    return int(
        re.search(shutter_speed_pattern, list(filter(lambda s: 'elektroniczna' in s, row.split('\r\n')))[0]).group(1))


@exc_raiser('video_modes')
def parse_video_modes(row: str) -> List[Tuple[int, int, int]]:
    modes: List[Tuple[int, int, int]] = []
    for part in row.split('\r\n'):
        if len(part) == 0:
            continue
        resols: List[int] = [int(resol_part) for resol_part in resolution_pattern.search(part).group().split('x')]
        frame_freq: int = int(frame_frequency_pattern.search(part).group(1))
        modes.append(tuple(resols + [frame_freq]))
    return modes


@exc_raiser('weight')
def parse_weight(row: str) -> int:
    return max(int(weight) for weight in re.findall(weight_pattern, row))


@exc_raiser('dimensions')
def parse_dimensions(row: str) -> Tuple[float, float, float]:
    return tuple(float(dim) for dim in row[:-3].split(' × '))
