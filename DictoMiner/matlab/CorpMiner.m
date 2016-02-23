classdef CorpMiner < handle
    %CORPMINER Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        wrds = {}; wrds_n = 0;
        chars = ''; chars_n = 0;
        labs = {}; labs_n = 0;
        labs_lut = []; labs_conv = [];
        lens = [];
    end
    
    
    methods (Static)
        
        % --------------------------------------------------------------- %
        
        function bing()
            dbWrds = BingBody();
            
            dbWrds = CorpMiner.preproc(dbWrds);
            CorpMiner.all(dbWrds);
        end
        
        function diceware()
            dbWrds = diceware();
            
            dbWrds = CorpMiner.preproc(dbWrds);
            CorpMiner.all(dbWrds);
        end
        
        function anc()
            dbWrds = ANC.tokens();
            
            dbWrds = CorpMiner.preproc(dbWrds);
            CorpMiner.all(dbWrds);
        end
        
        % --------------------------------------------------------------- %
        
        % prepare the database for processing
        function dbWrds = preproc(dbWrds)
            % remove words that contain non-alphanumeric characters
            nWrds = length(dbWrds); bLocs = false(1,nWrds);
            progress.bar('Preprocssing Words');
            for i = 1:nWrds
                [~,bad] = StringHandler.remchar_alpha(dbWrds(i).string);
                if ~isempty(bad), bLocs(i) = true; end
                progress.bar(i/nWrds);
            end
            dbWrds(bLocs) = [];
        end
        
        % run all available functions
        function all(dbWrds)
            tObj = CorpMiner(dbWrds);
            
            tObj.dist_letter();
            tObj.map_biletter();
            tObj.dist_wordlen();
            tObj.map_letterfreq();
            tObj.map_wordletter();
        end
        
        % --------------------------------------------------------------- %
        
    end
    
    
    methods
        
        % --------------------------------------------------------------- %
        
        function tObj = CorpMiner(dbWrds)
            % gather all words
            tObj.wrds = {dbWrds.string};
            tObj.wrds_n = length(tObj.wrds);
            % gather all characters and remove non-letters
            tObj.chars = [tObj.wrds{:}];
            tObj.chars_n = length(tObj.chars);
            % reduce to unique character set
            tObj.labs = unique([tObj.chars,' ']);
            tObj.labs_n = length(tObj.labs);
            % setup label LUT
            tObj.labs_conv = double(tObj.labs);
            tObj.labs_lut = zeros(1,max(tObj.labs_conv));
            tObj.labs_lut(tObj.labs_conv) = 1:tObj.labs_n;
            % get word lengths
            tObj.lens = [dbWrds.length];
        end
        
        % --------------------------------------------------------------- %
        
        % show letter frequency distribution
        function dist_letter(tObj)
            % get single letter distribution
            charconv = double(tObj.chars);
            edges = double(tObj.labs);
            vals = histc(charconv,edges);
            
            % attempt to normalize
            switch 1
                case 1
                    norm_str = 'Percentage';
                    norm_val = tObj.chars_n;
                case 2
                    %norm_str = 'Word Length';
                    %norm_val = len;
                otherwise
                    norm_str = 'None';
                    norm_val = 1;
            end
            vals = vals/norm_val;
            
            % sort by frequency
            [vals_sort,ix] = sort(vals,'descend');
            edges_sort = char(edges(ix));
            
            
            % plot single letter distribution
            getFig('Letter Analysis',1);
            bar(1:tObj.labs_n,vals_sort); axis('tight');
            set(gca,'XTick',1:tObj.labs_n,'XTickLabel',{edges_sort'});
            xlabel('Letter'); ylabel('Frequency');
            title(['Letter Distribution | Norm: ' norm_str]);
        end
        
        
        % show word length distribution
        function dist_wordlen(tObj)
            lens_vec = tObj.lens;
            
            % get word length distribution
            len_max = max(lens_vec);
            edges = 1:len_max;
            len_dist = histc(lens_vec,edges);
            
            % attempt to normalize
            switch 1
                case 1
                    norm_str = 'Percentage';
                    norm_val = tObj.wrds_n;
                otherwise
                    norm_str = 'None';
                    norm_val = 1;
            end
            len_dist = len_dist/norm_val;
            
            
            % plot length distribution
            getFig('Length Analysis',1);
            bar(edges,len_dist); axis('tight');
            set(gca,'XTick',1:len_max,'XTickLabel',{1:len_max});
            xlabel('Length'); ylabel('Frequency');
            title(['Word Length Distribution | Norm: ' norm_str]);
            xmax = round(mean(lens_vec)+5*std(lens_vec));
            xlim([0,xmax]);
        end
        
        % --------------------------------------------------------------- %
        
        % show bi-letter connectivity distribution
        function map_biletter(tObj)
            labs_i = tObj.labs;
            
            % get single letter distribution
            charconv = double(tObj.chars);
            edges = double(tObj.labs);
            vals = histc(charconv,edges);
            
            % get frequency matrix (for normalization)
            vals(1) = sum(vals);
            fMat = zeros(tObj.labs_n);
            for i = 1:tObj.labs_n
                for j = 1:tObj.labs_n
                    cFreq = vals(i) + vals(j);
                    fMat(j,i) = 1/cFreq;
                end
            end
            
            
            % get bi-letter connectivity
            progress.bar('Mapping Bi-Connectivity');
            bcMat = zeros(tObj.labs_n);
            for iWrd = 1:tObj.wrds_n
                cWrd = double([' ',tObj.wrds{iWrd},' ']);
                len = length(cWrd);
                
                % get current/next letters for each word
                for iChar = 1:len-1
                    % use LUT to find current/next indices for given tag
                    iStart = tObj.labs_lut(cWrd(iChar));
                    iStop = tObj.labs_lut(cWrd(iChar+1));
                    % skip if either character is not valid
                    if (iStart <= 0) || (iStop <= 0), continue; end
                    
                    % attempt to normalize?
                    switch 1
                        case 1
                            norm_str = 'Letter Frequency';
                            norm_val = fMat(iStop,iStart);
                        case 2
                            norm_str = 'Word Length';
                            norm_val = 1/len;
                        otherwise
                            norm_str = 'None';
                            norm_val = 1;
                    end
                    
                    bcMat(iStop,iStart) = bcMat(iStop,iStart) + norm_val;
                end
                progress.bar(iWrd/tObj.wrds_n);
            end
            
            
            % plot bi-letter heatmap
            pData = max(bcMat,1e-6); %pData = log10(pData);
            pData = (pData-min(pData(:)))/(max(pData(:))-min(pData(:)));
            getFig('Bi-Letter Analysis',1);
            imagesc(pData); axis('xy');
            set(gca,'XTick',1:tObj.labs_n,'XTickLabel',{labs_i'});
            set(gca,'YTick',1:tObj.labs_n,'YTickLabel',{labs_i'});
            xlabel('Current Letter'); ylabel('Next Letter');
            title(['Bi-Letter HeatMap | Norm: ' norm_str]);
        end
        
        
        % show letter frequency for different locations in words
        function map_letterfreq(tObj)
            % get single letter distribution (for normalization)
            char_conv = double(tObj.chars);
            char_edges = double(tObj.labs);
            char_dist = histc(char_conv,char_edges);
            char_norm = 1./char_dist;
            
            % get letter location frequency
            len_max = max(tObj.lens);
            llMat = zeros(len_max,tObj.labs_n);
            for iWrd = 1:tObj.wrds_n
                cWrd = double(tObj.wrds{iWrd});
                len = length(cWrd);
                
                % add letter location to running total for each letter
                for iChar = 1:len
                    % use LUT to find character index
                    iLoc = tObj.labs_lut(cWrd(iChar));
                    
                    % attempt to normalize
                    switch 1
                        case 1
                            norm_str =  'Letter Frequency';
                            norm_val = char_norm(iLoc);
                        case 2
                            % by word length
                            norm_str =  'Word Length';
                            norm_val = 1/len;
                        otherwise
                            norm_str = 'None';
                            norm_val = 1;
                    end
                    
                    llMat(iChar,iLoc) = llMat(iChar,iLoc) + norm_val;
                end
            end
            
            
            % plot location heatmap
            getFig('Location Analysis',1);
            imagesc(llMat); axis('xy');
            set(gca,'XTick',1:tObj.labs_n,'XTickLabel',{tObj.labs'});
            set(gca,'YTick',1:len_max,'YTickLabel',{1:len_max});
            xlabel('Letter'); ylabel('Location in Word');
            title(['Letter Location HeatMap | Norm: ' norm_str]);
            ymax = round(mean(tObj.lens)+2*std(tObj.lens));
            ylim([0.5,ymax]);
        end
        
        
        % show letter frequency for different word lengths
        function map_wordletter(tObj)
            % get length statistics
            len_vec = tObj.lens;
            len_avg = mean(len_vec);
            len_dev = std(len_vec);
            len_max = max(len_vec);
            % calculate lenght distribution
            len_bins = [1:len_avg+5*len_dev,len_max];
            len_bins_n = length(len_bins);
            if 0
                len_dist = histc(len_vec,len_bins);
                bar(len_bins(1:end-1),len_dist(1:end-1))
            end
            
            % calculate letter frequency for each word length bin
            progress.bar('Analyzing Word Length');
            fMat = zeros(tObj.labs_n,len_bins_n);
            for iBin = 1:len_bins_n-1
                % find words of given length and convert to char array
                cInds = (len_vec >= len_bins(iBin) & len_vec < len_bins(iBin+1));
                wrds_i = tObj.wrds(cInds);
                chars_i = [wrds_i{:},' '];
                
                % figure out frequency distribution of char array
                char_conv = double(chars_i);
                char_edges = double(tObj.labs);
                char_dist = histc(char_conv,char_edges);
                %char_norm = 1./char_dist;
                
                % attempt to normalize
                switch 1
                    case 1
                        norm_str = 'Letter Set';
                        norm_val = length(chars_i);
                    case 2
                        norm_str = 'Word Set';
                        norm_val = length(wrds_i);
                    otherwise
                        norm_str = 'None';
                        norm_val = 1;
                end
                vals = char_dist/norm_val;
                
                % add value for each character to the matrix
                for iChar = 1:tObj.labs_n
                    iLoc = tObj.labs_lut(char_edges(iChar));
                    fMat(iLoc,iBin) = fMat(iLoc,iBin) + vals(iChar);
                end
                
                progress.bar(iBin/(len_bins_n-1));
            end
            
            
            % plot single letter distribution
            getFig('Word Analysis',1);
            imagesc(fMat); axis('xy');
            set(gca,'XTick',len_bins,'XTickLabel',{len_bins});
            set(gca,'YTick',1:tObj.labs_n,'YTickLabel',{tObj.labs'});
            xlabel('Word Length'); ylabel('Letter');
            title(['Word Length Letter Distribution | Norm: ' norm_str]);
        end
        
        % --------------------------------------------------------------- %
        
    end
    
end

