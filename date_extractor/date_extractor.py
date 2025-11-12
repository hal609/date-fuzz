import re
from .date_extraction_classes import *

date_time_patterns_dict = {
    # 1. Full/Abbreviated Day Names (e.g., Mon, Monday)
    re.compile(r'\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b', re.IGNORECASE): IndicatorType.DAY,

    # 2. Full/Abbreviated Month Names (e.g., Jan, January)
    re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December)\b', re.IGNORECASE): IndicatorType.MONTH,

    # 3. Numeric Dates (e.g., 12/31/2025, 2025-12-31, 12.31.25)
    # Matches common DD/MM/YYYY, MM-DD-YY, or YYYY.MM.DD formats
    re.compile(r'\b\d{1,4}[-/.\\]\d{1,2}[-/.\\]\d{2,4}\b'): IndicatorType.DATE,

    # 4. Standalone Years (e.g., 1999, 2024)
    re.compile(r'\b(?:19|20)\d{2}\b'): IndicatorType.YEAR,

    # 5. Times (e.g., 10:30, 10:30:45)
    re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?\b'): IndicatorType.TIME,

    # 6. AM/PM Indicators (e.g., 10:30 am, 10 am, 5PM)
    re.compile(r'\b\d{1,2}(?::\d{2})?\s?(?:am|pm)\b', re.IGNORECASE): IndicatorType.TIME,

    # 7. Ordinal Dates (e.g., 1st, 22nd, 30th)
    re.compile(r'\b\d{1,2}(?:st|nd|rd|th)\b', re.IGNORECASE): IndicatorType.DAY,

    # 8. Relative/Descriptive Time Words (e.g., today, tomorrow, ago, noon)
    re.compile(r'\b(?:noon|midnight|o\'clock|ago|now)\b', re.IGNORECASE): IndicatorType.TIME,

    re.compile(r'\b(?:today|tomorrow|yesterday|later|next day|same day|that day|following day|day later)\b', re.IGNORECASE): IndicatorType.DAY,

    # 9. Time Zones (e.g., UTC, EST, PDT)
    re.compile(r'\b(?:GMT|UTC|EST|PST|CST|EDT|PDT|CDT)\b', re.IGNORECASE): IndicatorType.TIME
}

def find_date_time_indicators(text):
    found_list = []
    for pattern in date_time_patterns_dict.keys():
        matches = pattern.findall(text)
        for match in matches:
            found_list.append(DateIndicator(match, 0, date_time_patterns_dict[pattern]))
    return found_list


def find_dates(text):
    # Check for multiples of the same token
    token_counts = {}
    found_indicators = find_date_time_indicators(text)
    found_tokens = [indicator.token for indicator in found_indicators]
    for entry in found_tokens:
        token_counts[entry] = found_tokens.count(entry)

    token_running_counts = {}
    for token in token_counts.keys():
        token_running_counts[token] = 0

    words = text.split()
    found_indicators = find_date_time_indicators(text) 

    tokens = []
    for indicator in found_indicators:
        token, token_type = indicator.token, indicator.time_type
        for i, w in enumerate(words):
            if token in w:
                if token_running_counts[token] == token_counts[token]: break
                token_running_counts[token] += 1
                tokens.append(DateIndicator(token, i, token_type))
                if token_running_counts[token] == token_counts[token]: break

    groups = group_tokens(text, tokens)
    formatted_groups = format_token_groups(groups)

    return formatted_groups

def group_tokens(text, tokens):
    words = text.split()

    # Define connecting words that can bridge gaps of 2
    connecting_words = {"of", "the", "at", "on", "in"}

    # Sort tokens by position
    sorted_tokens = sorted(tokens, key=lambda x: x.pos)

    groups = []
    current_group = [sorted_tokens[0]]

    for i in range(1, len(sorted_tokens)):
        prev_token = sorted_tokens[i - 1]
        curr_token = sorted_tokens[i]
        distance = curr_token.pos - prev_token.pos

        if distance == 1:
            # Adjacent → same group
            current_group.append(curr_token)
        elif distance == 2:
            # Check if the in-between word is a connecting word
            between_word = words[prev_token.pos + 1].strip(",.")
            if between_word.lower() in connecting_words:
                current_group.append(curr_token)
            else:
                groups.append(sorted(current_group))
                current_group = [curr_token]
        else:
            # Too far apart → new group
            groups.append(sorted(current_group))
            current_group = [curr_token]

    # Add last group
    if current_group:
        groups.append(sorted(current_group))

    return groups

def format_token_groups(groups):
    formatted_groups = []
    for date in groups:
        composite_date = ""
        for indicator in date:
            if indicator.time_type == IndicatorType.DATE:
                composite_date = indicator.token
                break
            if indicator.time_type == IndicatorType.YEAR:
                composite_date += indicator.token + "-"
            if indicator.time_type == IndicatorType.MONTH:
                composite_date += month_dict[indicator.token.lower()] + "-"
            if indicator.time_type == IndicatorType.DAY:
                composite_date += indicator.token + " "
            if indicator.time_type == IndicatorType.TIME:
                composite_date += indicator.token + " "

        if composite_date[-1] == " " or composite_date[-1] == "-":
            composite_date = composite_date[:-1]
        formatted_groups.append(composite_date)

    return formatted_groups
        