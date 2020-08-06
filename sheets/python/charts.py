from enum import Enum

class ChartType(Enum):
  UNKNOWN = 1
  LINE = 1

_ChartTypeToSheetsChartInfo = {
  ChartType.LINE: {'chartClass': 'basicChart', 'chartType': 'LINE'},
}

class Chart:
  """
  This class is used to configure charts and add them to a spreadsheet.
  """
  def __init__(self, chart_type,
               title='Untitled'):
    """
    @param chart_type The type of chart to add.
    @param title The title to add to the chart.
    """
    self._chart_type = chart_type
    self._sheets_chart_info = _ChartTypeToSheetsChartInfo[self._chart_type]
    self._PrepareBody(title)

  def AddToSpreadsheet(self, sheets_api, spreadsheet_id):
    """
    Uses the provided sheets API service to add the instance of the chart to the
    spreadsheet with the provided ID.
    @param sheets_api The Google sheets API service.
    @param spreadsheet_id The ID of the spreadsheet where the data lives and
        wheare the chart will be added.
    @return The result of the 'addChart' request.
    """
    result = sheets_api.spreadsheets().batchUpdate(
      spreadsheetId=spreadsheet_id, body=self._body).execute()
    return result

  def AddTitle(self, title):
    """
    Sets the title of the chart.
    @param title The title to add to the chart.
    """
    spec = self._GetSpec()
    spec['title'] = title

  def AddDomain(self, range_name):
    """
    """
    # Get sheet_id
    sheet_id = 0
    # Convert range to row/column indexes.
    column = 0
    start_row = 0
    self.AddDomainByIndex(column, start_row, sheet_id)

  def AddDomainByIndex(self, column,
                       start_row=0, sheet_id=0):
    """
    """
    end_row = -1
    source = self._CreateSource(
      sheet_id, start_row, end_row, column, column+1)
    domain = {'sourceRange': {'sources': [source]}}
    chart = self._GetChart()
    # Line charts can only have one domain.
    chart['domains'] = [{'domain': domain}]

  def AddLine(self, range_name):
    """
    """
    # Get sheet_id
    sheet_id = 0
    # Convert range to row/column indexes.
    column = 0
    start_row = 0
    end_row = 0
    self.AddLineByIndex(self, column, start_row, end_row, sheet_id)

  def AddLineByIndex(self, column, start_row,
                     end_row = -1, sheet_id=0):
    """
    """
    end_col = column + 1
    source = self._CreateSource(
      sheet_id, start_row, end_row, column, end_col)
    series = {
      'series': {'sourceRange': {'sources': [source]}},
      'type': 'LINE'
    }
    chart = self._GetChart()
    chart['series'].append(series)

  def ConfigureXaxis(self):
    """
    """
    pass

  def ConfigureYaxis(self):
    """
    """
    pass

  def AddLegend(self, legend_position='RIGHT_LEGEND'):
    """
    """
    chart = self._GetChart()
    chart['legendPosition'] = 'RIGHT_LEGEND'

  def SetPosition(self, range_name,
                  width=600, height=371, offsetX=10, offsetY=10):

  def SetPositionByIndex(self, sheet_id, row_index, column_index,
                         width=600, height=371, offsetX=10, offsetY=10):
    """
    """
    chart_object = self._GetChartObject()
    chart_object['position'] = {
      'overlayPosition': {
        'anchorCell': {
          'sheetId': sheet_id,
          'rowIndex': row_index,
          'columnIndex': column_index,
        },
        'offsetXPixels': offsetX,
        'offsetYPixels': offsetY,
        'widthPixels': width,
        'heightPixels': height,
      },
    }

  def _GetChartObject(self):
    return self._body['requests'][0]['addChart']['chart']

  def _GetSpec(self):
    chart_object = self._GetChartObject()
    return chart_object['spec']

  def _GetChart(self):
    sheets_chart_class = self._sheets_chart_info['chartClass']
    spec = self._GetSpec()
    return spec[sheets_chart_class]

  def _CreateSource(
      self, sheet_id, start_row, end_row, start_col, end_col):
    source = {
      'sheetId': sheet_id,
      'startRowIndex': start_row,
      'startColumnIndex': start_col,
      'endColumnIndex': end_col,
    }
    if (end_row > 0):
      source['endRowIndex'] = end_row
    return source

  def _PrepareBody(self, title):
    # Create the main body.
    self._body = {
      'requests': [{
        'addChart': {
          'chart': {
            'spec': {'title': title}
          }
        }
      }]
    }

    # Update the spec.
    spec = self._GetSpec()
    sheets_chart_class = self._sheets_chart_info['chartClass']
    sheets_chart_type = self._sheets_chart_info['chartType']
    spec[sheets_chart_class] = {
      'chartType': sheets_chart_type,
      'headerCount': 1,
      'axis': [{
        'position': 'BOTTOM_AXIS',
        'title': 'Day',
        'viewWindowOptions': {
          'viewWindowMode': 'PRETTY',
        },
      }, {
        'position': 'LEFT_AXIS',
        'title': 'Emotional Value',
        'viewWindowOptions': {
          'viewWindowMin': 0,
          'viewWindowMax': 10,
          'viewWindowMode': 'EXPLICIT',
        }
      }],
      'domains': [],
      'series': [],
    }
