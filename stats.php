<?php



function standard_deviation($x){//find the mean absolute deviation of a set of numbers
    
    $average = array_sum($x) / count($x); //find the average of the set of numbers
    $differences = array(); //make an empty array to hold the differences between each number and the mean
    foreach ($x as $item){//go through item in the array
      array_push($differences, ($item - $average)*($item - $average)); //find the absolute difference between that number and the mean and add it to the differences array
    }
    $std_dev = array_sum($differences) / count($differences); //take the average of those differences
    return sqrt($std_dev);//return the square root of the average squared deviation
}


function zscore($x){
	$mean = array_sum($x) / count($x);
	$std_dev = standard_deviation($x);
	$scores = array();
	foreach ($x as $item){
		array_push($scores, ($item - $mean)/$std_dev);
	}
	return $scores;
		
}


function stats_absolute_deviation($x){//find the mean absolute deviation of a set of numbers
    
    $average = array_sum($x) / count($x); //find the average of the set of numbers
    $differences = array(); //make an empty array to hold the differences between each number and the mean
    foreach ($x as $item){//go through item in the array
      array_push($differences, abs($item - $average)); //find the absolute difference between that number and the mean and add it to the differences array
    }
    $mean_dev = array_sum($differences) / count($differences); //take the average of those differences
    return $mean_dev;//return the average absolute deviation
}

function correlation2($x, $y){
	$XZ = zscore($x);
	$YZ = zscore($y);
	$crossproduct = array_map(function($a,$b){return $a * $b;},$XZ,$YZ);
	return array_sum($crossproduct) / count($crossproduct);	
}

function correlation($x, $y){
	
	$length= count($x);
	$mean1=array_sum($x) / $length;
	$mean2=array_sum($y) / $length;

	$a=0;
	$b=0;
	$axb=0;
	$a2=0;
	$b2=0;

	for($i=0;$i<$length;$i++){
		$a=$x[$i]-$mean1;
		$b=$y[$i]-$mean2;
		$axb=$axb+($a*$b);
		$a2=$a2+ pow($a,2);
		$b2=$b2+ pow($b,2);
	}

	$denominator = sqrt($a2*$b2);
	if ($denominator == 0){return 0;}
	else {return  $axb / $denominator;}
}


//column sum
function column_sum($data){
	$transposed = array_map(null, ... $data );
	$colsum = array();
	foreach($transposed as $item){
		array_push($colsum, array_sum($item));
	}
	return $colsum;
}

//row sum
function row_sum($data){
	$rowsum = array();
	foreach($data as $item){
		array_push($rowsum, array_sum($item));
	}
	return $rowsum;
}
	

function itemdifficulty($rightwrong){
	//get the total number of respondents
	$numberrespondents =count($rightwrong);
	
	//sum up the items across participants
	$itemtotals = column_sum($rightwrong);
	
	//for each question total, divide it by the total number of respondents
	$difficulty = array();
		foreach ($itemtotals as $total){
			array_push($difficulty, $total / $numberrespondents);
	}
	
	return $difficulty;
}


function pointbiserial($rightwrong){
	//get people's scores
	$scores = row_sum($rightwrong);
	
	//transpose the rows and columns
	$transposed = array_map(null, ... $rightwrong );
	
	//for each item
	$point_biserial_correlations = array();
	foreach ($transposed as $item){
		$cor = correlation($item,$scores);
		array_push($point_biserial_correlations,$cor);
	}
	
	return $point_biserial_correlations;
}

function pairwise_combinations($n){
	$range1 = range (0 , $n-1,  1 );
	$range2 = range (0 , $n-1,  1 );
	$pairs = array();
	foreach($range1 as $item1){
			foreach($range2 as $item2){
				if ($item1 != $item2){
					array_push($pairs , array($item1,$item2));
				}
				
			}
		array_shift($range2);
	}
return $pairs;
}

 

function interitem_correlation($rightwrong){
	//find the correlation between each item and each other item
	//transpose the rows and columns
	$transposed = array_map(null, ... $rightwrong );
	
	$numberitems = count($transposed);
	
	$pairs = pairwise_combinations($numberitems);
	$correlations = array();
	foreach($pairs as $pair){
		$item1 = $transposed[$pair[0]];
		$item2 = $transposed[$pair[1]];
		$corr = correlation($item1,$item2);
		array_push($correlations,$corr);
		}
	$averagecorrelation = array_sum($correlations) / count($correlations) ;
	return $averagecorrelation;
}

function reliability($averagecorrelation,$numberitems){
	$alpha =  ($numberitems * $averagecorrelation)/(1 + ($numberitems - 1)*$averagecorrelation);
	return $alpha;
}


//$a = array(1,0,1,1);
//$b = array(1,0,1,1);
//$c = array(0,1,1,0);
//$d = array(1,1,1,0);
//$e = array(1,0,0,1);

//$rightwrong = array($a,$b,$c,$d,$e);

//$iic = interitem_correlation($rightwrong);