#set_size_column.py

import pandas as pd
import numpy as np

def set_size_column(feature_df, col_to_use, max_size=20, use_sqrt=True):
    """
        Creates a "point_size" column in the features_df DataFrame...this is used to set the size of the glyph for bokeh plotting.
        The size can be based on the column values  or their square roots, and is normalized to the largest value in the specified column 

        Parameters:

            feature_df: the DataFrame to add the column to
            col_to_use: the column to base the size on
            max_size: the maximum size of the glyph *default=20)
            use_sqrt: take the square root of the column before scaling

        Returns

            a string describing the scaling applied

    """
    #add the 'point_size' column as the poriginal or its square root
    if use_sqrt:
        feature_df['point_size'] = np.sqrt(feature_df[col_to_use])
    else:
        feature_df['point_size'] = feature_df[col_to_use]

    # get the maximum of the colum (or the sqrt)
    max_point_size = feature_df['point_size'].max()

    #normalize to the largest point_size and scale
    feature_df['point_size'] = feature_df['point_size'] * max_size/max_point_size

    # get the largest value in the original column - used only for the descriptive string
    feature_max = max(feature_df[col_to_use])
    
    #generate te description and return it
    desc = f'sqrt({col_to_use}), (max: {feature_max:.1f})' if use_sqrt else f'{col_to_use}, (max: {feature_max:.1f})'
    
    return desc