import smartsheet

# import smartsheets_user
from smartsheet_connector.model.smartsheet_user import SmartsheetUser
from smartsheet_connector.service.smartsheet_user import build_smartsheet_user

from smartsheet_connector.service.smartsheet_conn import smartsheets_login
from smartsheet_connector.service.smartsheet_columns import sheet_columns_json
# import smartsheets_row


def smartsheets_data_load(dataframe, sheet_id):
    print(dataframe)

    # build smartsheets user from .env
    smartsheets_user = build_smartsheet_user()

    # connect object for smartsheet
    smartsheets_client = smartsheets_login(
        smartsheets_user)

    # neatly package columns
    smartsheets_columns_dict = sheet_columns_json(
        smartsheets_client, sheet_id)
    issue_ids = smartsheets_columns_dict["id"]["id"]

    # build dictionary of existing issues
    smartsheets_sheet = smartsheets_client.Sheets.get_sheet(sheet_id)

    existing_issue_row_id = {}
    for row in smartsheets_sheet.rows:
        for cell in row.cells:
            if cell.column_id == issue_ids:
                existing_issue_row_id[cell.value] = row.id

    # dataframe parsing
    dataframe_columns = dataframe.columns

    # loop over dataframe
    print(f'existing_issue_row_id: {existing_issue_row_id}')
    new_issues_rows = []
    for entry in dataframe.to_dict('records'):
        print(entry)

        # check if issue exists already
        if entry["id"] in existing_issue_row_id:
            print(entry['id'])

            # update existing row in sheet by assigning row id to new row object
            existing_row = smartsheet.models.Row()
            existing_row.id = existing_issue_row_id[entry["id"]]

            for item in entry:
                # check if cell has data within
                if entry[item]:
                    # build new cell
                    new_cell = smartsheet.models.Cell()
                    new_cell.value = entry[item]
                    new_cell.column_id = smartsheets_columns_dict[item]["id"]
                    # Build the row to update
                    existing_row.cells.append(new_cell)

            # Update rows with new data
            updated_row = smartsheets_client.Sheets.update_rows(
                sheet_id,
                [existing_row]
            )

        else:  # add with new issue to sheet
            new_row = smartsheet.models.Row()
            new_row.to_bottom = True

            for item in entry:
                # check if cell has data within
                if entry[item]:
                    new_cell = smartsheet.models.Cell()
                    new_cell.value = entry[item]
                    new_cell.column_id = smartsheets_columns_dict[item]["id"]
                    new_row.cells.append(new_cell)

            new_issues_rows.append(new_row)

    if len(new_issues_rows) != 0:
        print("new rows:", new_issues_rows, sep="\n")
        # add rows to sheet
        response = smartsheets_client.Sheets.add_rows(
            sheet_id,
            new_issues_rows
        )


if __name__ == "__main__":
    pass
