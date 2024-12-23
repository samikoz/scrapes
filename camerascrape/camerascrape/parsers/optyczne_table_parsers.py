import re

from datetime import date
from functools import wraps
from typing import List, Tuple, Callable, Any, NewType, Optional
from camerascrape.exceptions import OptyczneSubparserException


RowParser = NewType('RowParser', Callable[[str], Any])


resolution_pattern: re.Pattern = re.compile(r'\d,?\d{3} ?x ?\d,?\d{3}')
matrix_pattern: re.Pattern = re.compile(r'(\d+(?:\.\d)?)[ a-z]{0,4}[x×] ?(\d+(?:\.\d)?)')
iso_range_pattern: re.Pattern = re.compile(r'\d+ ?- ?\d+')
shutter_speed_pattern: re.Pattern = re.compile(r'1/(\d+)')
weight_pattern: re.Pattern = re.compile(r'\d+(?:\.\d)?')
mechanical_shutter_pattern: re.Pattern = re.compile(r'mechan', re.I)
electronic_shutter_pattern: re.Pattern = re.compile(r'elektron', re.I)


def exc_raiser(parsee: str) -> Callable[[RowParser], RowParser]:
    def wrapping_decorator(f: RowParser) -> RowParser:
        @wraps(f)
        def wrapped_f(row: str) -> Any:
            try:
                return f(row)
            except Exception as e:
                raise OptyczneSubparserException(parsee, e)
        return wrapped_f
    return wrapping_decorator


@exc_raiser('release')
def date_parser(row: str) -> date:
    return date(*[int(date_part) for date_part in row.split('-')])


@exc_raiser('pixels')
def pixels_parser(row: str) -> float:
    return float(row[:-5])


@exc_raiser('resolution')
def parse_resolution(row: str) -> int:
        return max(
            *[tuple(int(resol_part.replace(",", "")) for resol_part in resol.split('x')) for resol in re.findall(resolution_pattern, row)],
            key=lambda resol_pair: resol_pair[0] * resol_pair[1]
        )


@exc_raiser('matrix_size')
def parse_matrix_size(row: str) -> Tuple[float, float]:
    match = matrix_pattern.search(row)
    return float(match.group(1)), float(match.group(2))


@exc_raiser('iso_range')
def parse_iso(row: str) -> Tuple[int, int]:
    return tuple(int(iso) for iso in re.search(iso_range_pattern, row).group().split('-'))


@exc_raiser('inverse_mechanical_shutter')
def parse_mechanical_shutter(row: str) -> Optional[int]:
    shutter_speeds: List[str] = re.findall(shutter_speed_pattern, row)
    if mechanical_shutter_pattern.search(row) and len(shutter_speeds) > 0:
        return min(int(speed) for speed in shutter_speeds)


@exc_raiser('inverse_electronic_shutter')
def parse_electronic_shutter(row: str) -> Optional[int]:
    shutter_speeds: List[str] = re.findall(shutter_speed_pattern, row)
    if electronic_shutter_pattern.search(row) and len(shutter_speeds) > 0:
        return max(int(speed) for speed in shutter_speeds)


@exc_raiser('weight')
def parse_weight(row: str) -> int:
    return max(int(weight) for weight in re.findall(weight_pattern, row))


@exc_raiser('dimensions')
def parse_dimensions(row: str) -> Tuple[float, float, float]:
    return tuple(float(dim) for dim in re.findall(weight_pattern, row))
