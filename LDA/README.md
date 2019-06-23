# Topic model: LDA 
## Step 1. Use to extract title and total content from dataset
- get <strong>title_all.csv</strong> directly from google drive, and skip this step.
https://drive.google.com/file/d/1tCnNfWKFz5tSyaPmY0LUQ-B5cXaiavG6/view?usp=sharing
- including text preprocess
- create <strong>title_all.csv</strong> which is used in next step
- python extract.py [input filename] [output filename]
```c
python extract.py TREC_Washington_Post_collection.v2.jl title_all.csv
```

## Step 2. Run LDA
- 25 categories
- Take <strong>title and total content</strong> into consideration
- python test_LDA.py [all document filename] [query document filename] [LDA model]
```c
python test_LDA.py title_all.csv filelist model/lda_model_25c_all
```
