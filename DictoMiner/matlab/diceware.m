


fname = 'C:\users\wboyett\Desktop\diceware_wordlist.txt';
fid = fopen(fname,'r');

i = 1; dbWrd = struct();
while ~feof(fid)
    cline = fgetl(fid);
    if isempty(cline), continue; end
    ct = textscan(cline,'%d %s');
    
    index = ct{1};
    if isempty(index), continue; end
    
    word = ct{2}{1};
    dbWrd(i,1).index = index;
    dbWrd(i).string = word;
    dbWrd(i).length = length(word);
    
    i = i+1;
end

fclose(fid);
