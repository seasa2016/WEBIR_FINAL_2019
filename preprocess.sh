java -Xmx4g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner -fileList ./input/input_file -outputFormat text -outputDirectory ./input &> ./ner_log

python parsing_ner.py ./input