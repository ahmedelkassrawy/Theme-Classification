import gradio as gr
import pandas as pd
import plotly.express as px
from theme_classifier import ThemeClassifier
import os

def get_themes(theme_list_str, subtitles_path, save_path):
    print("Button clicked!")  # Debugging
    print(f"Themes: {theme_list_str}, Subtitles Path: {subtitles_path}, Save Path: {save_path}")  # Debugging

    if not os.path.exists(subtitles_path):
        return "Error: Subtitles file not found!"

    # Split theme list and initialize classifier
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)

    # Remove 'dialogue' from the theme list
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    output_df = output_df[theme_list]

    # Sum scores for each theme
    output_df = output_df.sum().reset_index()
    output_df.columns = ['Theme', 'Score']

    # Create BarPlot using Plotly
    fig = px.bar(
        output_df,
        x="Score",
        y="Theme",
        title="Series Themes",
        orientation="h",
        text="Score"
    )

    return fig

with gr.Blocks() as iface:
    # Theme Classification Section
    with gr.Row():
        with gr.Column():
            gr.HTML("<h1>Theme Classification (Zero Shot Classifiers)</h1>")
            with gr.Row():
                with gr.Column():
                    plot = gr.Plot()
                with gr.Column():
                    theme_list = gr.Textbox(label="Themes")
                    subtitles_path = gr.Textbox(label="Subtitles or Script Path")
                    save_path = gr.Textbox(label="Save Path")
                    get_themes_button = gr.Button("Get Themes")
                    get_themes_button.click(
                        fn=get_themes,
                        inputs=[theme_list, subtitles_path, save_path],
                        outputs=[plot]
                    )

# Launch the Gradio app
iface.launch()
