# get_tool_tips_format

# TOOLTIPS is html code that defines the way the HoverTool displays data points.
# Ideally this would not be hardcoded but would be written by code

def get_tool_tips_format(with_expt=False):
    """
        Provides two versions of the html code used to display the tool_tips generated by the hover tool
        
        One version includes the experiment number (useful for SWATH data) and the other doesn't
    """
    if with_expt:
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
                    <span style="font-size: 12px;">Expt:</span>
                    <span style="font-size: 12px;">@expt</span>
                </div>
                <div>
                    <span style="font-size: 12px;">Non_zero:</span>
                    <span style="font-size: 12px;">@non_zero</span>
                </div>
           </div>
        """ 
    else:
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
 
    return TOOLTIPS