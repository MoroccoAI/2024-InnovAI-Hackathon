import re

def convert_message_to_html(message):
    """
    Converts a formatted message into HTML.
    - Ordered lists are detected by patterns like `1. **Item**`.
    - Unordered lists are detected by patterns like `* **Item**`.
    - Bold text is enclosed in **.

    :param message: The AI-generated message.
    :return: The message converted into HTML.
    """
    html = ""
    lines = message.split("\n")
    in_ordered_list = False
    in_unordered_list = False

    for line in lines:
        line = line.strip()

        # Check for ordered list
        ol_match = re.match(r"^(\d+)\.\s\*\*(.+?)\*\*", line)
        if ol_match:
            if not in_ordered_list:
                if in_unordered_list:
                    html += "</ul>"
                    in_unordered_list = False
                html += "<ol>"
                in_ordered_list = True
            html += f"<li><strong>{ol_match.group(2)}</strong>{line[len(ol_match.group(0)):]}</li>"
            continue

        # Check for unordered list
        ul_match = re.match(r"^\*\s\*\*(.+?)\*\*", line)
        if ul_match:
            if not in_unordered_list:
                if in_ordered_list:
                    html += "</ol>"
                    in_ordered_list = False
                html += "<ul>"
                in_unordered_list = True
            html += f"<li><strong>{ul_match.group(1)}</strong>{line[len(ul_match.group(0)):]}</li>"
            continue

        # Handle closing tags
        if in_ordered_list:
            html += "</ol>"
            in_ordered_list = False
        if in_unordered_list:
            html += "</ul>"
            in_unordered_list = False

        # Convert bold text and append plain text
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        html += f"<p>{line}</p>"

    # Ensure all open tags are closed
    if in_ordered_list:
        html += "</ol>"
    if in_unordered_list:
        html += "</ul>"

    return html
