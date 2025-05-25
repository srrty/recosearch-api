import xml.etree.ElementTree as ET


def parse_xml(text: str) -> ET.Element:
    """XML 문자열을 파싱하여 최상위 Element를 반환합니다."""
    return ET.fromstring(text)