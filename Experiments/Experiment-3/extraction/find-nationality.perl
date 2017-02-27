foreach $filename (@ARGV) {
    open(my $fh, '<:encoding(UTF-8)', $filename);


    $line = <$fh>;    
    if($line =~ / is a .*?([A-Z]\w+\s)+.*?\./g) {
	print $filename . "\t" . $1 . "\n";
    } elsif ($line =~ / is an .*?([A-Z]\w+\s)+.*?\./g) {
	print $filename . "\t" . $1 . "\n";
    } elsif ($line =~ / was a .*?([A-Z]\w+\s)+.*?\./g) {
	print $filename . "\t" . $1 . "\n";
    } elsif ($line =~ / was an .*?([A-Z]\w+\s)+.*?\./g) {
	print $filename . "\t" . $1 . "\n";
    } else {
	print "\n";
    }

    close($fh);
}

