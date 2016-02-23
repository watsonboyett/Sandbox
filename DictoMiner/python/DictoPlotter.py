

""" Plots statistical information about different lexicons """

import pdb
import numpy as np
import matplotlib.pyplot as plt


class DictoPlotter:
    save_plots = True
    save_dir = r'../images/'

    @staticmethod
    def demo(dm):
        """ run all available functions """
        
        fig = DictoPlotter.plot_letter_dist(dm)
        if (DictoPlotter.save_plots):
            fpath = DictoPlotter.save_dir + '/dist_letter_freq.png'
            fig.savefig(fpath, dpi=600)
        
        fig = DictoPlotter.plot_length_dist(dm)
        if (DictoPlotter.save_plots):
            fpath = DictoPlotter.save_dir + '/dist_word_length.png'
            fig.savefig(fpath, dpi=600)
            
        fig = DictoPlotter.plot_biletter_map(dm)
        if (DictoPlotter.save_plots):
            fpath = DictoPlotter.save_dir + '/map_letter_pairs.png'
            fig.savefig(fpath, dpi=600)
            
        fig = DictoPlotter.plot_letterfreq_map(dm)
        if (DictoPlotter.save_plots):
            fpath = DictoPlotter.save_dir + '/map_letter_freq.png'
            fig.savefig(fpath, dpi=600)
            
        fig = DictoPlotter.plot_wordletter_map(dm)
        if (DictoPlotter.save_plots):
            fpath = DictoPlotter.save_dir + '/map_word_length.png'
            fig.savefig(fpath, dpi=600)

    # --------------------------------------------------------------- #

    @staticmethod
    def plot_letter_dist(dm):
        """ plot single letter frequency distribution """
        
        vals = dm.charset_dist
        labels = dm.charset

        width = 0.8
        inds = np.arange(len(vals)) + 0.5

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.bar(inds, vals, width)
        plt.xticks(inds + width/2.0, labels)
        plt.xlabel('Letter')
        plt.ylabel('Frequency')
        plt.title('Letter Distribution | Norm: {0}'.format(dm.charset_norm))
        plt.tight_layout()
        plt.xlim(min(inds), max(inds))
        plt.show()

        return fig


    @staticmethod
    def plot_length_dist(dm):
        """ plot word length frequency distribution """
        
        vals = dm.wordlen_set_dist
        labels = dm.wordlen_set

        width = 0.8
        inds = np.arange(len(vals)) + 0.5

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.bar(inds, vals, width)
        plt.xticks(inds + width/2.0, labels)
        plt.xlabel('Length')
        plt.ylabel('Frequency')
        plt.title('Word Length Distribution | Norm: {0}'.format(dm.charset_norm))
        plt.tight_layout()
        plt.xlim(min(inds), 26.5)
        plt.show()

        return fig

    # --------------------------------------------------------------- #

    @staticmethod
    def plot_biletter_map(dm):
        """ plot digram (bi-letter) connectivity frequency distribution """
        
        char_labs = list(dm.charset)
        char_n = len(char_labs)
        char_dist = dm.charset_dist
        char_lut = dm.charset_lut

        # get frequency matrix (for normalization)
        vals_sum = np.sum(char_dist)
        char_dist = [x/float(vals_sum) for x in char_dist]
        freq_mat = np.zeros((char_n, char_n))
        for i in xrange(char_n):
            for j in xrange(char_n):
                freq_mat[j,i] = 1/(char_dist[i] + char_dist[j])
        freq_mat[0,0] = 0;

        # get bi-letter connectivity
        blc_mat = np.zeros((char_n, char_n))
        for word_i in xrange(dm.words_n):
            word_cur = [ord(x) for x in dm.words[word_i]]
            word_len = len(word_cur)

            # get current/next letters for each word
            for char_i in xrange(word_len-1):
                # use LUT to find current/next indices for given tag
                cur_i = char_lut[word_cur[char_i]]
                nxt_i = char_lut[word_cur[char_i+1]]

                # attempt to normalize?
                case = 1
                if (case == 1):
                    norm_str = 'Letter Frequency'
                    norm_val = freq_mat[nxt_i,cur_i]
                elif (case == 2):
                    norm_str = 'Word Length'
                    norm_val = 1/word_len
                else:
                    norm_str = 'None'
                    norm_val = 1

                blc_mat[nxt_i,cur_i] = blc_mat[nxt_i,cur_i] + norm_val

        # sort matrix into lex. order
        sort_lex = True
        if sort_lex:
            char_ix = np.argsort(char_labs)
            char_labs = [char_labs[ix] for ix in char_ix]
            blc_mat = blc_mat[np.ix_(char_ix,char_ix)]

        # plot bi-letter heatmap
        pData = blc_mat
        #pData = np.maximum(pData, 1e-6) pData = log10(pData)
        pData = (pData - np.min(pData))/(np.max(pData) - np.min(pData))

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        plt.imshow(pData, aspect='equal', origin='lower', interpolation='nearest')
        #plt.colorbar()
        plt.xticks(range(len(char_labs)), char_labs)
        plt.yticks(range(len(char_labs)), char_labs)
        plt.xlabel('Current Letter')
        plt.ylabel('Next Letter')
        plt.title('Bi-Letter HeatMap | Norm: {0}'.format(norm_str))
        plt.show()
        
        return fig


    # FIXME: this doesn't *seem* to produce accurate results
    @staticmethod
    def plot_letterfreq_map(dm):
        """ plot letter frequency for different locations in words """
        
        char_labs = list(dm.charset)
        char_n = len(char_labs)
        char_dist = dm.charset_dist
        char_lut = dm.charset_lut
        
        char_norm = [1/float(x) for x in char_dist]

        # get letter location frequency
        len_max = np.max(dm.wordlen_list)
        ll_mat = np.zeros((len_max, char_n))
        for word_i in xrange(dm.words_n):
            word_cur = [ord(x) for x in dm.words[word_i]]
            word_len = len(word_cur)

            # add letter location to running total for each letter
            for char_i in xrange(word_len):
                # use LUT to find character index
                iLoc = char_lut[word_cur[char_i]]

                # attempt to normalize
                case = 1
                if (case == 1):
                    norm_str =  'Letter Frequency'
                    norm_val = char_norm[iLoc]
                elif (case == 2):
                    # by word length
                    norm_str =  'Word Length'
                    norm_val = 1/float(word_len)
                else:
                    norm_str = 'None'
                    norm_val = 1

                ll_mat[char_i,iLoc] = ll_mat[char_i,iLoc] + norm_val

        # sort matrix into lex. order
        sort_lex = False
        if sort_lex:
            char_ix = np.argsort(char_labs)
            char_labs = [char_labs[ix] for ix in char_ix]
            ll_mat = ll_mat[np.ix_(range(len_max),char_ix)]
            
        pData = ll_mat
        #pData = (pData - np.min(pData))/(np.max(pData) - np.min(pData))

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        plt.imshow(pData, aspect = 'equal', origin='lower', interpolation='nearest')
        plt.colorbar()
        plt.xticks(range(char_n), char_labs)
        plt.yticks(range(1,len_max), range(1,len_max))
        plt.xlabel('Letter')
        plt.ylabel('Location in Word')
        plt.title('Letter Location HeatMap | Norm: {0}'.format(norm_str))
        ymax = round(np.mean(dm.wordlen_list) + 2*np.std(dm.wordlen_list)) + 0.5
        plt.ylim(0.5, ymax)
        plt.show()
        
        return fig


    @staticmethod
    def plot_wordletter_map(dm):
        """ plot letter frequency for different word lengths """
        
        # get length statistics
        len_vec = np.array(dm.wordlen_list)
        len_avg = np.mean(len_vec)
        len_dev = np.std(len_vec)
        len_max = np.max(len_vec)
        
        # calculate length distribution
        len_bins = np.arange(1, len_avg + 5*len_dev) 
        len_bins_n = len(len_bins)
        if (False):
            len_dist = np.histogram(len_vec, len_bins)
            plt.bar(len_bins[:-1], len_dist[:-1])
            plt.show()

        char_labs = dm.charset
        char_dist = dm.charset_dist
        char_lut = dm.charset_lut

        # calculate letter frequency for each word length bin
        freq_mat = np.zeros((dm.charset_n,len_bins_n))
        for bin_i in range(0, len_bins_n-1):
            # find words of given length and convert to char array
            word_inds = np.nonzero((len_vec >= len_bins[bin_i]) & (len_vec < len_bins[bin_i+1]))[0]
            if len(word_inds) < 1:
                continue
            words = [dm.words[int(i)] for i in word_inds]
            chars = ''.join(words)

            # figure out frequency distribution of char array
            char_conv = np.array([ord(x) for x in chars])
            char_set = np.unique(char_conv)
            char_set = np.append(char_set, char_set[-1]+1)
            char_edges = np.sort(char_set)
            char_dist = np.histogram(char_conv, char_edges)[0]

            # attempt to normalize
            case = 1
            if (case == 1):
                norm_str = 'Letter Set'
                norm_val = len(chars)
            elif (case == 2):
                norm_str = 'Word Set'
                norm_val = len(words)
            else:
                norm_str = 'None'
                norm_val = 1

            char_dist = char_dist / float(norm_val)

            # add value for each character to the matrix
            for char_i in range(len(char_dist)):
                iLoc = char_lut[char_edges[char_i]]
                freq_mat[iLoc,bin_i] = freq_mat[iLoc,bin_i] + char_dist[char_i]

        # sort matrix into lex. order
        sort_lex = True
        if sort_lex:
            char_ix = np.argsort(char_labs)
            char_labs = [char_labs[ix] for ix in char_ix]
            freq_mat = freq_mat[np.ix_(char_ix,range(len_bins_n))]
            
        pData = freq_mat
        #pData = (pData - np.min(pData))/(np.max(pData) - np.min(pData))

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        plt.imshow(pData, aspect = 'equal', origin='lower', interpolation='nearest')
        plt.colorbar()
        xticks = [int(x) for x in len_bins]
        plt.xticks(range(len(len_bins)), xticks)
        plt.yticks(range(len(char_labs)), char_labs)
        plt.xlabel('Word Length')
        plt.ylabel('Letter')
        plt.title('Word Length Letter Distribution | Norm: {0}'.format(norm_str))
        plt.show()
        
        return fig


if __name__ == "__main__":
    import pickle
    
    from ANC import ANC
    from DictoMiner import DictoMiner
    from DictoPlotter import DictoPlotter
    

    reload_data = True
    if (reload_data):
        dicto = ANC.get_dictionary()
        dm = DictoMiner(dicto)
    
        print 'Saving data...'
        fid = open('testing.ser', 'wb')
        pickle.dump(dm, fid, -1)
        fid.close
        print 'Done.'

    print 'Reading data...'
    fid = open('testing.ser', 'rb')
    dm = pickle.load(fid)
    fid.close
    print 'Done.'
    

    try:
        DictoPlotter.demo(dm)
    except Exception as e:
        print e

        import sys
        tb = sys.exc_info()[2]
        pdb.post_mortem(tb)


