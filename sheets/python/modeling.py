import datetime as dt
import numpy as np

def invert(data):
    num_entries = data['entries']
    headers = data['headers']
    rows = [headers]
    for day in range(num_entries):
        row = []
        for header in headers:
            column_data = data[header]
            row.append(str(data[header][day]))
        rows.append(row)
    return rows

def create_binomial_emotions(start_date, num_days):
    joy = np.random.binomial(10, 0.373, num_days) + 1
    sadness = np.random.binomial(10, 0.440, num_days) + 1
    power = np.random.binomial(10, 0.327, num_days) + 1
    peace = np.random.binomial(10, 0.333, num_days) + 1
    fear = np.random.binomial(10, 0.540, num_days) + 1
    anger = np.random.binomial(10, 0.160, num_days) + 1
    headers = ['Date', 'Joy', 'Sadness', 'Power', 'Peace', 'Fear', 'Anger']
    return invert({
        'entries': num_days,
        'headers': headers,
        'Date': [start_date + dt.timedelta(days=x) for x in range(num_days)],
        'Joy': joy,
        'Sadness': sadness,
        'Power': power,
        'Peace': peace,
        'Fear': fear,
        'Anger': anger,
    })
