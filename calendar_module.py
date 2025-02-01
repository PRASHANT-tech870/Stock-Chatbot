from datetime import datetime, timedelta

def get_first_last_days():
    today = datetime.now()
    
    # Get current month's last day
    current_month_last_day = today.replace(day=1)
    current_month_last_day = (current_month_last_day.replace(month=current_month_last_day.month % 12 + 1, day=1) if current_month_last_day.month < 12 
                             else current_month_last_day.replace(year=current_month_last_day.year + 1, month=1, day=1)) - timedelta(days=1)
    
    # Get 6 months ago first day (instead of just last month)
    past_month_first_day = today.replace(day=1)
    for _ in range(6):  # Go back 6 months
        past_month_first_day = (past_month_first_day - timedelta(days=1)).replace(day=1)
    
    # Create consecutive month labels
    months = []
    date = past_month_first_day
    while date <= current_month_last_day:
        months.append(date.strftime('%Y-%m'))
        # Move to next month
        if date.month == 12:
            date = date.replace(year=date.year + 1, month=1)
        else:
            date = date.replace(month=date.month + 1)
    
    return (past_month_first_day.strftime('%Y-%m-%d'), 
            current_month_last_day.strftime('%Y-%m-%d'),
            months)


'''
If the current date is August 20, 2024:

past_month_first_day_str is "2024-03-01"
current_month_last_day_str is "2024-08-31"
year_month_labels is ["2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]

'''