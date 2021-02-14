# This code can be used to check Spark configuration
# pass the input source file and calculated word count should appear in part file in output
from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    # create Spark context with Spark configuration
    conf = SparkConf().setAppName("Word Count - Python").set("spark.hadoop.yarn.resourcemanager.address","192.168.0.104:8032")
    sc = SparkContext(conf=conf)



    # read in text file and split each document into words
    words = sc.textFile("/Users/patthar/Documents/IOT_PROJECTS/spring_iot_project/data/input/sample_data.txt").flatMap(lambda line: line.split(" "))
    # count the occurrence of each word
    wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

    wordCounts.saveAsTextFile("/Users/patthar/Documents/IOT_PROJECTS/spring_iot_project/data/output")