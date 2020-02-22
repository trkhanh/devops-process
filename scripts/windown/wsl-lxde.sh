# Set up
$app = "vcxsrv.exe"
$url ="https://sourceforge.net/projects/$($app)/files/latest/download"
$user = "khanhtran"
$output = "C:\Users\$($user)\Downloads\$($app)"


# $wc = New-Object System.Net.WebClient
# $wc.DowloadFile($ulr, $output)

(New-Object System.Net.WebClient).DownloadFile($url, $output);