use Understand;

#uperl  pro.pl  xxx.udb    com.ibatis

$udbFileName = $ARGV[0]; #../RS17_source_data/RS17_jpestore6/static/source/jpetstore6.udb
$packageName = $ARGV[1]; 


@array = split(/\//, $udbFileName);
$len = @array;
$udb = $array[$len - 1];
@tmp = split(/\.udb/, $udb);
$project = $tmp[0];
pop @array;
$dir = join("/", @array);
$outfileName = $dir . "/" . $project . "_interface_parent_class.csv";
print $outfileName . "\n";


($db, $status) = Understand::open($udbFileName);
die "Error status: ", $status, "\n" if $status;

@classList = $db->ents("Class");
@interfaceList = $db->ents("Interface");

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
if (@interfaceList)
{
	#print "ccccccccccccc\n";
	foreach $interface (@interfaceList)
	{
		my @tmpList;
	
		if ($interface->metric("CountLineCode") != 0  && index($interface->longname(1), $packageName) == 0)
		{	
			my @children = $interface->ents("Implementby", "Class");
			if (@children)
			{
				foreach $child (@children)
				{
					if ($child->metric("CountLineCode") != 0 && index($child->longname(1), $packageName) == 0)
					{
						$oneLineStr = $index . "," . "C" . "," .  $child->longname(1) . "\n";
						push @tmpList, $oneLineStr;
					}
				}

				$len = @tmpList;
				if ($len > 0)
				{
					$oneLineStr = $index . "," . "I" . "," .  $interface->longname(1) . "\n";
					my @oneList;
					push @oneList, $oneLineStr;
					@tmpList = (@oneList, @tmpList);
					printFile(@tmpList);
					$index = $index + 1;
				}


			}
		}
	}
}


foreach $class (@classList)
{
	my @tmpList;

	if ($class->metric("CountLineCode") != 0  && index($class->longname(1), $packageName) == 0)
	{
		my @children = $class->ents("Extendby", "Class");
		if (@children)
		{
			foreach $child (@children)
			{
				if ($child->metric("CountLineCode") != 0 && index($child->longname(1), $packageName) == 0)
				{
					$oneLineStr = $index . "," . "C" . "," .  $child->longname(1) . "\n";
					push @tmpList, $oneLineStr;
					#print $oneLineStr;
				}
			}
		}

		$len = @tmpList;
		if ($len > 0)
		{
			$oneLineStr = $index . "," . "P" . "," .  $class->longname(1) . "\n";
			my @oneList;
			push @oneList, $oneLineStr;
			@tmpList = (@oneList, @tmpList);
			printFile(@tmpList);
			$index = $index + 1;
		}
	}

}
