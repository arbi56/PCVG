#set_size_column.py

import pandas as pd
import numpy as np

def set_size_column(feature_df, col_to_use, max_size=20, size_mode = 'sqrt'):
    """
        Creates a "point_size" column in the features_df DataFrame...this is used to set the size of the glyph for bokeh plotting.
        The size can be based on the column values, their square roots or logs, and is normalized to the largest value in the specified column
        For ln (natural log) and log10, '1' is added to the result

        Parameters:

            feature_df: the DataFrame to add the column to
            col_to_use: the column to base the size on
            max_size: the maximum size of the glyph *default=20)
            size_mode: take the square root of the column before scaling choices are:
                'sqrt' - take the square root
                'ln' - take the natural log (and add 1)
                'log10' - take the base 10 log (and add 1)
                'lin' - use the column 'as is'

        Returns

            a string describing the scaling applied

    """

     #add the 'point_size' column as the poriginal or its square root
    if size_mode == 'sqrt':
        feature_df['point_size'] = np.sqrt(feature_df[col_to_use])
    elif size_mode == 'ln':
        feature_df['point_size'] = np.log(feature_df[col_to_use] + 1) + 1
    elif size_mode == 'log10':
        feature_df['point_size'] = np.log10(feature_df[col_to_use] + 1) + 1
    elif size_mode == 'lin':
        feature_df['point_size'] = feature_df[col_to_use]
    else:
        raise Exception("Unknown size_mode. Choices are 'lin', 'sqrt', 'ln', 'log10'.")

    # get the maximum of the column (or the sqrt)
    max_point_size = feature_df['point_size'].max()

    #normalize to the largest point_size and scale
    feature_df['point_size'] = feature_df['point_size'] * max_size/max_point_size

    # get the largest value in the original column - used only for the descriptive string
    feature_max = max(feature_df[col_to_use])
    
    #generate te description and return it
    desc = f'{col_to_use} (max: {feature_max:.1f})' if size_mode == 'lin' else f'{size_mode}({col_to_use}) (max: {feature_max:.1f})'
    
    return desc