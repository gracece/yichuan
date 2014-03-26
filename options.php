<?php
$filename = "line.txt";
if(isset($_GET['clear']))
{
$fh = fopen($filename,'w');
}
