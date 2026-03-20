import matplotlib.pyplot as plt
import pandas as pd
import io

def generate_basic_plot(df, x_column, y_column, title="Basic Plot"):
    """
    Generates a simple line plot from a DataFrame and returns it as a PNG image.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df[x_column], df[y_column], marker="o")
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(title)
    ax.grid(True)

    # Save to buffer for Streamlit
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)

    return buffer
