import json
import smartsheet


def sheet_columns_json(smartsheet_client, sheet_id):
    column_details = smartsheet_client.Sheets.get_columns(
        sheet_id,
    )

    json_columns = {}
    for column in column_details.data:
        column_name = column.title.lower()
        json_columns[column_name] = {
            "id": column.id,
            "index": column.index,
            "title": column.title,
            "type": column.type.value,
            "validation": column.validation,
            "version": column.version,
            "width": column.width
        }

    return json_columns
