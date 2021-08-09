import os
import jieba
# 去除停用词
def filterStopWords(sentence_seg,stopwordsDict_path):
    with open(stopwordsDict_path,"r",encoding="utf-8") as stopwordsFile:
        stopwords=[line.strip() for line in stopwordsFile.readlines()]
    sentence_seg_list=list(sentence_seg)
    sentence_seg_filter=[]
    for word in sentence_seg_list:
        if word not in stopwords:
            if word!='\t':
                sentence_seg_filter.append(word)
    # sentence_seg_filter=sentence_seg_filter.encode()
    sentence_seg_filter=[word for word in sentence_seg_filter if (word!='' and word!='\n')]
    return sentence_seg_filter
# 语句分词
def segment_filter(sentence,stopwordsDict_file):
    sentence_seg=jieba.cut(sentence)
    sentence_seg_filter=filterStopWords(sentence_seg,stopwordsDict_file)
    return sentence_seg_filter
# 文本文件分词
def segment_file(corpus_file,stopwordsDict_file=''):
    segmentResult_str=[]
    with open(corpus_file,'r',encoding='utf-8') as file_input:
        if stopwordsDict_file=='':
            for line in file_input:
                line_seg=jieba.cut(line)
                segmentResult_str.extend(list(line_seg)) 
        else:
            for line in file_input:
                line_seg=segment_filter(line,stopwordsDict_file)
                segmentResult_str.extend(line_seg)
    return " ".join(segmentResult_str)
# 语料文本预处理
def preCorpusFile(corpus_file,stopwordsDict_file,result_file='',label=''):
    preResult=segment_file(corpus_file,stopwordsDict_file)
    if result_file!='':
        with open(result_file,'a+',encoding='utf-8') as file_output:
            if label!='':
                file_seg=label+":"+preResult+"\n"
                file_output.write(file_seg)
            else:
                file_output.write(preResult+"\n")
    return preResult
# 关键词提取
def extractKeywords(segment_filter_dict,keywordsfile,topk=10,labellen=0):
    with open(segment_filter_dict,"r",encoding="utf-8") as fr,open(keywordsfile,"w",encoding="utf-8") as fd:
        for line in fr.readlines():
            if line.split():
                keywords=jieba.analyse.extract_tags(line,topK=topk)
                if labellen!=0:
                    fd.write(line[:labellen+1])
                for item in keywords:
                    fd.write(item)
                    fd.write(' ')
                fd.write("\n")
# 语料库加载及预处理
def loadPreCorpuslib(corpuslib_path,stopwordsDict_file,classifyTag='',preResultfile=''):
    if os.path.isdir(corpuslib_path)==False:
        return preCorpusFile(corpuslib_path,stopwordsDict_file,preResultfile,classifyTag)
    allfiles=os.listdir(corpuslib_path)
    textset=[]
    allclassifyTags=[]
    for thefile in allfiles:
        corpus_file=corpuslib_path+"/"+thefile
        preResult=preCorpusFile(corpus_file,stopwordsDict_file,preResultfile,classifyTag)
        textset.append(preResult)
        if classifyTag!='':
            allclassifyTags.append(classifyTag)
    return textset,allclassifyTags
# 加载分词数据集
def loadSegmentXDataset(segment_file):
    textset=[]
    allclassifyTags=[]
    with open(segment_file,"r",encoding="utf-8") as file_input:        
        for line in file_input.readlines():
            lineContent=line.split(":")
            if lineContent>1:
                allclassifyTags.append(lineContent[0])
                textset.append(lineContent[1])
            else:
                textset.append(line)
    return textset,allclassifyTags
if __name__ == '__main__':
    loadPreCorpuslib("predata/comment.txt","predata/stopdict.txt","","predata/dataset.txt")