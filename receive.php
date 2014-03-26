<?php
$filename = "line.txt";
if(isset($_POST['line']))
{
$data = explode(',',$_POST['line']);
$record = sprintf('{"x1":%s,"y1":%s,"x2":%s,"y2":%s}',$data[0],$data[1],$data[2],$data[3]);

$word = time()."#".$record."\n";
$fh = fopen($filename,'a');
if(fwrite($fh,$word))
    echo "success";
fclose($fh);
}
else if(isset($_GET['clear']))
{
$fh = fopen($filename,'w');
}
