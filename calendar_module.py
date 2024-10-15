import datetime
import calendar

def get_first_last_days():
    # Get the current date
    current_date = datetime.date.today()

    # Calculate the first day of the month 5 months ago 
    past_year, past_month = current_date.year, current_date.month
    for _ in range(5):  # For 5 months
        if past_month == 1:
            past_month = 12
            past_year -= 1
        else:
            past_month -= 1
    past_first_day = datetime.date(past_year, past_month, 1)

    # Calculate the last day of the current month
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    current_month_last_day = datetime.date(current_date.year, current_date.month, last_day)

    # Format the dates to the desired format
    past_month_first_day_str = past_first_day.strftime('%Y-%m-%d')
    current_month_last_day_str = current_month_last_day.strftime('%Y-%m-%d')

    # Generate list of year-month labels from 5 months ago to the next month
    year_month_labels = []
    year, month = past_year, past_month
    for _ in range(7):  # Including the current month and the next month
        year_month_labels.append(f"{year}-{str(month).zfill(2)}")
        month += 1
        if month > 12:
            month = 1
            year += 1

    return past_month_first_day_str, current_month_last_day_str, year_month_labels


'''
If the current date is August 20, 2024:

past_month_first_day_str is "2024-03-01"
current_month_last_day_str is "2024-08-31"
year_month_labels is ["2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]

'''