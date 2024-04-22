from dash.dependencies import Input, Output, State
from .utils import get_data, save_zip
from dash.exceptions import PreventUpdate
from flask_login import current_user

def register_callbacks(app):
    @app.callback(
        Output('table-paging-with-graph', 'data'),
        [Input('table-paging-with-graph', "page_current"),
         Input('table-paging-with-graph', "page_size"),
         Input('df-household', 'value'),
         Input('df-data', 'value')],
         prevent_initial_callback=True
    )
    def update_table(page_current=0, page_size=100, selected_hshd_num=10, data='8451_sample'):
        if page_current is None:
            page_current = 0
        if page_size is None:
            page_size = 100
        if selected_hshd_num is None:
            selected_hshd_num = 10
        if data is None:
            data = "8451_sample"
        
        df = get_data(folder=data)
        filtered_df = df[df['HSHD_NUM'] == selected_hshd_num]
        sorted_df = filtered_df.sort_values(by=['HSHD_NUM', 'BASKET_NUM', 'DATE', 'PRODUCT_NUM', 'DEPARTMENT', 'COMMODITY'])
        return sorted_df.iloc[page_current*page_size:(page_current+1)*page_size].to_dict('records')
    
    @app.callback(
            Output('upload-status', 'children'),
            [Input('upload-data', 'contents')],
            [State('upload-data', 'filename')],
            prevent_initial_callback=True
    )
    def upload_file(contents, filename):
        if contents is None:
            raise PreventUpdate
        return save_zip(contents, filename, current_user.first_name)
