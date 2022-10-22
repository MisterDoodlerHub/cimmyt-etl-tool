
from dash.dependencies import Input, Output, State
from dash import Dash, html, dcc
from modules.output_table import parse_contents, process_data
from dash.exceptions import PreventUpdate

EXTERNAL_STYLESHEET = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEET, suppress_callback_exceptions=True)

server = app.server

app.layout = html.Div(children=[
    dcc.Upload(
        id = 'upload-data',
        children = html.Div([
            'Drag and Drop or ', html.A('Upload Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),

    html.Div(id='output-datatable'),
    html.Button("Download Processed Data", id='btn-download'),
    dcc.Download(id='download-dataframe-as-csv')
])

@app.callback(
    Output('output-datatable','children'),
    Input('upload-data','contents'),
    State('upload-data','filename'),
    State('upload-data','last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children

@app.callback(
    Output('download-dataframe-as-csv', 'data'),
    Input('btn-download',"n_clicks"),
    Input('upload-data','contents'),
    State('upload-data','filename'),
    prevent_initial_call=True
)
def download_fn(n_clicks, raw_data, raw_file_names):
    if not n_clicks:
        PreventUpdate
    else:
        if raw_data is not None:
            children = [
                process_data(c, n) for c, n in zip(raw_data, raw_file_names)
            ]
            
            output_file_name = f"{raw_file_names[0].split('.')[0]}_processed.csv"
            return dcc.send_data_frame(children[0].to_csv, output_file_name, index=False)

if __name__=='__main__':
    app.run_server(debug=True)