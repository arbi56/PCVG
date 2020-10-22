#add_plot_selection_tools.py

from bokeh.models import LassoSelectTool, BoxSelectTool
from bokeh.layouts import row
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn


# Add the selection tools to a Bokeh plot and provide the selection mechanism
def add_plot_selection_tools(p, source, plot_height, v_field, js_code, include_expt_col = False):
    """
        Unfortunately it is not possible to retrieve tha values of data points selected in a Bokeh plot,
        so this code creates a Bokeh data Table, adds it to the plot and provides JS code to transfer the selcted
        value to the table.
        Largely based on https://github.com/surfaceowl-ai/python_visualizations/blob/main/notebooks/bokeh_save_linked_plot_data.ipynb
        
        Parameters
            p - the exsting Bokeh plot
            source - yhe Bokeh datasource used by the plot
            plot_height
            v_field - the field in the data source to use for the 'Value' column in the table
            js_code - the cutom JS code used for selection. 
            include_expt_column - do we want to display the Expt column or not
            
        Returns
            a layout containg the plot and the table
            
        Notes
            The idea is that we create an invisible DataSource (s2) that is linked to a DataTable.
            The job of the JS code is to copy the selected values to S2, and hence the table, so they will be displayed
        
    """
        
    # add the selection tools to the plot
    p.add_tools(LassoSelectTool(), BoxSelectTool())
    
    table_width = 250

    # create the columns and DataTable...link it to the second data source
    columns = [TableColumn(field ="f",  title = "Feature"),
                TableColumn(field ="rt",  title = "RT (min)"),
                TableColumn(field ="mz",  title = "m/z")
              ]
    
    if include_expt_col:
        columns.append(TableColumn(field ="x",  title = "Expt"))
        table_width += 50
    
    columns.append(TableColumn(field ="v",  title = v_field))
    
    # create a second data source to hold the selected values
    s2 = ColumnDataSource(data=dict(rt=[], mz=[], f=[]))

    table = DataTable(source=s2, columns = columns, width = table_width, height = plot_height)
   
    # provide a JavaScript Callback routine;
    source.selected.js_on_change('indices', CustomJS(args=dict(s1=source, s2=s2, table=table, v_field=v_field), code=js_code))

    layout = row(p, table)
    
    return layout