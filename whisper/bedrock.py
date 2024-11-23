import re
from datetime import datetime, timedelta

current_day = datetime.now().day
current_month = datetime.now().month
current_year = datetime.now().year
current_hour = datetime.now().hour
current_minute = datetime.now().minute

curr_date = str(current_day) + '/' + str(current_month) + '/' + str(current_year) + ' ' + str(current_hour) + ':' + str(current_minute)


def get_timestamps(prompt):
    # Updated regex to handle "a.m." or "p.m." with or without spaces
    match = re.search(r'(\d{1,2}(?::\d{2})?)\s*(a\.?m\.?|p\.?m\.?)?\s+to\s+(\d{1,2}(?::\d{2})?)\s*(a\.?m\.?|p\.?m\.?)?', prompt, re.IGNORECASE)
    
    if match:
        start_time = match.group(1)
        start_period = match.group(2)  # Can be "am", "pm", or None
        end_time = match.group(3)
        end_period = match.group(4)  # Can be "am", "pm", or None

        # Clean up periods in AM/PM for consistency
        def normalize_period(period):
            return period.replace('.', '').upper() if period else None

        start_period = normalize_period(start_period)
        end_period = normalize_period(end_period)

        # Default assumptions for missing AM/PM
        def add_default_period(time_str, period):
            # Assume AM for times 1-11 if period is missing
            if period is None:
                hour = int(time_str.split(":")[0])
                period = "AM" if 1 <= hour < 12 else "PM"
            return f"{time_str} {period}"

        # Apply default period if not specified
        start_time = add_default_period(start_time, start_period)
        end_time = add_default_period(end_time, end_period)

        # Parse times with assumptions in place
        try:
            # Standardize to datetime objects
            today = datetime.now().date()  # Get the current date
            start_datetime = datetime.strptime(start_time, '%I:%M %p' if ':' in start_time else '%I %p')
            end_datetime = datetime.strptime(end_time, '%I:%M %p' if ':' in end_time else '%I %p')

            # Combine with today's date
            start_full = datetime.combine(today, start_datetime.time())
            end_full = datetime.combine(today, end_datetime.time())

            # Format to 'yyyy-MM-DD HH:mm:ss'
            start_timestamp = start_full.strftime('%Y-%m-%d %H:%M:%S')
            end_timestamp = end_full.strftime('%Y-%m-%d %H:%M:%S')

            return start_timestamp, end_timestamp
        except ValueError:
            print("Error: Could not parse time.")
    
    return None, None

    
# print(get_timestamps("12:00 PM to 1:00 PM"))
# print(get_timestamps("12 PM to 1 PM"))
# print(get_timestamps("12:00 PM to 1 PM"))
# print(get_timestamps("9 am to 5 pm"))
# print(get_timestamps("9 p.m. to 10:00 p.m."))