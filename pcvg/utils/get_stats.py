#get_stats.py

def get_stats(feature_df, data_df):
    """
        Adds statistic  columns to feature_df (a Dataframe); used to visualize and/or filter the raw data

        Parameters:

            feature_df: a DataFrame containing the features; the stats columns are added to this
            data_df: a DataFrame containing samples in rows, features in columns and response values in the cells

        Returns
            
            An updated feature DataFrame

        Note: 'non-zero' is a count of the non-zero samples for each feature
    """ 
    # extract column-wise statistics, i.e. across all samples

    feature_df['non_zero'] =  (data_df != 0.0).sum(0)    #since True==1, the sum is the number of fields that are non-zero
    feature_df['mean'] = data_df.mean(axis=0)
    feature_df['median'] = data_df.median(axis=0)
    feature_df['std'] = data_df.std(axis=0)
    
    feature_df['max'] = data_df.max(axis=0)

    return feature_df