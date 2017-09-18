use Understand;
$udbFileName = $ARGV[0]; #../RS17_source_data/RS17_jpestore6/static/source/jforum219.udb
$project = $ARGV[1];      #jforum219
$packageName = $ARGV[2];  #net.jforum
$outfileName = $project . "_all_class.txt";

($db, $status) = Understand::open($udbFileName);
die "Error status: ", $status, "\n" if $status;

open(OUTFILE, ">" . $outfileName);

sub printFile
{
	my @tmpList  = @_;
	foreach $str (@tmpList)
	{
		print OUTFILE $str;
	}
}

my @tmpList;
foreach $class ($db->ents("Class"))
{
	if ($class->metric("CountLineCode") != 0  && index($class->longname(1), $packageName) == 0)
	{
    $oneLineStr = $class->longname(1) . "\n";
    push @tmpList, $oneLineStr;
	}
}
printFile(@tmpList);
print $outfileName . "\n";
