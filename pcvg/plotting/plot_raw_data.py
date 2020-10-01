#plot_raw_data.py

from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import HoverTool, ColorBar, LinearColorMapper, LogColorMapper, LogTicker, BasicTicker
from bokeh.palettes import Viridis256, Inferno256
from bokeh.transform import transform

from .set_size_column import set_size_column

def plot_raw_data(feature_df, x, y, x_label, y_label, data_desc, size_field, colour_field, colour_use_log=True, **kwargs):
    
    kwargs.setdefault("plot_width",1200)
    kwargs.setdefault("plot_height", 800)
    
    kwargs.setdefault("size_max", 20)
    kwargs.setdefault("size_use_sqrt", False)
    
    kwargs.setdefault("colour_use_log", True)
    kwargs.setdefault("palette", Viridis256[::-1])
    kwargs.setdefault("line_colour", 'lightblue')
    kwargs.setdefault("fill_alpha", 0.5)
    
    TOOLTIPS = """
        <div>
            <div>
                <span style="font-size: 12px;">@index</span>
            </div>

            <div>
                <span style="font-size: 12px;">m/z:</span>
                <span style="font-size: 12px;">@mz{0.0000}</span>
            </div>
            <div>
                <span style="font-size: 12px;">rt:</span>
                <span style="font-size: 12px;">@rt{(0.00)}</span>
            </div>
             <div>
                <span style="font-size: 12px;">Non_zero:</span>
                <span style="font-size: 12px;">@non_zero</span>
            </div>
       </div>
    """ 
  
    bokeh_source = ColumnDataSource(feature_df)
    
    size_desc = set_size_column(feature_df, size_field, kwargs['size_max'], kwargs["size_use_sqrt"])
    
    colours = kwargs['palette']
    
    if kwargs['colour_use_log']:
        mapper = LogColorMapper(palette=colours, low=1, high=max(feature_df[colour_field]))
        map_type = "log"
        ticker_fn = LogTicker()
    else:
        mapper = LinearColorMapper(palette=colours, low=0, high=max(feature_df[colour_field]))
        map_type = "linear"
        ticker_fn = BasicTicker()       

    # create a new plot with default tools, using figure
    p = figure(plot_width=kwargs['plot_width'], plot_height=kwargs['plot_height'], tooltips=TOOLTIPS)

    # add a circle renderer with x and y coordinates, size, color, and alpha
    p.circle(x, y, source=bokeh_source, size='point_size', line_color=kwargs['line_colour'], 
             fill_color=transform(colour_field, mapper), fill_alpha=kwargs['fill_alpha'])

    # color_bar = ColorBar(color_mapper=mapper, ticker=p.xaxis.ticker, formatter=p.xaxis.formatter,
    color_bar = ColorBar(color_mapper=mapper, height=10, ticker=ticker_fn,
                         location=(0,0), orientation='horizontal')

    p.add_layout(color_bar, 'below')
    
    max_colour_value = feature_df[colour_field].max()

    p.title.text = f"{data_desc}, colour: {map_type} {colour_field} (max: {max_colour_value:.1f}), size: {size_desc}"
    p.xaxis.axis_label = x_label
    p.yaxis.axis_label = y_label

    #p.add_tools(HoverTool(tooltips=[("rt", "@rt"), ("mz", "@mz")]))
    
    return p