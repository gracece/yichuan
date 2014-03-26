<?php
if(isset($_GET['t']))
    $t = $_GET['t'];
else
    $t = 0;
$filename="line.txt";
$fh = fopen($filename,'r');
while(!feof($fh))
{
 $buf = fgetcsv($fh,900,"#");
 if($buf['0']>= $t)
 {
     $line[] = array(
     'timestamp' => $buf[0],
     'line' => json_decode($buf[1]),
     );
 }
}
echo json_encode($line);
