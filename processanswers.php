<?php


function getanswer($pic) {
    $pic -> negateImage(True);
   
    $it = $pic->getPixelIterator();
    $marks = array();
    $amark =0;
    $bmark=0;
    $cmark=0;
    $dmark=0;
    $emark=0;
    /* Loop trough pixel rows */
    foreach( $it as $row => $pixels )
    {
        /* Loop trough the pixels in the row (columns) */
        foreach ( $pixels as $column => $pixel )
            {
                $color = $pixel->getColor();   
                $intesity = $color['r'];
                
                if ($column > 19 && $column < 38){
                    $amark = $amark + $intesity;
                }
                
                elseif ($column >= 38 && $column  < 56){
                    $bmark = $bmark + $intesity;
                }    
                    
                elseif ($column >= 56 && $column  < 73){
                    $cmark = $cmark + $intesity;
                }    
                    

                elseif ($column >= 73 && $column  < 95){
                    $dmark = $dmark + $intesity;
                } 
                
                elseif ($column >= 95 && $column < 109){
                    $emark = $emark + $intesity;
                }                 
                
                
                };
              }


    $dev = stats_absolute_deviation(array($amark,$bmark,$cmark,$dmark,$emark));

	if ($dev < 1400){return "";}
    else{
    $maximum = max(array($amark,$bmark,$cmark,$dmark,$emark));
	
	
    if ($maximum == $amark){return "A";}
    if ($maximum == $bmark){return "B";}
    if ($maximum == $cmark){return "C";}
    if ($maximum == $dmark){return "D";}
    if ($maximum == $emark){return "E";}
    }

}


function read_test($img){
    


    $w = $img->getImageWidth(); // get the width of uploaded image
    $h = $img->getImageHeight(); //get the height of uploaded image
	
    $img -> cropImage($w*.99, $h*.99, $w*.01, $h*.01); //trim off the immediate border slightly
	


    
	$img -> modulateImage(100,0,100);//make the image greyscale
    //$img -> modulateImage(105, 100, 100); //increase the brightness by 5%

    $img -> normalizeImage (Imagick::CHANNEL_ALL ); //normalize the contrast
	$img-> contrastImage(1);
	$img-> contrastImage(1);
	$img-> contrastImage(1);
	$img-> contrastImage(1);
    $img -> blackthresholdimage( "#1E1E1E" ); //turn shaded areas to completely black
    $img -> whitethresholdimage( "#1E1E1E" ); // turn everything else white


	$img -> deskewImage(.80); // align image to correct for angled image


    $img->trimImage(40000); //trim the white area away leaving just the border
	$img -> deskewImage(.90); // align image to correct for angled image
	$img->trimImage(40000); //trim the white area away leaving just the border
   
	$w = $img->getImageWidth(); // get the width of uploaded image
    $h = $img->getImageHeight(); //get the height of uploaded image

	
	if ($w > $h){ // if the image uploaded  was taken horizontally
		$img->rotateImage(new ImagickPixel('#00000000'), 90); //rotate the image clockwise by 90 degrees	
		}
		


    $img-> thumbnailImage(472, 695); // make the image a uniform size
	//header("Content-Type: image/jpg");
    //echo $img ->getImageBlob();
	

    $w = $img->getImageWidth(); //get the width of the image
    $h = $img->getImageHeight(); //get the height of the image

    $img -> setImagePage(0, 0, 0, 0); //reset the cropping starting position
    $img -> cropImage($w ,  $h*.59,  0, $h * .35); // crop the image to get just the responses

    
    $img -> setImagePage(0, 0, 0, 0); //reset the cropping starting position

	$w = $img->getImageWidth(); //get the width of the image
    $h = $img->getImageHeight(); //get the height of the image



    $answers = array(); // make an empty array to hold the answers
    $x = 1;
    for ($j = 0; $j < 4; $j++) {
        for ($i = 0; $i < 12; $i++) {
       
            $response = clone $img;
			
            $response -> setImagePage(0, 0, 0, 0);
            $response-> cropImage(117, 34 ,  $j * 117,  $i*34 );
			//header("Content-Type: image/jpg");
			//echo $response ->getImageBlob();
            //$response -> writeImage ("test_".$x.".jpg");
			$response-> writeImage("test_".$x.".jpg"); //also works
            $answer = getanswer($response);
            array_push($answers,$answer);
            $x = $x + 1;
        
        }
    }
    return $answers;
}

?>
