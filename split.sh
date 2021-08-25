rm -rf segments
mkdir -p segments
#split -b 50m files.db splits/files.db.seg_
#split -b 50m data.db splits/data.db.seg_
#rm segments/list
for f in compression/*.gz; do
    n=`basename ${f}`
    split -b 50m ${f} segments/${n}.segment_
    ls segments | grep -P "${n}.segment_*" > segments/${n}.list
    echo ${n} >> segments/list
done;

cd segments/
md5sum *.segment_* > md5sum
sha1sum *.segment_* > sha1sum

cd ..
rm -rf compression
