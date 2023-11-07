# Similarity Join

COMP9313 - Big Data Management, Project 3
- Term 3 2023, 31 Oct 2023 - 22 Nov 2023

- [Similarity Join](#similarity-join)
  - [Similarity Join in E-commerce Transaction Logs (22 marks)](#similarity-join-in-e-commerce-transaction-logs-22-marks)
  - [Submission](#submission)
  - [Late submission penalty](#late-submission-penalty)
  - [Some notes](#some-notes)
  - [Optional (this will not be marked)](#optional-this-will-not-be-marked)
  - [Marking Criteria](#marking-criteria)


## Similarity Join in E-commerce Transaction Logs (22 marks)

**Background**: Similarity join is an important task in data mining. Given a set of records, it aims to find all the pairs of records with **similarity** larger than a threshold. A record is a set of items. For example, in Amazon, a record could represent the set of products that a customer purchases in a single transaction. The problem can find various applications in different domains, such as data cleaning and product recommendation. 

Given a collection $R$ of records, a similarity function $sim()$ and threshold $t$, the similarity join on $R$, is to find all the record pairs $r$ and $s$ from $R$, such that $sim(r, s) \ge t$. In this project, we use the Jaccard similarity function to compute similarity. That is, 

~~~math
sim(r, s) = \frac{r \cap s}{r \cup s}
~~~

Given the following example, and set $t=0.5$, 

| id | record |
| :- | :----- |
|0|1 4 5 6|
|1|2 3 6|
|2|4 5 6|
|3|1 4 6|
|4|2 5 6|
|5|3 5|

we can get the result pairs below:

| pair | similarity |
| :--- | :--------- |
|(0,2)|0.75|
|(0,3)|0.75|
|(1,4)|0.5|
|(2,3)|0.5|
|(2,4)|0.5|

**Problem definition**: In this project, we are still going to use the E-Commerce dataset of customer purchase transaction logs. Each record in the dataset has the following five fields (see the example dataset): 

~~~txt
InvoiceNo: the unique ID to record one purchase transaction
Description: the name of the item in a transaction (a name can contain multiple characters)
Quantity: the amount of the items purchased
InvoiceDate: the time of the transaction
UnitPrice: the price of a single item
~~~

**Each transaction** contains a **set** of **items** purahced. For example, in the sample dataset, we have `transactoin 1 = {A, B, C}`, `trasaction 2 = {A, C, DD}` and `transaction 3 = {A, B, C, DD}`. Your task is to utilize Spark to find all the similar transaction pairs **across different years**. 

**Output Format**: The output file contains all the similar transactions together with their similarities. The output format is `(InvoiceNo1,InvoiceNo2):similarity value`. In each pair, the transactions must be from **different years** with `InvoiceNo1` $<$ `InvoiceNo2`. There should be no duplicates in the output results. The pairs are sorted in ascending order (by the first and then the second). Given the sample dataset above with the threshold $0.5$, the output result should be: 

~~~txt
(1,3):0.75
(2,3):0.75
~~~

**(1,2): 0.5 is not returned since transaction 1 and 2 are in the same year.**

**Code Format**: The code template has been provided. Your code should take three parameters: the input file, the output folder, and the similarity threshold tau. You need to use the command below to run your code: 

~~~console
$ spark-submit project3.py input output tau
~~~

## Submission

**Deadline**: Wednesday 22 November 11:59:59 PM

If you need an extension, please apply for a special consideration via “myUNSW” first. You can submit multiple times before the due date and we will only mark your final submission. To prove successful submission, please take a screenshot as the assignment submission instructions show and keep it to yourself. If you have any problems with submissions, please email siqing.li@unsw.edu.au or yi.xu10@student.unsw.edu.au. 

## Late submission penalty

5\% reduction of your marks for up to 5 days, submissions delayed for over 5 days will be rejected.

## Some notes

- You need to design an exact approach to finding similar records.
- You cannot compute the pairwise similarities.
- Regular Python programming is not permitted in project3.
- When testing the correctness and efficiency of submissions, all the code will be run with two local threads using the default setting of Spark. Please be careful with your runtime and memory usage.
- Please revisit part II of  Week 8 Thursday slides before strating. 
- Check the paper mentioned in slides if you want to know more details [Efficient Parallel Set-Similarity Joins Using MapReduce. SIGMOD’10](https://flamingo.ics.uci.edu/pub/sigmod10-vernica.pdf)

## Optional (this will not be marked)

You can try to run it in Google Dataproc to see the power of distributed computation, where your code should scale well with the number of nodes used in a cluster. Create a project, test everything on your local computer, and finally do it in Google Dataproc. 

Create a bucket with the name `comp9313-<YOUR_STUDENTID>` in Dataproc. Create a folder `project3` in this bucket for holding the input files. You can create three clusters in Dataproc to run the same job: 
- Cluster1 - 1 master node and 2 worker nodes;
- Cluster2 - 1 master node and 4 worker nodes;
- Cluster3 - 1 master node and 6 worker nodes.

For both master and worker nodes, select n1-standard-2 (2 vCPU, $7.5GB$ memory).

Unzip and upload the given large data set to your bucket and set $T$ to 0.85 to run your program.

## Marking Criteria

Your source code will be inspected and marked based on readability and ease of understanding. The efficiency and scalability of this project are very important and will be evaluated as well.

- Submission can be compiled and run on Spark => $+6$ 
- Accuracy (no unexpected pairs, no missing pairs, correct order, correct similarity scores, correct format) => $+5$
- Efficiency (rules are shown as follows) => $+9$ 
  - The rank of runtime (using two local threads): 
  - Correct results: $0.9 \times (10 - \lfloor\frac{\text{rank percentage} - 1}{10}\rfloor)$, e.g., top 10\% => $9$
  - Incorrect results: $0.4 \times (10 - \lfloor\frac{\text{rank percentage} - 1}{10}\rfloor)$
- Code format and structure, readability, and documentation, including the description of the optimization techniques used => $+2$
