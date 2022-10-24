
from dash.dependencies import Input, Output, State
from dash import Dash, html, dcc
from modules.utils import get_raw_data, show_data
from modules.soil_texture_classification import soil_texture_classification
from dash.exceptions import PreventUpdate

EXTERNAL_STYLESHEET = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEET, suppress_callback_exceptions=True)

server = app.server


INSTRUCTIONS = """
- This is for demonstration purpose only.
- So far it supports excel sheet and csv file.
- Upload an **excel sheet or csv file.**
- Click on **'Transform Data'** Button to process your data.
"""

TRANSFORM_OPTIONS = ["Soil Classification", "Some Other Task"]

app.layout = html.Div(children=[
    html.H1(children='DEMO ETL TOOL', style={'textAlign': 'center'}),
    dcc.Markdown(INSTRUCTIONS, style={'textAlign': 'center'}),
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
            'margin': '20px'
        },
        multiple=False
    ),
    html.Div(id='upload-success'),
    html.Div([
        html.H4("Select Your Task:", style={"margin":'10px'}),    
        dcc.Dropdown(TRANSFORM_OPTIONS, id = 'task-select',
        style={
                'width': '250px',
                'height': '30px',
                'borderWidth': '1px',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            }),
    ]),

    html.Div([
        html.Button("Transform Data", id='btn-transform'),
        html.H4(),
        html.Div(id='output-datatable'),
        html.Button("Download Processed Data", id='btn-download'),
    ], style={"margin":'20px'}),

    
    dcc.Download(id='download-dataframe-as-csv')
])


@app.callback(
    Output('upload-success','children'),
    Input('upload-data','contents'),
    State('upload-data','filename'))
def upload_success(raw_contents, file_name):
    try:
        if raw_contents is not None:
            df = get_raw_data(raw_contents, file_name)
            children = [
            html.H5(file_name),
            html.H5("Data upload successful", style={'color':'green'}),
            html.Hr()]
            return children
    except Exception as e:
        print(e)
        return html.Div([html.H4('There was an error processing this file.', style={"color":"red"})])

@app.callback(
    Output('output-datatable', 'children'),
    Input('btn-transform',"n_clicks"),
    Input('task-select','value'),
    Input('upload-data','contents'),
    State('upload-data','filename'),
    prevent_initial_call=True
)
def transform_fn(n_clicks, task_select, raw_contents, file_name):
    if not n_clicks:
        PreventUpdate
    else:
        if raw_contents is not None:
            df = get_raw_data(raw_contents, file_name)
            if task_select == TRANSFORM_OPTIONS[0]:
                df = soil_texture_classification(df)
            else:
                pass
            return show_data(df)


@app.callback(
    Output('download-dataframe-as-csv', 'data'),
    Input('btn-download',"n_clicks"),
    Input('upload-data','contents'),
    State('upload-data','filename'),
    prevent_initial_call=True
)
def download_fn(n_clicks,  raw_contents, file_name):
    if not n_clicks:
        PreventUpdate
    else:
        if raw_contents is not None:
            df = get_raw_data(raw_contents, file_name)
            df = soil_texture_classification(df)
            output_file_name = f"{file_name.split('.')[0]}_processed.csv"
            return dcc.send_data_frame(df.to_csv, output_file_name, index=False)

if __name__=='__main__':
    app.run_server(debug=True)