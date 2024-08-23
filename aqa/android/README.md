# Extract apk file from android device
View all app packages
`adb shell pm list packages`

Get actual file name and direction 
`adb shell pm path your-package-name`

Pull the file 
`adb pull /data/app/your-package-name-1/base.apk /path/to/store/file.apk`

