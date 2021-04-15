import datetime
import os
import pickle
import random
import string
import sys
import traceback
from io import BytesIO, StringIO

import matplotlib.pyplot as plt
import pandas as pd
import shap
from flask import Response

from app.libs.global_varible import g
from app.models.node import Node


def change_node(node):
    from app.nodes import node_mapping

    try:
        return node_mapping[node.node_type](
            node.id,
            node.node_type,
            node.project_id,
            node.in_edges,
            node.out_edges,
            node.extra,
        )
    except KeyError:
        raise Exception("Node{}({}) not support".format(node.id, node.node_type))


def run_nodes(nodes, testing, thread):
    if not testing or thread:
        from flask_app import create_app

        app = create_app(test=testing, file_directory=getattr(g, "file_directory", None))
        app.app_context().push()
    fail_flag = False
    for node in nodes:
        if not testing:
            old_stdout = sys.stdout
            sys.stdout = open(node.join_path("log.txt"), "w")
        print("node-{}({}) run start".format(node.id, node.node_type))
        if fail_flag is False:
            try:
                node.run()
                node.finish()
                node.modify(status=Node.Status.FINISH)  # 成功
                print("node-{}({}) run success".format(node.id, node.node_type))
            except Exception:
                if testing and not thread:
                    raise  # pragma: no cover
                print(traceback.format_exc())
                fail_flag = True
                node.modify(status=Node.Status.FAILED)  # 失败
                print("node-{}({}) run failed: 节点运行出错".format(node.id, node.node_type))
        else:
            print("node-{}({}) run failed: 前序节点运行出错".format(node.id, node.node_type))
            node.modify(status=Node.Status.FAILED)  # 失败
        print("node-{}({}) run finish".format(node.id, node.node_type))
        if not testing:
            sys.stdout.close()
            sys.stdout = old_stdout


def change_columns(raw):
    res = set()
    try:
        raw = raw.replace(" ", "")
        parts = raw.split(",")
        while "" in parts:
            parts.remove("")
        for part in parts:
            if ":" in part:
                left, right = part.split(":")
                left = int(left)
                right = int(right)
                if left == right:
                    res.add(left)
                    continue
                sign = (right - left) // abs(right - left)
                res.update(set(range(left, right + sign, sign)))
            else:
                res.add(int(part))
    except ValueError:
        raise Exception("column should be integer")
    return list(res)


def get_files(path):
    res = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            res.append(
                {
                    "name": filename,
                    "type": "file",
                    "size": os.path.getsize(filepath),
                    "access_time": datetime.datetime.fromtimestamp(os.path.getatime(filepath)),
                    "create_time": datetime.datetime.fromtimestamp(os.path.getctime(filepath)),
                    "modify_time": datetime.datetime.fromtimestamp(os.path.getmtime(filepath)),
                }
            )
        elif os.path.isdir(filepath):
            res.append({"name": filename, "type": "dir"})
    return res


def get_random_string(length):
    return "".join(random.sample(string.ascii_letters + string.digits, length))


def split_csv(data):
    data = data.split("\n")
    header = data[0]
    r = []
    for i in data[1:]:
        if i == "":
            continue
        r.append(header + "\n" + i)
    return r


def get_predict(node, type_, start, end):
    if type_ == 1:
        x = pd.read_csv(node.join_path("x_train.csv", node.in_edges[0]))
    else:
        x = pd.read_csv(node.join_path("x_test.csv", node.in_edges[0]))
    count = x.shape[0]
    x = x[start:end]
    with open(node.join_path("x.model"), "rb") as f:
        model = pickle.load(f)
    y = model.predict(x, validate_features=False)
    y = pd.DataFrame(y)
    # x
    s_io = StringIO()
    x.to_csv(s_io, index=False)
    input_data = split_csv(s_io.getvalue())
    # y
    s_io = StringIO()
    y.to_csv(s_io, index=False)
    output_data = split_csv(s_io.getvalue())
    return {
        "input": [
            {
                "type": "csv",
                "data": input_data,
            },
        ],
        "output": [{"type": "csv", "data": output_data}],
        "meta": {"count": count},
    }


def get_force_plot(node, type_, data_id, shap_type):
    if type_ == 1:
        x = pd.read_csv(node.join_path("x_train.csv", node.in_edges[0]))
    else:
        x = pd.read_csv(node.join_path("x_test.csv", node.in_edges[0]))
    x = x[data_id - 1 : data_id]
    with open(node.join_path("x.model"), "rb") as f:
        model = pickle.load(f)
    explainer = shap.Explainer(model)
    shap_values = explainer(x)[0]
    if shap_type == 1:
        plot = shap.plots.force(shap_values, feature_names=x.columns)
        s_io = StringIO()
        shap.save_html(s_io, plot)
        save_html = StringIO()
        shap.save_html(save_html, plot)
        return Response(s_io.getvalue(), mimetype="text/html")
    else:
        shap.plots.waterfall(shap_values, show=False)
        b_io = BytesIO()
        plt.savefig(b_io)
        plt.close()
        return Response(b_io.getvalue(), mimetype="image/jpeg")


def get_predict_analysis(node, type_, shap_type):
    if type_ == 1:
        x = pd.read_csv(node.join_path("x_train.csv", node.in_edges[0]))
    else:
        x = pd.read_csv(node.join_path("x_test.csv", node.in_edges[0]))
    with open(node.join_path("x.model"), "rb") as f:
        model = pickle.load(f)
    explainer = shap.Explainer(model)
    shap_values = explainer(x)
    if shap_type in [1, 2]:
        if shap_type == 1:
            shap.plots.beeswarm(shap_values, show=False, plot_size=(25, 10))
        else:
            shap.plots.bar(shap_values, show=False)
        b_io = BytesIO()
        plt.savefig(b_io)
        plt.close()
        return Response(b_io.getvalue(), mimetype="image/jpeg")
    else:
        plot = shap.plots.force(explainer.expected_value, shap_values.values, shap_values.data, show=False)
        s_io = StringIO()
        shap.save_html(s_io, plot)
        save_html = StringIO()
        shap.save_html(save_html, plot)
        return Response(s_io.getvalue(), mimetype="text/html")
