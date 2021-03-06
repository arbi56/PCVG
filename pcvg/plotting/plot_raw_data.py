#plot_raw_data.py

from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import HoverTool, ColorBar, LinearColorMapper, LogColorMapper, LogTicker, BasicTicker
from bokeh.palettes import Viridis256
from bokeh.transform import transform

from .set_size_column import set_size_column

#def plot_raw_data(feature_df, x, y, x_label, y_label, data_desc, tool_tips, size_field, colour_field, **kwargs):
def plot_raw_data(feature_df, x, y, x_label, y_label, data_desc, tool_tips, size_field, colour_field, **kwargs):
 
    """
            Generalized interactive scatter plot that encodes one parameter as circle size and another as colour.
            Several parameters have default values that can be overwritten by passing a dictionary as **kwargs, e.g.
                {'plot_height':600}
            
            Parameters
                feature_df - DafaFrame to plot
                x,y - columns to plot
                x_label, y_label - axes labels
                data_desc - basic plot title...will be extended by to reflect settings
                tool_tips - the format for text displayed by the hover tools (see 'get_tool_tips_format for examples')
                size_field -  name of column used to define glyph size
                colour_field - name of column to define glyph colour
            
            Returns
                a plot that can be diplayed with show(p) (Bokeh show command)
                the ColumndataSource used by bokeh (to allow additional processing)
            
            Default parameters are set by adding them to the kwargs dictionary (which need not be specified by the caller) and
            can be overridden by passing a dictionary.
            
            201021
            The tool tips format is now specified by an supplied html string so it can be changed. get_tool_tips_format provides two veariants.       
            The code to add the selection tools and table display is now a separate routine
        
"""

    # default values - 'setdefault' will set the value in the dictionary if it does not already exist, i.e.
    # if a field is passed in a dictionary it will be used preferentially
    kwargs.setdefault("plot_width",1200)
    kwargs.setdefault("plot_height", 800)
    
    kwargs.setdefault("size_max", 20)
    kwargs.setdefault("size_mode", 'sqrt')
    
    kwargs.setdefault("colour_use_log", True)
    kwargs.setdefault("palette", Viridis256[::-1])   #reverse Viridis so it gives yellow->blue
    kwargs.setdefault("line_colour", 'white')
    kwargs.setdefault("fill_alpha", 0.6)
    
    # add a 'point_size' column to the feature DataFrame.
    # the field to use is passed in by the caller
    # the default settings are used for circle size and whether to take the square root; can be overriden with kwargs.
    # the return value is a string that describes the data used for sizing
    size_desc = set_size_column(feature_df, size_field, kwargs['size_max'], size_mode = kwargs["size_mode"])
    
     # define the ColumnDataSource to be used 
    bokeh_source = ColumnDataSource(feature_df)
    
    colours = kwargs['palette']
    
    # set up the colour mapper and axis labelling dependent on log or linear
    if kwargs['colour_use_log']:
        mapper = LogColorMapper(palette=colours, low=1, high=max(feature_df[colour_field]))
        map_type = "log"
        ticker_fn = LogTicker()
    else:
        mapper = LinearColorMapper(palette=colours, low=0, high=max(feature_df[colour_field]))
        map_type = ""
        ticker_fn = BasicTicker()       

    # create a new plot with default tools using figure
    p = figure(plot_width=kwargs['plot_width'], plot_height=kwargs['plot_height'])

    # add a circle renderer with x and y coordinates, size, color, and alpha
    p.circle(x, y, source=bokeh_source, size='point_size', line_color=kwargs['line_colour'], 
             fill_color=transform(colour_field, mapper), fill_alpha=kwargs['fill_alpha'])

    # ColorBar position and size are hardcoded; could also become parameters
    color_bar = ColorBar(color_mapper=mapper, height=10, ticker=ticker_fn,
                         location=(0,0), orientation='horizontal')

    p.add_layout(color_bar, 'below')
    
    p.add_tools(HoverTool(tooltips=tool_tips))
    
    # retrieve the maximum value of the colour field for our title
    max_colour_value = feature_df[colour_field].max()

    p.title.text = f"{data_desc}, colour: {map_type} {colour_field} (max: {max_colour_value:.1f}), size: {size_desc}"
    p.xaxis.axis_label = x_label
    p.yaxis.axis_label = y_label
    
    return p, bokeh_source