import numpy as np

def process(shots, names, kinds):
    '''
    Return the average and vairance of the pyro-normalized output signal.
    Choppers are ignored.

    Parameters
    ----------
    shots : ndarray
        A 2D ndarray (input index, shot index)
    names : list of str
        A list of input names
    kinds : list of {'channel', 'chopper'}
        Kind of each input

    Returns
    -------
    list
        [ndarray (channels), list of channel names]

    '''
    needed_channels = ['signal','pyro2']
    index_dict = dict()
    for c in needed_channels:
        if c in names:
            index_dict[c]=names.index(c)
    arr = np.ones(shots.shape[1])
    for c in needed_channels:
        if c == 'signal':
            arr = arr*shots[index_dict[c]]
        else:
            arr = arr/shots[index_dict[c]]

    out = np.full(2,np.nan)
    out[0] = np.mean(arr)
    out[1] = np.var(arr)
    out_names = ['pyro2_normed_signal_mean','pyro2_normed_signal_variance']

    return [out, out_names]
