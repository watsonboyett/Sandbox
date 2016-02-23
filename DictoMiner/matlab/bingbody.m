function dbWrd = bingbody
    
    % open file for reading
    fname = '\\scires1\audio\Boyett\_twenty\data\Bing-Apr10.txt';
    fid = fopen(fname,'r');
    
    % get all words in the list
    i = 1; dbWrd = struct();
    while ~feof(fid)
        cline = fgetl(fid);
        if isempty(cline), continue; end
        ct = textscan(cline,'%s');
        
        word = ct{1}{1};
        dbWrd(i,1).index = i;
        dbWrd(i).string = upper(word);
        dbWrd(i).length = length(word);
        
        i = i+1;
    end
    % close file
    fclose(fid);
    
end

