#gmail account if need checkmail
email=''
password=''

ip_docker='34.87.182.148'
ip_release='35.187.235.57'

#env=(release or staging) if using venta on docker input env=docker and IP=your_IP_of_venta_on_docker
env='release'

#url
url_group_docker=f'http://{ip_docker}:21264'
url_group_release='https://group-release.gigacover.com'

#sentinel
sentinel_docker=f'http://{ip_docker}:21262'
sentinel_release='https://auth-release.gigacover.com'

#selenium running mode, fill 'yes' if u wanna run on headless , ortherwise fill 'no'(if run on CHROME_DRI_ENV=docker skip this)
headless=''

#chrome driver
dri="docker"

#ssh on host: aqa will be run on host which is found (available and valuable) and order by docker -> release -> staging
# docker="jarvis@34.87.120.231"
release="trieu@35.187.235.57"

#.env
environment="release"
