<?php
$pdf_file = 'demo.pdf';
$save_to  = 'demo.png';

$img = new Imagick();
$img->setResolution(100,100);
$img->readImage("{$pdf_file}[2]");

$img->setImageFormat('png');
$img->flattenImages();
$img->writeImage($save_to);

