#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s"  # get SCRIPT_HOME=executed script's path, containing folder, cd & pwd to get container path
a="$SCRIPT_HOME/../.."; ROOT=$(cd "$a" && pwd);
green=$(tput setaf 2)
red=$(tput setaf 1)
normal=$(tput sgr0)
yellow=$(tput setaf 3)

cd $ROOT; pipenv sync
source $ROOT/.venv/bin/activate
CONFIG="$SCRIPT_HOME/config.py"
source $CONFIG
remote_host="release"
feature="sponsored_purchase"
user=$USER
host=$HOSTNAME
userhost="$user@$host"

if [[ $userhost == "trieu@release" || $userhost == "jarvis@release" ]]; then
    export PYTHONPATH=$PYTHONPATH:/opt/gigacover/assurance
fi

# generate test files for sponsored purchase feature
echo $(python "$SCRIPT_HOME/sponsored_purchase.py")

if [[ $userhost != "trieu@release" && $userhost != "jarvis@release" && $userhost != "jarvis@aqa-appium" ]]; then
    if [[ -z $docker ]]; then
        if [[ -z $release ]]; then
            echo "Cannot find out any host in config file. AQA Sponsored Purchase will exit in";
            countdown "00:00:03";
            exit
        else remote_host="$release"; echo "AQA Sponsored Purchase on ${green}release by $user${normal}"; fi
    else remote_host=$docker; echo "AQA Sponsored Purchase on ${green}docker by $user${normal}"; fi
    ssh_host=$(echo $remote_host | cut -d'@' -f 2);
    remote_folder="/opt/gigacover/aqa/$feature/$userhost";

    # upload script run-on-remote.sh to remote host :staging/:release
    ssh "$remote_host" "mkdir -p $remote_folder"  1>/dev/null 2>&1; cd - >/dev/null
    scp "$SCRIPT_HOME/run-on-remote.sh" "$remote_host:$remote_folder/run-on-remote.sh"  1>/dev/null 2>&1; cd - >/dev/null
    scp -r "$SCRIPT_HOME/testfiles" "$remote_host:$remote_folder"  1>/dev/null 2>&1; cd - >/dev/null

    # run the script
    ssh "$remote_host" "$remote_folder/run-on-remote.sh $remote_folder $user $host"
else
    ssh_host=$(echo $userhost | cut -d'@' -f 2);
    "$SCRIPT_HOME/run-on-remote.sh" $SCRIPT_HOME $user $host
fi


countdown()
{
  IFS=:
  set -- $*
  secs=$(( ${1#0} * 3600 + ${2#0} * 60 + ${3#0} ))
  while [ $secs -gt 0 ]
  do
    sleep 1 &
    printf "\r%02d:%02d:%02d" $((secs/3600)) $(( (secs/60)%60)) $((secs%60))
    secs=$(( $secs - 1 ))
    wait
  done
  echo
}