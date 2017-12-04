from pyspark import SparkContext
import MySQLdb

sc = SparkContext("spark://spark-master:7077", "Recommendations")

data = sc.textFile("/tmp/data/log.txt", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: tuple(line.split(",")))   # tell each worker to split each line of it's partition
pairs = pairs.distinct()
pairs = pairs.mapValues(lambda id: int(id))
visited_sites = pairs.groupByKey()
paired_items = visited_sites.mapValues(lambda sites: [(x,y) for x in sites for y in sites if x != y])
paired_items = paired_items.mapValues(lambda sites: [(x,y) for x,y in sites if x <= y])
list_of_item_pairs = paired_items.flatMap(lambda line: [(line[1][i], line[0]) for i in range(len(line[1]))])
grouped_items = list_of_item_pairs.groupByKey()
grouped_items = grouped_items.mapValues(lambda users: len(users))
filtered_items = grouped_items.filter(lambda item: item[1] >= 3)
recommended = filtered_items.collect()
print(recommended)
sc.stop()

table = {}
for rec in recommended:
    pair = rec[0]
    if pair[0] in table:
        table[pair[0]].append(str(pair[1]))
    else:
        table[pair[0]] = [str(pair[1])]
    if pair[1] in table:
        table[pair[1]].append(str(pair[0]))
    else:
        table[pair[1]] = [str(pair[0])]

print(table)

db = MySQLdb.connect("db", "www", "$3cureUS", "cs4501")
cursor = db.cursor()
try:
    cursor.execute("USE cs4501;")
    cursor.execute("TRUNCATE models_recommendations;")
    for key, value in table.items():
        command = "INSERT INTO models_recommendations (item_id, recommended_items) VALUES ({},\'{}\');".format(key, ",".join(value))
        cursor.execute(command)
    db.commit()
    cursor.execute("SELECT * from models_recommendations")
    print(cursor.fetchall())
except:
    print("error occured")
    db.rollback()



db.close()
