for i in 0 5 4
do
	echo $i
	java -Xmx4g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner -fileList ./file_dir/l_${i}  -outputFormat text -outputDirectory ./NER &> ./check/q_${i} &

done

wait

