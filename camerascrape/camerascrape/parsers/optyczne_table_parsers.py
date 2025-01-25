import re
from abc import ABC, abstractmethod

from datetime import date
from typing import List, Tuple, Any, NewType, Optional, Iterable
from camerascrape.exceptions import OptyczneSubparserException


ParsedFieldName = NewType('ParsedFieldName', str)


resolution_pattern: re.Pattern = re.compile(r'\d,?\d{3} ?[x×] ?\d,?\d{3}')
matrix_pattern: re.Pattern = re.compile(r'(\d+(?:\.\d)?)[ a-z]{0,4}[x×] ?(\d+(?:\.\d)?)')
iso_range_pattern: re.Pattern = re.compile(r'\d+ ?[-–] ?\d+')
shutter_speed_pattern: re.Pattern = re.compile(r'1/(\d+)')
weight_pattern: re.Pattern = re.compile(r'\d+')
dimension_pattern: re.Pattern = re.compile(r'\d+(?:\.\d)?')
mechanical_shutter_pattern: re.Pattern = re.compile(r'mechan', re.I)
electronic_shutter_pattern: re.Pattern = re.compile(r'elektron', re.I)


class OptyczneTableParser(ABC):
    @abstractmethod
    def parse(self, table_row: str) -> Iterable[Tuple[ParsedFieldName, Any]]:
        pass


class OptyczneSingleFieldParser(OptyczneTableParser):
    @abstractmethod
    def _get_parsed_fieldname(self) -> str:
        pass

    @abstractmethod
    def _parse_table_row(self, row: str) -> Any:
        pass

    def parse(self, row: str) -> Iterable[Tuple[ParsedFieldName, Any]]:
        try:
            return [(ParsedFieldName(self._get_parsed_fieldname()), self._parse_table_row(row))]
        except Exception as e:
            raise OptyczneSubparserException([self._get_parsed_fieldname()], e)


class VacuousParser(OptyczneTableParser):
    def __init__(self, field_name: str) -> None:
        self._field_name: str = field_name

    def parse(self, table_row: str) -> Iterable[Tuple[ParsedFieldName, Any]]:
        return [(ParsedFieldName(self._field_name), table_row)]


class DateParser(OptyczneSingleFieldParser):
    def _get_parsed_fieldname(self) -> str:
        return 'release'

    def _parse_table_row(self, row: str) -> date:
        return date(*[int(date_part) for date_part in row.split('-')])


class PixelsParser(OptyczneSingleFieldParser):
    def _get_parsed_fieldname(self) -> str:
        return 'pixels'

    def _parse_table_row(self, row: str) -> float:
        return float(row[:-5])


class ResolutionParser(OptyczneSingleFieldParser):
    def _get_parsed_fieldname(self) -> str:
        return 'resolution'

    def _parse_table_row(self, row: str) -> Tuple[int, int]:
        resolutions: List[Tuple[int, int]] = [
            tuple(int(resol_part.replace(",", "")) for resol_part in re.split(r'[x×]', resol))
            for resol in re.findall(resolution_pattern, row)]
        return max(*resolutions, key=lambda pair: pair[0]*pair[1]) if len(resolutions) > 1 else resolutions[0]


class MatrixSizeParser(OptyczneSingleFieldParser):
    def _get_parsed_fieldname(self) -> str:
        return 'matrix_size'

    def _parse_table_row(self, row: str) -> Tuple[float, float]:
        # if fails search for: https://fotoblogia.pl/rodzaje-i-wielkosci-matryc-wszystko-co-powinienes-wiedziec-poradnik,6793597927618689a
        match = matrix_pattern.search(row)
        return float(match.group(1)), float(match.group(2))


class ISOParser(OptyczneSingleFieldParser):
    def _get_parsed_fieldname(self) -> str:
        return 'iso_range'

    def _parse_table_row(self, row: str) -> Tuple[float, float]:
        return tuple(int(iso) for iso in re.split(r'[-–]', re.search(iso_range_pattern, row).group()))


class ShutterParser(OptyczneTableParser):
    mechanical_name: ParsedFieldName = ParsedFieldName('inverse_mechanical_shutter')
    electronic_name: ParsedFieldName = ParsedFieldName('inverse_electronic_shutter')

    def parse(self, row: str) -> Iterable[Tuple[ParsedFieldName, Optional[int]]]:
        mechanical_match = mechanical_shutter_pattern.search(row)
        electronic_match = electronic_shutter_pattern.search(row)
        shutter_speeds: List[str] = re.findall(shutter_speed_pattern, row)
        if len(shutter_speeds) > 0:
            try:
                if not (mechanical_match or electronic_match):
                    return [(self.mechanical_name, int(shutter_speeds[0])), (self.electronic_name, None)]

                mechanical_parse: Optional[int] = min(int(speed) for speed in shutter_speeds) if mechanical_match else None
                electronic_parse: Optional[int] = max(int(speed) for speed in shutter_speeds) if electronic_match else None
                return [(self.mechanical_name, mechanical_parse), (self.electronic_name, electronic_parse)]
            except Exception as e:
                raise OptyczneSubparserException([self.mechanical_name, self.electronic_name], e)


class WeightParser(OptyczneSingleFieldParser):
    def _get_parsed_fieldname(self) -> str:
        return 'weight'

    def _parse_table_row(self, row: str) -> int:
        return max(int(weight) for weight in re.findall(weight_pattern, row))


class DimensionsParser(OptyczneSingleFieldParser):
    def _get_parsed_fieldname(self) -> str:
        return 'dimensions'

    def _parse_table_row(self, row: str) -> Tuple[float, float, float]:
        return tuple(float(dim) for dim in re.findall(dimension_pattern, row))
