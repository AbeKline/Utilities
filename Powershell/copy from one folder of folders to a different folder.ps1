set-location "Z:\Books\bookz\RAR"
Get-ChildItem -Recurse | Move-item -destination "Z:\Books\aaaa" -Verbose -Force
