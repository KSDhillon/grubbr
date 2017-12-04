from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "Recommendations")

data = sc.textFile("/tmp/data/log.txt", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: tuple(line.split(",")))   # tell each worker to split each line of it's partition
pairs = pairs.distinct()
visited_sites = pairs.groupByKey()
paired_items = visited_sites.mapValues(lambda sites: list((list(sites)[x], list(sites)[x+1]) for x in range(len(sites) - 1)))
list_of_item_pairs = paired_items.flatMap(lambda line: line[1])
count_pairs = list_of_item_pairs.map(lambda pair: (pair, 1))
o = count_pairs.collect()
print(o)

sc.stop()
