classdef ANC
    
    methods (Static)
        
        function dbWrds = tokens( )
            %ANC Summary of this function goes here
            %   Detailed explanation goes here
            
            
            % open file for reading
            fname = '\\scires1\audio\Boyett\_twenty\data\ANC\ANC-token-count.txt';
            fid = fopen(fname,'r');
            
            nLines = 240e3;
            
            % get all words in the list
            i = 1; dbWrds(nLines,1).index = -1;
            while ~feof(fid)
                % get and parse current line
                cline = fgetl(fid);
                if isempty(cline), continue; end
                ct = textscan(cline,'%s %d %f');
                
                % save data to db
                word = ct{1}{1};
                dbWrds(i,1).index = i;
                dbWrds(i).string = upper(word);
                dbWrds(i).length = length(word);
                dbWrds(i).count = ct{2};
                dbWrds(i).freq = ct{3};
                
                % increment counter and show progress
                i = i+1;
                progress.bar(i/nLines);
            end
            % close file
            fclose(fid);
            progress.bar(1);
            
            
            % reduce to proper size (last line is TOTAL data)
            dbWrds = dbWrds(1:i-2);
        end
        
    end
    
end
