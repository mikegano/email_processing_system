# app/parsers/base_parser.py

from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def can_parse(self, source):
        """Determine if this parser can handle the given source."""
        pass

    @abstractmethod
    def parse(self, source):
        """Parse the source and return extracted data."""
        pass
