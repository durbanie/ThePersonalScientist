#!/usr/bin/env python3
from __future__ import print_function
from charts import Chart, ChartType
from pprint import pprint
from sheets_api_service import build_sheets_api
import modeling
import datetime as dt
import numpy as np

def add_binomial_values(sheets_api, spreadsheet_id, start_date, num_days):
    """
    Add random values for emotions via a binomial distribution.
    """
    test_data = modeling.create_binomial_emotions(start_date, num_days)
    values = test_data
    data = [{'range': 'A1:G30', 'values': values}]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data,
    }
    result = sheets_api.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body).execute()
    print('%s cells updated.' % (result.get('totalUpdatedCells')))

def get_spreadsheet(sheets_api, spreadsheet_id):
    """
    Gets the spreadsheet properties.
    """
    result = sheets_api.spreadsheets().get(
        spreadsheetId=spreadsheet_id).execute()
    return result

def add_summary_chart(sheets_api, spreadsheet_id):
    """
    """
    # Add the full time-series chart.
    chart = Chart(ChartType.LINE, 'Emotional Awareness')
    chart.AddDomainByIndex(column=0, start_row=0, sheet_id=0)
    for i in range(6):
        chart.AddLineByIndex(column=(i+1), start_row=0)
    chart.AddLegend('RIGHT_LEGEND')
    chart.SetPositionByIndex(sheet_id=0, row_index=10, column_index=5)
    chart.AddToSpreadsheet(sheets_api, spreadsheet_id)

def create_emotion_sheet(sheets_api, spreadsheet_id, emotion_column):
    """
    """
    # Get the data from the base sheet.
    base_sheet = 'Form Responses 1'
    range_name = '%s!%s:%s' % (base_sheet, emotion_column, emotion_column)
    result = sheets_api.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])
    title = rows[0][0]  # title is in the first row of the first column.

    # Now, create the new sheet.
    body = {
        'requests': [{
            'addSheet': {
                'properties': {'title': title}
            }
        }]
    }
    result = sheets_api.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body).execute()
    sheet_id = result['replies'][0]['addSheet']['properties']['sheetId']

    # Add the data to the sheet.
    # First construct the data in the list of rows.
    values = []
    for i in range(1000):
        row = []
        num_row = i + 1
        # Add a reference to the date row.
        row.append('=\'%s\'!A%s' % (base_sheet, num_row))
        # Add a reference to the emotion data.
        row.append('=\'%s\'!%s%s' % (base_sheet, emotion_column, num_row))
        values.append(row)

    # Now add the data
    range_name = '%s!A1:B1000' % title
    data = [{'range': range_name, 'values': values}]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data,
    }
    result = sheets_api.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body).execute()

    # Add the summary stats analysis.
    def create_stats_row(stat_label, stat_formula, stat_number_format=''):
        stat_label_value = {'userEnteredValue': {'stringValue': stat_label}}
        stat_formula_value = {
            'userEnteredValue': {'formulaValue': stat_formula},
            'userEnteredFormat': {'horizontalAlignment': 'RIGHT'},
        }
        if stat_number_format:
            stat_formula_value['userEnteredFormat']['numberFormat'] = {
                'type': 'NUMBER',
                'pattern': stat_number_format,
            }
        return {'values': [stat_label_value, stat_formula_value]}
    requests = [{
        'updateCells': {
            'rows': [
                create_stats_row('Range', '=E5&" - "&E6'),
                create_stats_row('Average', '=AVERAGE(B2:B)', '#.00'),
                create_stats_row('Standard Dev', '=STDEV(B2:B)', '#.00'),
                create_stats_row('Minimum', '=MIN(B2:B)'),
                create_stats_row('Maximum', '=MAX(B2:B)'),
            ],
            'fields': 'userEnteredValue,userEnteredFormat',
            'start': {
                'sheetId': sheet_id,
                'rowIndex': 1,
                'columnIndex': 3,
            },
        }
    }]
    result = sheets_api.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={'requests': requests}).execute()

    # Finally, add the charts.
    # Add the full time-series chart.
    chart = Chart(ChartType.LINE, title)
    chart.AddDomainByIndex(column=0, start_row=0, sheet_id=sheet_id)
    chart.AddLineByIndex(column=1, start_row=0, end_row=-1, sheet_id=sheet_id)
    chart.AddLegend('RIGHT_LEGEND')
    chart.SetPositionByIndex(sheet_id=sheet_id, row_index=8, column_index=5)
    chart.AddToSpreadsheet(sheets_api, spreadsheet_id)

    # Add the histogram.

    # Print a nice message.
    print('Created sheet for %s' % title)

# The main entry point.
def main():
    sheets_api = build_sheets_api()

    # My test sheet.
    spreadsheet_id = '1TnFhr6OXs6wTHDvpVFIYiWdIBaRZTZnK6njHQekg7Hg'
    start_date = dt.date(2020, 7, 11)
    num_days = 20
    add_binomial_values(sheets_api, spreadsheet_id, start_date, num_days)
    #add_summary_chart(sheets_api, spreadsheet_id)
    #for column in ['B', 'C', 'D', 'E', 'F', 'G']:
    #    create_emotion_sheet(sheets_api, spreadsheet_id, column)
    create_emotion_sheet(sheets_api, spreadsheet_id, 'B')

    # My data sheet.
    #spreadsheet_id = '1RjISLBakHtvWEpf5K432Zd0__WbOIckMx0-gGlMNBQA'

    #
    #spreadsheet = create_spreadsheet(sheets_api, 'test')
    #print('Spreadsheet ID: %s' % (spreadsheet.get('spreadsheetId')))
    #print(create_random_emotions(dt.datetime(2020, 7, 11), 3))

if __name__ == '__main__':
    main()
