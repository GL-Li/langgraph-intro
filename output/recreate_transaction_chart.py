import json
import base64
import numpy as np
import plotly.io as pio
from plotly import graph_objects as go

def decode_plotly_binary_data(b64_data):
    """Decode Plotly's binary data format"""
    decoded = base64.b64decode(b64_data)
    dtype = np.dtype('<f8')  # Little-endian float64
    return np.frombuffer(decoded[8:], dtype=dtype)  # Skip first 8 bytes (header)

# Load the original chart data
with open('total_transaction_by_type.json') as f:
    chart_data = json.load(f)

# Extract and decode the y-axis data
y_data = chart_data['data'][0]['y']['bdata']
amounts = decode_plotly_binary_data(y_data)

# Recreate the figure using the original configuration
fig = go.Figure(
    data=[go.Bar(
        x=chart_data['data'][0]['x'],
        y=amounts,
        marker_color=chart_data['data'][0]['marker']['color'],
        hovertemplate=chart_data['data'][0]['hovertemplate']
    )],
    layout=chart_data['layout']
)

# Save as interactive HTML
pio.write_html(fig, 'total_transaction_by_type_chart.html', auto_open=True)
