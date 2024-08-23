# usage
# run on release to have backup file: docker exec phoenix_db_c pg_dump -Ujarvis -d phoenix | gzip -c > /tmp/hoa/phoenix_20230202_1156.gz
#./script/tool_script/rsync_backup_file_from_relase.sh /tmp/hoa/ phoenix_20230121_0836.gz hoa

# download file from relase to local
filepath=$1
file=$2
user=$3
pass=$4
rsync -e ssh $user@15.235.185.146:/$filepath/$file ~/Downloads/$file

# remove .gz in file
f="${file/.gz/}"
echo "$f from $file"

# unzip first
gzip -d ~/Downloads/$file

# restore to db
cat ~/Downloads/$f | docker exec -i solarsys_zeus_db psql -Uroot -dzeus
