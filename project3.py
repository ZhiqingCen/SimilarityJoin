import sys
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

'''
optimization techniques used
- broadcast dataframe before join
    - it reduce the need of shuffling data while performing join
    - it reduce the need of transfering data repeatedly across the network
- join dataframe with condition before calculating similarity such that 
    - df1.invoiceNo is less than df2.invoiceNo to prevent duplicates pairs
    - df1.invoiceDate is different from df2.invoiceDate to filter out transaction pairs of the same year
    - these prevent extra calculation
- use standard join
    - prevent the large number of cartesian product produced by crossjoin to reduce computational cost
'''

class project3:
    def __init__(self):
        self.invoiceNo = "invoiceNo"        # the unique ID to record one purchase transaction
        self.description = "description"    # the name of the item in a transaction
        self.quantity = "quantity"          # the amount of the items purchased
        self.invoiceDate = "invoiceDate"    # the time of the transaction
        self.unitPrice = "unitPrice"        # the price of a single item
    
    @staticmethod
    # @udf(returnType=FloatType())
    @udf()
    def jaccardSimilarity(itemSet1, itemSet2):
        itemSet1 = set(itemSet1)
        itemSet2 = set(itemSet2)
        numerator = len(itemSet1.intersection(itemSet2))
        denominator = len(itemSet1.union(itemSet2))
        return float(numerator / denominator)

    def run(self, inputpath, outputpath, k):
        # conf = SparkConf()
        # sc = SparkContext(conf = conf)
        spark = SparkSession.builder.getOrCreate()
        spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
        
        # define schema of dataframe
        schema = StructType([\
                    StructField(self.invoiceNo, IntegerType(), True),\
                    StructField(self.description, StringType(), True),\
                    StructField(self.quantity, IntegerType(), True),\
                    StructField(self.invoiceDate, StringType(), True),\
                    StructField(self.unitPrice, FloatType(), True)])
        
        # read dataframe from inputpath
        df = spark.read.format("csv").option("header", "false").schema(schema).load(inputpath)
        df = df.select(self.invoiceNo, self.description, self.invoiceDate)
        
        # format invoiceDate
        dataDF = df.withColumn(self.invoiceDate, year(to_date(self.invoiceDate, "dd/M/yyyy hh:mm a")))
        
        # get itemSets for each invoiceNo
        itemSetDF = dataDF.groupBy(self.invoiceNo, self.invoiceDate) \
                          .agg(collect_set(self.description).alias("itemSets"))
        
        # broadcast dataframe
        broadcastDF = broadcast(itemSetDF)
        
        # map pairs based on different years
        pairDF = broadcastDF.alias("df1").join(broadcastDF.alias("df2"), \
                                               (col(f"df1.{self.invoiceNo}") < col(f"df2.{self.invoiceNo}")) & \
                                               (col(f"df1.{self.invoiceDate}") != col(f"df2.{self.invoiceDate}")), \
                                                "inner")
        
        # calculate similarity
        similarityDF = pairDF.withColumn("similarity", self.jaccardSimilarity(col("df1.itemSets"), col("df2.itemSets")))
        
        # filter output with given tau value
        filterDF = similarityDF.filter(col("similarity") >= k)
        
        # modify output format
        outputDF = filterDF.withColumn("output", concat_ws(":", concat(lit("("), concat_ws(",", col(f"df1.{self.invoiceNo}"), col(f"df2.{self.invoiceNo}")), lit(")")), col("similarity"))) \
                           .select("output")

        # output to outputpath
        outputDF.write.text(outputpath)
        spark.stop()

        
if __name__ == '__main__':
    project3().run(sys.argv[1], sys.argv[2], sys.argv[3])
    

