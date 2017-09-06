use Understand;

$udbFileName = $ARGV[0]; #../RS17_source_data/RS17_jpestore6/static/source/jpetstore6.udb
$packageName = $ARGV[1]; 


@array = split(/\//, $udbFileName);
$len = @array;
$udb = $array[$len - 1];
@tmp = split(/\.udb/, $udb);
$project = $tmp[0];
pop @array;
$dir = join("/", @array);
$outfileName = $dir . "/" . $project . "_interface_parent.csv";
print $outfileName . "\n";


($db, $status) = Understand::open($udbFileName);
die "Error status: ", $status, "\n" if $status;

@classList = $db->ents("Class");
#@absClassList = $db->ents("Abstract Class");
#@allClassList = (@classList, @absClassList);
$len = @classList;
print $len;
#print "@absClassList\n\n";

open(OUTFILE, ">" . $outfileName);

sub printFile
{
	my @tmpList  = @_;
	foreach $str (@tmpList)
	{
		print OUTFILE $str;
	}
}

$index = 0;
foreach $class (@classList)
{
	my @tmpList;
	
	if ($class->metric("CountLineCode") != 0  && index($class->longname(1), $packageName) == 0)
	{	
		my @interfaces = $class->ents("Implement", "Interface");
		if (@interfaces)
		{
			foreach $interface (@interfaces)
			{
				if ($interface->metric("CountLineCode") != 0 && index($interface->longname(1), $packageName) == 0)
				{
					$oneLineStr = $index . "," . "I" . "," .  $interface->longname(1) . "\n";
					push @tmpList, $oneLineStr;
				}
			}
		}
		
	
		my @parents = $class->ents("Extend", "Class");
		if (@parents)
		{
			foreach $parent (@parents)
			{
				if ($parent->metric("CountLineCode") != 0 && index($parent->longname(1), $packageName) == 0)
				{
					$oneLineStr = $index . "," . "P" . "," .  $parent->longname(1) . "\n";
					push @tmpList, $oneLineStr;
				}
			}
		}

=pod
		my @abs_parents = $class->ents("Extend", "Abstract Class");
		if (@abs_parents)
		{
			foreach $abs_parent (@abs_parents)
			{
				if ($abs_parent->metric("CountLineCode") != 0 && index($abs_parent->longname(1), $packageName) == 0)
				{
					$oneLineStr = $index . "," . "AP" . "," .  $abs_parent->longname(1) . "\n";
					push @tmpList, $oneLineStr;
				}
			}
		}	
=cut

		$len = @tmpList;
		if ($len > 0)
		{
			$oneLineStr = $index . "," . "C" . "," .  $class->longname(1) . "\n";
			push @tmpList, $oneLineStr;
			printFile(@tmpList);
			$index = $index + 1;
		}

	}


}
