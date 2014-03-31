<?php
$pdf_file = './static/upload/demo.pdf';
$save_to  = 'demo.png';

$img = new Imagick($pdf_file);
$img->setResolution(100,100);
$pageNumber = $img->getNumberImages();
for ($i=0; $i < $pageNumber; $i++)
{
    $img->readImage("{$pdf_file}[".$i."]");
    $img->setImageFormat('png');
    $img->flattenImages();
    $img->writeImage($i.$save_to);
}


