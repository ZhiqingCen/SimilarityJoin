import sys
from pyspark import SparkConf, SparkContext

class project3:
    def run(self, inputpath, outputpath, k):
        conf = SparkConf()
        sc = SparkContext(conf = conf)

        
if __name__ == '__main__':
    project3().run(sys.argv[1], sys.argv[2], sys.argv[3])
    

