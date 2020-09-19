def get_scaled_copy(data, scaling_type = None):     
    """ Returns a scaled copy of a pandas DataFrame ready for PCA.

    Parematers:
        data - the dataframe to scale...samples in rows and features in columns
        Scaling_type - choice of:
                            'None' - returns a copy without scaling
                            'Pareto' - mean centred and divided by sqrt(std deviation)
                            'Auto' - autoscale - mean and divide bu std dev
                    anything else is assumed to be Mean Centre
    """

    data_copy = data.copy()

    if scaling_type is None:
        return data_copy

    # we take advantage of numpy's vectored operations to deal with entire columns at once
    else:
        # we'll always mean centre the data
        data_scaled = data_copy - data_copy.mean(axis=0)			# axis = 0 indicates to take the mean of each column

        if scaling_type == "Auto":
            data_scaled = data_scaled/data_scaled.std(axis=0)
        elif scaling_type == "Pareto":
            data_scaled = data_scaled/np.sqrt(data_scaled.std(axis=0))

        return data_scaled
        