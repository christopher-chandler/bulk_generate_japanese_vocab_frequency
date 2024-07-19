# Standard
import re

# Pip
# None

# Custom
# None


re_xml_tag = re.compile(r"<.*?>")  # HTML/XML tags
re_parenthesis = re.compile(r"[(（].*[)）]")  # Handle JP parenthesis too


def preprocess_field(content: str) -> str:
    """
    Performs the following operations on the given field content:
    - Remove HTML/XML tags
    - Remove parenthesis and their contents
    - Replace non-breaking space with actual space
    - Trim leading and trailing whitespace

    :param content: The field's content to preprocess
    :return: The vocab literal
    """

    # Replace non-breaking space
    content = content.replace("&nbsp;", " ")

    # Remove HTML/XML tags (just the tags, keep contents)
    content = re_xml_tag.sub("", content)

    # Remove parenthesis and their contents
    content = re_parenthesis.sub("", content)

    # Strip leading and trailing whitespace
    content = content.strip()

    return content
