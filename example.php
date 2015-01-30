<?php
// Example php file
function whatever($variable)
{
	$test = strtolower($variable);
	if ($test=='anything')
	{
		$test = 'nothing';
	}
	return $test;
}

?>