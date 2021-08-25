#cat segments/segment_* > dist.zip
#rm splits/segment_*
#unzip dist.zip

mkdir temp
cd segments
while read p; do
    eval "cat `cat ${p}.list | tr '\n' ' '` > ../temp/${p}"
done < list

cd ..
for f in temp/*.gz; do
    echo `basename ${f} .gz`
    gzip -cd ${f} > `basename ${f} .gz`
done;

rm -rf temp