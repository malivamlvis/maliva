# Maliva: Generating Hinted Queries Using Machine Learning for Middleware-Based Visualization
This repository hosts the source code of the paper `Maliva` submitted to SIGMOD 2022.

We provide a [Tutorial](https://github.com/malivamlvis/maliva/wiki) to run Maliva on top of PostgreSQL hosting 15 million NYC Taxi data.

Maliva is a middleware that optimizes visualization queries to compute results within a time limit. It adopts Machine Learning techniques to add `hints` to the original SQL queries to help the database optimizer choose proper indexes for generating an efficient physical plan.

![](https://github.com/malivamlvis/maliva/blob/main/pub/intro-slow-query.png "Traditional Middleware") ![](https://github.com/malivamlvis/maliva/blob/main/pub/intro-fast-query.png "Maliva Middleware")

The following figure shows the architecture of Maliva.

![](https://github.com/malivamlvis/maliva/blob/main/pub/architecture.png "Maliva Architecture")

The core module is the `ML-based Query Generator`. It enumerates different possible hinted SQL queries, asks the `Query Time Estimator (QTE)` to estimate the query time for each considered hinted query, and then decides one hinted query as the generated hinted SQL query. The Query Generator models the sequential decision-making of which hinted query to estimate as a Markov Decision Process model. It learns a good strategy from historical queries to balance the planning time and the querying time.

![](https://github.com/malivamlvis/maliva/blob/main/pub/maliva-vs-postgresql.png "Experiment Results on 100m Tweets")

The experiment results show that for 100 Million tweets dataset, for "hard" workloads where each query has only one viable plan (i.e. only one physical plan can meet the time budget requirement), Maliva using both an Accurate QTE and an Approximate QTE outperformed the original query plan generated by PostgreSQL significantly. The metric `Viable Query Percentage (%)` means that for an approach, how many of the generated hinted queries by Maliva (or physical plans by PostgreSQL) were `viable`, where viable means the total query response time was within the given time budget (e.g., 1 second)
