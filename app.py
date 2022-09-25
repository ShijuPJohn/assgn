import sys

import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Template

data_file = open("data.csv", 'r')
data_file.readline()
data = data_file.readlines()
data_file.close()
o_list = [i.strip().split(',') for i in data]
base_template_str = """
<!DOCTYPE html>
<html>
<head>
<title>{{title}}</title>
</head>
<body>
{{body}}
</body>
</html>
"""
body_template_str = """
<h1>{{body_title}}</h1>
<div>
{{main_body}}
</div>
"""
t1_str = """
<table border>
<tr><th>Student id</th><th>Course id</th><th>Marks</th></tr>
{% for n in t_arr %} 
<tr>    <td>{{n[0]}}</td>   <td>{{n[1]}}</td>   <td>{{n[2]}}</td>   </tr>
{% endfor %}
<tr><td colspan="2">Total Marks</td><td>{{total}}</td></tr>
</table>
"""
t2_str = """
<table border>
<tr><th>Average Marks</th><th>Maximum Marks</th></tr>
<tr><td>{{avg}}</td><td>{{mx}}</td></tr>
</table>
<img src="hist.png" alt="histogram">
"""
error_template_str = """
<h1>Wrong Inputs</h1>
<p>Something went wrong</p>
"""
base_template = Template(base_template_str)
body_template = Template(body_template_str)
t1 = Template(t1_str)
t2 = Template(t2_str)
error_template = Template(error_template_str)
try:
    if sys.argv[1] == '-s':
        tot_marks = 0
        n_arr = []
        not_found = True
        for i in o_list:
            if i[0] == sys.argv[2]:
                not_found = False
                n_arr.append([sys.argv[2], i[1], i[2]])
                tot_marks += int(i[2])
        if not_found:
            raise Exception
        html_file = open("output.html", 'w')
        html_file.write(
            base_template.render(title="Student Page",
                                 body=body_template.render(body_title="Student Details",
                                                           main_body=t1.render(
                                                    t_arr=n_arr, total=str(tot_marks))))
        )
        html_file.close()
    elif sys.argv[1] == '-c':
        ol = [int(i[2]) for i in o_list if i[1].strip() == sys.argv[2].strip()]
        if len(ol) == 0:
            raise Exception
        avg = sum(ol) / len(ol)
        mx = max(ol)
        npa = np.array(ol)
        plt.hist(npa, bins=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        plt.xlabel("Marks")
        plt.ylabel("Frequency")
        plt.savefig("hist.png")
        html_file = open("output.html", 'w')
        html_file.write(
            base_template.render(title="Course Page",
                                 body=body_template.render(
                                     body_title="Course Details",
                                     main_body=t2.render(avg=avg, mx=mx)))
        )
        html_file.close()
except Exception:
    html_file = open("output.html", 'w')
    html_file.write(
        base_template.render(title="Something went wrong",
                             body=error_template.render())
    )
    html_file.close()