import argparse
import numpy as np
from smart_query_estimator import Query_Estimator
from smart_util import Util


###########################################################
#  smart_train_query_estimator.py
#
#  -d  / --dimension       dimension: dimension of the queries. Default: 3
#  -sf / --sel_file        input file that holds queries' selectivities generated by smart_collect_queries_sels.py
#  -lf / --labeled_file    input file that holds queries' real running times generated by smart_label_queries.py
#  -op / --out_path        output path to save the models used by Query Estimator
#  -nj / --num_join        number of join methods. Default: 1
#
###########################################################


if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser(description="Train Query Estimator.")
    parser.add_argument("-d", "--dimension",
                        help="dimension: dimension of the queries. Default: 3",
                        type=int, required=False, default=3)
    parser.add_argument("-sf", "--sels_file",
                        help="sels_file: input file that holds queries' selectivities",
                        type=str, required=True)
    parser.add_argument("-lf", "--labeled_file",
                        help="labeled_file: input file that holds queries's real running times",
                        type=str, required=True)
    parser.add_argument("-op", "--out_path",
                        help="out_path: output path to save the models used by Query Estimator",
                        type=str, required=True)
    parser.add_argument("-nj", "--num_join", help="num_join: number of join methods. Default: 1", 
                        required=False, type=int, default=1)
    args = parser.parse_args()

    dimension = args.dimension
    queries_sels_file = args.sels_file
    labeled_queries_file = args.labeled_file
    out_path = args.out_path
    num_of_joins = args.num_join

    num_of_plans = Util.num_of_plans(dimension, num_of_joins)

    # 1. read queries' selectivities into memory
    queries_sels = Util.load_queries_sels_file(dimension, queries_sels_file)
    # Build queries_sels_map <id, query_sels>
    queries_sels_map = {}
    for query_sels in queries_sels:
        queries_sels_map[query_sels["id"]] = query_sels

    # 2. read queries' real running times into memory
    labeled_queries = Util.load_labeled_queries_file(dimension, labeled_queries_file, num_of_joins)

    # 3. new a Query Estimator
    query_estimator = Query_Estimator(dimension, num_of_joins)

    # 4. train the Query Estimator for all plans
    print("start training query estimator ...")
    # plan = 1 ~ num_of_plans
    for plan in range(1, num_of_plans + 1):
        xtr = []
        ytr = []
        sel_ids = Util.sel_ids_of_plan(plan, dimension, num_of_joins)
        for labeled_query in labeled_queries:
            id = labeled_query["id"]
            x = []
            query_sels = queries_sels_map[id]
            for sel_id in sel_ids:
                x.append(query_sels["sel_" + str(sel_id)])
            xtr.append(x)
            y = [labeled_query["time_" + str(plan)]]
            ytr.append(y)
        xtr = np.array(xtr)
        ytr = np.array(ytr)
        query_estimator.fit(plan, xtr, ytr)
        print("    plan [" + str(plan) + "] trained.")

    # 5. save Query Estimator models to files
    query_estimator.save(out_path)
    print("query estimator models saved.")
