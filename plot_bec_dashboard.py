import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

with open("/home/wayne/Desktop/qcd_bridge/bec_goldstone_results/bec_dynamics.json") as f:
    d = json.load(f)

df = pd.DataFrame({
    "time": d["times"],
    "left": d["left_density"],
    "right": d["right_density"],
    "com_x": d["com_x"]
})

fig = make_subplots(rows=2, cols=1, subplot_titles=("Lobe Populations", "Center of Mass"))
fig.add_trace(go.Scatter(x=df.time, y=df.left,  name="Left lobe",  line=dict(color="blue")), row=1, col=1)
fig.add_trace(go.Scatter(x=df.time, y=df.right, name="Right lobe", line=dict(color="orange")), row=1, col=1)
fig.add_trace(go.Scatter(x=df.time, y=df.com_x, name="COM x", line=dict(color="green", dash="dash")), row=2, col=1)

fig.update_layout(height=800, title="BEC Goldstone Dynamics - 15 time units")
fig.write_html("bec_dashboard.html")
fig.show()
