use Understand;

$udbFileName = $ARGV[0];
$packagepre = $ARGV[1];

@array = split(/\.udb/, $udbFileName);
$projectName = $array[0];
$outputFileName = $projectName . "_code_method_call.txt"; 
print "input filename = " . $udbFileName . ",  output filename = " . $outputFileName . "\n\n";


( $db, $status ) = Understand::open($udbFileName);
die "Error status: ", $status, "\n" if $status;


open(EDGEFILE, ">" . $outputFileName);

my %hashmap;

$number_of_nodes = 0;
$number_of_edges = 0;
$inner_method_count = 0;

#this function get the parameter list just including type, not the variable name.
sub reduce_parameter_list
{
	# my $method_parameters=shift(@_);
	my @method_parameters_list = @_;  # @_ is the parameter list = [arg0, arg1, ...]
	my $method_parameters = join(',',@method_parameters_list);
	# print $method_parameters,"**";
	@parameter_list = split(/\,/,$method_parameters);
	@parameter_type_list=();
	foreach $parameter (@parameter_list)
	{
		@parameter_one=split(/\ /,$parameter);
		@parameter_one_strip=split(/\[/,@parameter_one[0]);
		@parameter_type_list=(@parameter_type_list,@parameter_one_strip[0]);
	}
	$reduced_parameter = join(',',@parameter_type_list);
	# print $reduced_parameter,"\n";
	return $reduced_parameter;
}


#get parameter number
sub get_parameter_num
{
	my @method_parameters_list = @_;
	my $len = @method_parameters_list;
	my $method_parameters = join(',', @method_parameters_list);
	#print $method_parameters;
	#print "      len=" .  $len, "\n";
	return $len;
}

foreach $method ($db->ents("Method"))
{
	$method_name=$method->name();

	if(index($method_name, "(Anon") != -1)
	{
		$inner_method_count=$inner_method_count + 1;
		next;
	}

	$loc=$method->metric("CountLineCode");
	if($loc == 0)
	{
		next;
	}

}
print "Number of Inner Methods=",$inner_method_count,"\n";


foreach $method ($db->ents("Method"))
{
	$loc = $method->metric("CountLineCode");
	$callee_name = $method->longname(1);
	if($loc != 0 && index($callee_name, $packagepre) == 0 )
	{

		#the method inside this sourcecode, the LOC is not 0
		foreach $caller ($method->ents("Callby","Method"))
		{
			$caller_loc = $caller->metric("CountLineCode");
			if($caller_loc != 0 && index($caller->longname(1), $packagepre) == 0 )
			{
				$callee_name = $method->longname(1);
				$caller_name = $caller->longname(1);

				my $caller_parameters = $caller->ents("Define","Parameter");
				if($caller_parameters)
				{
					$caller_full_name = $caller->type() . ' ' . $caller_name . "(" . reduce_parameter_list($caller->parameters()) . ")";
					#$caller_full_name_paralen = get_parameter_num($caller->parameters());
				}
				else
				{
					$caller_full_name = $caller->type() . ' ' . $caller_name . "()";
					#$caller_full_name_paralen = 0;
				}

				my $callee_parameters = $method->ents("Define","Parameter");
				if($callee_parameters)
				{
					$callee_full_name = $method->type() . ' ' . $callee_name . "(" . reduce_parameter_list($method->parameters()) . ")";
					#$callee_full_name_paralen = get_parameter_num($method->parameters());
				}
				else
				{
					$callee_full_name = $method->type() . ' ' . $callee_name . "()";
					#$callee_full_name_paralen = 0;
				}

				if ( !exists $hashmap{$caller_full_name} ) 
				{
					$hashmap{$caller_full_name} = 1;				
					#print NODEFILE $caller_full_name .  ";" . $caller_full_name_paralen .  "\n";
					$number_of_nodes = $number_of_nodes + 1;
				}
				if ( !exists $hashmap{$callee_full_name} ) 
				{
					$hashmap{$callee_full_name} = 1;
					#print NODEFILE $callee_full_name . ";". $callee_full_name_paralen .  "\n";
					$number_of_nodes = $number_of_nodes + 1;
				}
				print EDGEFILE $caller_full_name .  ";"  .  $callee_full_name . "\n"; 

				$number_of_edges = $number_of_edges + 1;
			}
		}

		foreach $caller ($method->ents("Callby Nondynamic","Method"))
		{
			$caller_loc = $caller->metric("CountLineCode");
			if($caller_loc != 0 && index($caller->longname(1) , $packagepre) == 0)
			{
				$callee_name = $method->longname(1);
				$caller_name = $caller->longname(1);

				my $caller_parameters = $caller->ents("Define","Parameter");
				if($caller_parameters)
				{
					$caller_full_name = $caller->type() . ' ' .  $caller_name . "(" . reduce_parameter_list($caller->parameters()) . ")";
					#$caller_full_name_paralen = get_parameter_num($caller->parameters());
				}
				else
				{
					$caller_full_name = $caller->type() . ' ' . $caller_name . "()";
					#$caller_full_name_paralen = 0
				}

				my $callee_parameters = $method->ents("Define","Parameter");
				if($callee_parameters)
				{
					$callee_full_name = $method->type() . ' ' . $callee_name . "(" . reduce_parameter_list($method->parameters()) . ")";
					#$callee_full_name_paralen = get_parameter_num($method->parameters());
				}
				else
				{
					$callee_full_name = $method->type() . ' ' . $callee_name . "()";
					#$callee_full_name_paralen = 0
				}

				if ( !exists $hashmap{$caller_full_name} ) 
				{
					$hashmap{$caller_full_name} = 1;
					#print NODEFILE $caller_full_name . ";" .  $caller_full_name_paralen . "\n";
					$number_of_nodes = $number_of_nodes + 1;
				}
				if ( !exists $hashmap{$callee_full_name} ) 
				{
					$hashmap{$callee_full_name} = 1;
					#print NODEFILE $callee_full_name . ";" .  $callee_full_name_paralen . "\n";
					$number_of_nodes = $number_of_nodes + 1;
				}

				print EDGEFILE $caller_full_name . ";" . $callee_full_name . "\n"; 
				$number_of_edges = $number_of_edges + 1;
			}
		} 
	}
}

print "Number of Nodes = ",$number_of_nodes,"   Number of Edges = ", $number_of_edges,"\n";
