import numpy as np
#import scipy.optimize as opt

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

# Each Channel Averaged

    channel_indicies = [i for i, x in enumerate(kinds) if x == 'channel']
    out = np.full(len(channel_indicies)*2+2+3, np.nan)
    out_index = 0
    out_names = []
    for i in channel_indicies:
        out[out_index] = np.mean(shots[i])
        out_names.append(names[i] + '_mean')
        out_index += 1
        out[out_index] = np.std(shots[i])
        out_names.append(names[i] + '_std')
        out_index += 1

# Shot-Normalized Signal

    needed_channels = ['signal','pyro1','pyro2']
    optional_channels = ['pyro3']
    index_dict = dict()
    for c in needed_channels:
        if c in names:
            index_dict[c]=names.index(c)
        else:
            # a needed channel isn't avalible
            # g.logger.log('error', 'Additional signal channels are needed to normalize signal!')
            return [out, out_names]
    for c in optional_channels:
        if c in names:
            index_dict[c]=names.index(c)
            needed_channels.append(c)

    arr = np.ones(shots.shape[1])
    for c in needed_channels:
        if c == 'signal':
            arr = arr*shots[index_dict[c]]
        else:
            arr = arr/shots[index_dict[c]]
    out[-5] = np.mean(arr)
    out[-4] = np.var(arr)
    out_names.append('p_norm_sig_mean')
    out_names.append('p_norm_sig_var')
    
# Raw and (Bulk) Normalized Photon Counting
    
    high_baseline = 0.016
    low_baseline = -0.019
    #one_photon_max = .02
    num_shots = len(shots[0])
    photon_count = [0,0,0] # 0 = 0 phontons, 1 = 1 photon, -1 = dark count
    for idx in range(len(shots[0])):
        p = shots[0][idx]
        if low_baseline < p < high_baseline:
            photon_count[0]+=1
        elif p >= high_baseline:
            photon_count[1] +=1
        elif p <= low_baseline:
            photon_count[-1]+=1
    # Fish Stats
    # First, use the 0-counts
    zero_adj = (2*photon_count[-1]+photon_count[0])/float(num_shots)
    if zero_adj >= 0.04:
        null_mean = -np.log(zero_adj)
    else:
        null_mean = np.nan
    # The future may hold many things, including more sophisticated algorithems
    # Including using multiple photon counts, etc.
    norm_fac = out[out_names.index('pyro1_mean')]*out[out_names.index('pyro2_mean')]
    out_names.append('raw_0_photon')    
    out_names.append('calc_pp100s_0')
    out_names.append('b_norm_pps_0')
    out[-3] = photon_count[0]+photon_count[-1]
    out[-2] = null_mean*100
    out[-1] = null_mean/norm_fac
    
    return [out, out_names]