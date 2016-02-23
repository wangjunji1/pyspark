from pyspark import SparkConf, SparkContext

conf = SparkConf()

conf.setAppName("spark_app_wordcount_merge")

sc = SparkContext(conf=conf)

hadoopConf = {"mapreduce.input.fileinputformat.inputdir": "/user/hdfs/rawlog/app_weibomobilekafka1234_topweiboimpression",
              "mapreduce.input.fileinputformat.input.dir.recursive": "true",
              "mapreduce.input.fileinputformat.split.minsize.per.node": "67108864",
              "mapreduce.input.fileinputformat.split.minsize.per.rack": "134217728"}

source = sc.newAPIHadoopRDD(inputFormatClass="org.apache.hadoop.mapreduce.lib.input.CombineTextInputFormat",
                            keyClass="org.apache.hadoop.io.LongWritable",
                            valueClass="org.apache.hadoop.io.Text",
                            conf=hadoopConf)

source = source.coalesce(500)

lines = source.map(lambda pair: pair[1])

words = lines.flatMap(lambda line: line.split(","))

pairs = words.map(lambda word: (word, 1))

counts = pairs.reduceByKey(lambda a, b: a + b, 30)

counts.saveAsTextFile("/user/yurun/spark/output/wordcount/")

sc.stop()
