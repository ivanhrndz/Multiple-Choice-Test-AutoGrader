<?php



function getidanswer($pic) {
    $pic -> negateImage(True); //reverse the colors
    $it = $pic->getPixelIterator(); // get the pixel color values

    $zeromark =0; //see how intense the mark for a zero is
    $onemark =0; //see how intense the mark for a one is
    $twomark=0; //see how intense the mark for a two is
    $threemark=0; //see how intense the mark for a three is
    $fourmark=0; //see how intense the mark for a four is
    $fivemark=0; //see how intense the mark for a five is
    $sixmark=0; //see how intense the mark for a six is
    $sevenmark=0; //see how intense the mark for a seven is
    $eightmark=0; //see how intense the mark for a eight is
    $ninemark=0; //see how intense the mark for a nine is
    /* Loop trough pixel rows */
    foreach( $it as $row => $pixels )
    {
        /* Loop trough the pixels in the row (columns) */
        foreach ( $pixels as $column => $pixel )
            {
                $color = $pixel->getColor();    // get the color value for that pixek
                $intesity = $color['r']; //get the red channel (they will all be the same if image is grayscale)
                
                if ($row > 20 && $row < 35){ //for the pixels between row 20 and 35
                    $zeromark = $zeromark + $intesity; //add the darkness values to the zero mark
                }
                
                elseif ($row >= 35 && $row  < 55){
                    $onemark = $onemark + $intesity; //add the darkness values to the one mark
                }    
                    
                elseif ($row >= 55 && $row  < 75){
                    $twomark = $twomark + $intesity; //add the darkness values to the two mark
                }    
                    

                elseif ($row >= 75 && $row  < 95){
                    $threemark = $threemark + $intesity; //add the darkness values to the three mark
                } 
                
                elseif ($row >= 95 && $row < 110){
                    $fourmark = $fourmark + $intesity; //add the darkness values to the four mark
                }                 

                elseif ($row >= 110 && $row < 130){
                    $fivemark = $fivemark + $intesity; //add the darkness values to the five mark
                }                 

                elseif ($row >= 130 && $row < 145){
                    $sixmark = $sixmark + $intesity; //add the darkness values to the six mark
                } 
                
                elseif ($row >= 145 && $row < 170){
                    $sevenmark = $sevenmark + $intesity;//add the darkness values to the seven mark
                } 

                elseif ($row >= 170 && $row < 185){
                    $eightmark = $eightmark + $intesity;//add the darkness values to the eight mark
                } 
                
 
                 elseif ($row >= 185 && $row < 200){
                    $ninemark = $ninemark + $intesity;//add the darkness values to the nine mark
                }   
                
                };
              }

    
    $dev = stats_absolute_deviation(array($zeromark,$onemark,$twomark,$threemark,$fourmark.$fivemark,$sixmark,$sevenmark,$eightmark,$ninemark)); // see what the mean absolute deviation is  for all the marks
    if ($dev < 800){return "";} //if the marks have little deviation (below 1000) then say there is no mark there
    else{ //otherwise, do the following
        $maximum = max(array($zeromark,$onemark,$twomark,$threemark,$fourmark,$fivemark,$sixmark,$sevenmark,$eightmark,$ninemark)); //find the darkest mark
        if ($maximum == $zeromark){return "0";} // if zeromark is the maximum, return a 0
        if ($maximum == $onemark){return "1";} // if zeromark is the maximum, return a 1
        if ($maximum == $twomark){return "2";} // if zeromark is the maximum, return a 2
        if ($maximum == $threemark){return "3";} // if zeromark is the maximum, return a 3
        if ($maximum == $fourmark){return "4";} // if zeromark is the maximum, return a 4
        if ($maximum == $fivemark){return "5";} // if zeromark is the maximum, return a 5
        if ($maximum == $sixmark){return "6";} // if zeromark is the maximum, return a 6
        if ($maximum == $sevenmark){return "7";} // if zeromark is the maximum, return a 7
        if ($maximum == $eightmark){return "8";} // if zeromark is the maximum, return a 8
        if ($maximum == $ninemark){return "9";} // if zeromark is the maximum, return a 9
    }
}


function read_id($img){

    $w = $img->getImageWidth();
    $h = $img->getImageHeight();
    $img -> cropImage($w*.99, $h*.99, $w*.01, $h*.01);

    $img -> modulateImage(100,0,100);
    $img -> modulateImage(105, 100, 100); 
    $img -> normalizeImage (Imagick::CHANNEL_ALL );
	$img-> contrastImage(1);
	$img-> contrastImage(1);
	$img-> contrastImage(1);
	$img-> contrastImage(1);
    $img -> blackthresholdimage( "#1E1E1E" ); //turn shaded areas to completely black
    $img -> whitethresholdimage( "#1E1E1E" ); // turn everything else white



 

    $img->trimImage(40000);


    $img -> deskewImage(.9);
	
	if ($w > $h){ // if the image uploaded  was taken horizontally
		$img->rotateImage(new ImagickPixel('#00000000'), 90); //rotate the image clockwise by 90 degrees	
		}
		

    $img-> thumbnailImage(472, 695);
    $w = $img->getImageWidth();
    $h = $img->getImageHeight();

    $img -> setImagePage(0, 0, 0, 0);
    $img -> cropImage($w * .36 ,  $h*.30,  $w * .57 , $h * .05);


	
    $w = $img->getImageWidth();
    $h = $img->getImageHeight();
    $img -> setImagePage(0, 0, 0, 0);

    $response = clone $img;
    $response -> setImagePage(0, 0, 0, 0);
	


    $answers = array(); // make an empty array to hold the answers
    $x = 1;
    for ($j = 0; $j < 10; $j++) {
         $response = clone $img;
         $response -> setImagePage(0, 0, 0, 0);
          $response-> cropImage($w*.098, $h,  $j * ($w*.098),  0 );

		  $answer = getidanswer($response);
         array_push($answers,$answer);
        $x = $x + 1;
    } 
    
    return  implode("", $answers);
}
?>