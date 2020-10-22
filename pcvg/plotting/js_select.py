# JS_select.py

# Provide a string containing javascript that is used when visualizing the points selected ib a bokeh plot
def js_select(with_expt=False):
    """
        Provides a string of JS code that can be used to update a Table of selected values that is part of the parent plot
        largely based on https://github.com/surfaceowl-ai/python_visualizations/blob/main/notebooks/bokeh_save_linked_plot_data.ipynb
        essentially, the indices of the selectd points are used to populate a second data source and hence the DataTable

        if 'with_expt' is True, the JS code will also retrieve the experiment number and update it
    """
    
    if with_expt:
        js_code = """
            var inds = cb_obj.indices;
            var d1 = s1.data;
            var d2 = s2.data;
            d2['f'] = []
            d2['rt'] = []
            d2['mz'] = []
            d2['v'] = []
            d2['x'] = []

            for (var i = 0; i < inds.length; i++) {
                d2['f'].push(d1['index'][inds[i]])
                d2['rt'].push(d1['rt'][inds[i]])
                d2['mz'].push(d1['mz'][inds[i]])
                d2['x'].push(d1['expt'][inds[i]])
                d2['v'].push(d1[v_field][inds[i]])
            }
            s2.change.emit();
            table.change.emit();
        """
    else:    
        js_code = """
            var inds = cb_obj.indices;
            var d1 = s1.data;
            var d2 = s2.data;
            d2['f'] = []
            d2['rt'] = []
            d2['mz'] = []
            d2['v'] = []

            for (var i = 0; i < inds.length; i++) {
                d2['f'].push(d1['index'][inds[i]])
                d2['rt'].push(d1['rt'][inds[i]])
                d2['mz'].push(d1['mz'][inds[i]])
                d2['v'].push(d1[v_field][inds[i]])
            }
            s2.change.emit();
            table.change.emit();
        """
    return js_code