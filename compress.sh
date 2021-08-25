#rm data.zip tags.zip files.zip
#zip data.zip data.json
#zip tags.zip tags.json
#zip files.zip files.json

#rm dist.zip #*.db
#zip dist.zip *.json
#rm *.json

#rm dist.tar.gz
#tar -czf dist.tar.gz --files-from=/dev/null #Empty tar gz
#tar -zcvfm dist.tar.gz *.json
rm -rf compression
mkdir compression
gzip -cnf data.json > compression/data.json.gz # k option
gzip -cnf tags.json > compression/tags.json.gz
gzip -cnf files.json > compression/files.json.gz
rm data.json tags.json files.json
