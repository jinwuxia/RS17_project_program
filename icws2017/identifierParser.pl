use Understand;
$udbFileName = $ARGV[0]; #../RS17_source_data/RS17_jpestore6/static/source/jpetstore6.udb
$packageName = $ARGV[1];
$outfileName = $ARGV[2];

($db, $status) = Understand::open($udbFileName);
die "Error status: ", $status, "\n" if $status;

open(OUTFILE, ">" . $outfileName);
sub printFile
{
  my @tmpList = @_;
  foreach $str (@tmpList)
  {
    print OUTFILE $str;
  }
}

@classList = $db->ents("Class");
@interfaceList = $db->ents("Interface");
push @classList, @interfaceList;

#{classname}=[itmes1, item2,..]
my @allArray;
foreach $class (@classList)
{
    if (index($class->longname(1), $packageName) ==0)
    {
      undef @itemArray;
     	$classLongName = $class->longname(1);
     	print "classname=", $classLongName, "\n";
     	push(@itemArray, $classLongName); #append list
      push(@itemArray, $classLongName);
     	#variable member name
     	@varList = $class->ents("Define", "Variable Member");
     	foreach $var (@varList)
     	{
        $varName = $var->longname(1);
        print "varName=", $varName, "\n";
        push(@itemArray, $varName); #append list
      }

      #method membern name
      @methodList = $class->ents("Define", "Method Member");
      foreach $method  (@methodList)
      {
        $methodName = $method->longname(1);
        push(@itemArray, $methodName);  #append list
        print "methodName=", $methodName, "\n";

        @parameterList = $method->ents("Define", "Parameter");
        #$parameterList = $method->parameters();
        for $param  (@parameterList)
        {
          push(@itemArray, $param->type());
          push(@itemArray, $param->name);
          print "param type: ", $param->type(), "  param name: ", $param->name, "\n";
        }

      }

    $oneLine = join(',' , @itemArray)  .  "\n";
    push(@allArray, $oneLine);
    } #end if

}# end foreach

printFile(@allArray);
