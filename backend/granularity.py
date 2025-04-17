from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any
import math

def calculate_granularity(start_date: str, end_date: str) -> str:
    """
    Calculate appropriate time granularity based on the timeframe.
    
    Args:
        start_date: Start date in format 'DD-MM-YYYY'
        end_date: End date in format 'DD-MM-YYYY'
    
    Returns:
        String representing the time granularity (e.g., '30min', '1h', '4h', '1d', '1w')
    """
    # Parse dates
    start = datetime.strptime(start_date, '%d-%m-%Y')
    end = datetime.strptime(end_date, '%d-%m-%Y')
    
    # Calculate the difference in days
    delta_days = (end - start).days
    
    # Define granularity based on the timeframe
    if delta_days <= 1:
        return '30min'  # 30-minute intervals for 1 day
    elif delta_days <= 7:
        return '2h'     # 2-hour intervals for a week
    elif delta_days <= 30:
        return '8h'     # 8-hour intervals for a month
    elif delta_days <= 90:
        return '1d'     # 1-day intervals for 3 months
    elif delta_days <= 180:
        return '2d'     # 2-day intervals for 6 months
    elif delta_days <= 365:
        return '1w'     # 1-week intervals for a year
    else:
        return '2w'     # 2-week intervals for more than a year

def generate_time_intervals(start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """
    Generate time intervals based on the calculated granularity.
    
    Args:
        start_date: Start date in format 'DD-MM-YYYY'
        end_date: End date in format 'DD-MM-YYYY'
    
    Returns:
        List of dictionaries containing start and end timestamps for each interval
    """
    granularity = calculate_granularity(start_date, end_date)
    
    # Parse dates
    start = datetime.strptime(start_date, '%d-%m-%Y')
    end = datetime.strptime(end_date, '%d-%m-%Y') + timedelta(days=1) - timedelta(seconds=1)
    
    intervals = []
    current = start
    
    # Map granularity to timedelta
    if granularity == '30min':
        delta = timedelta(minutes=30)
    elif granularity == '1h':
        delta = timedelta(hours=1)
    elif granularity == '2h':
        delta = timedelta(hours=2)
    elif granularity == '4h':
        delta = timedelta(hours=4)
    elif granularity == '8h':
        delta = timedelta(hours=8)
    elif granularity == '12h':
        delta = timedelta(hours=12)
    elif granularity == '1d':
        delta = timedelta(days=1)
    elif granularity == '2d':
        delta = timedelta(days=2)
    elif granularity == '1w':
        delta = timedelta(weeks=1)
    elif granularity == '2w':
        delta = timedelta(weeks=2)
    else:
        delta = timedelta(days=1)  # Default to daily
    
    # Generate intervals
    while current < end:
        interval_end = min(current + delta, end)
        intervals.append({
            'start': current,
            'end': interval_end,
            'start_timestamp': int(current.timestamp()),
            'end_timestamp': int(interval_end.timestamp())
        })
        current = interval_end
    
    return intervals

def get_appropriate_data_points(start_date: str, end_date: str, max_points: int = 100) -> Tuple[str, int]:
    """
    Determine the appropriate granularity and number of data points to fetch.
    
    Args:
        start_date: Start date in format 'DD-MM-YYYY'
        end_date: End date in format 'DD-MM-YYYY'
        max_points: Maximum number of data points to return
    
    Returns:
        Tuple containing granularity and number of points
    """
    start = datetime.strptime(start_date, '%d-%m-%Y')
    end = datetime.strptime(end_date, '%d-%m-%Y')
    
    delta_days = (end - start).days
    granularity = calculate_granularity(start_date, end_date)
    
    # Calculate how many points would be generated with the current granularity
    if granularity == '30min':
        points = delta_days * 48
    elif granularity == '1h':
        points = delta_days * 24
    elif granularity == '2h':
        points = delta_days * 12
    elif granularity == '4h':
        points = delta_days * 6
    elif granularity == '8h':
        points = delta_days * 3
    elif granularity == '12h':
        points = delta_days * 2
    elif granularity == '1d':
        points = delta_days
    elif granularity == '2d':
        points = delta_days // 2
    elif granularity == '1w':
        points = delta_days // 7
    elif granularity == '2w':
        points = delta_days // 14
    else:
        points = delta_days
    
    # Adjust if we have too many points
    if points > max_points:
        # Find the appropriate granularity
        if delta_days <= 7:
            return '1h', min(delta_days * 24, max_points)
        elif delta_days <= 30:
            return '4h', min(delta_days * 6, max_points)
        elif delta_days <= 90:
            return '12h', min(delta_days * 2, max_points)
        elif delta_days <= 180:
            return '1d', min(delta_days, max_points)
        elif delta_days <= 365:
            return '2d', min(delta_days // 2, max_points)
        else:
            return '1w', min(delta_days // 7, max_points)
    
    return granularity, points