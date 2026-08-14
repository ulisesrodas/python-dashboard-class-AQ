# Ejecutar en Terminal: pip install pandas plotly

import plotly.graph_objects as go
import pandas as pd

def get_figure(plot_data, segregated, fit_line):
        fig = go.Figure(layout = go.Layout(width=900))
        fig.update_layout(
                xaxis_title="Exercise (hours/week)",
                yaxis_title="Cholesterol (mg/dL)"
        )
        if not segregated:
                fig.add_trace(go.Scatter(
                        x = plot_data.exercise,
                        y = plot_data.cholesterol,
                        mode = "markers",
                        showlegend = False,
                        marker_color = "black"
                ))
                if fit_line:
                        sorted_data = plot_data.sort_values("exercise")
                        fig.add_trace(go.Scatter(
                                x = sorted_data.exercise,
                                y = sorted_data.aggregated_fit,
                                mode = "lines",
                                showlegend = False,
                                marker_color = "red"
                        ))
                        fig.add_trace(go.Scatter(
                                x = sorted_data.exercise,
                                y = sorted_data.aggregated_ci_upper,
                                mode = "lines",
                                line = dict(width=0),
                                showlegend = False
                        ))
                        fig.add_trace(go.Scatter(
                                x = sorted_data.exercise,
                                y = sorted_data.aggregated_ci_lower,
                                mode = "lines",
                                line = dict(width=0),
                                fill = "tonexty",
                                fillcolor = "rgba(255, 0, 0, 0.15)",
                                showlegend = False
                        ))
                return fig
        for age, group in plot_data.groupby("age_groups"):
                fig.add_trace(go.Scatter(
                        x = group.exercise,
                        y = group.cholesterol,
                        mode = "markers",
                        name = age
                ))
                if fit_line:
                        sorted_group = group.sort_values("exercise")
                        fig.add_trace(go.Scatter(
                                x = sorted_group.exercise,
                                y = sorted_group.disaggregated_fit,
                                mode = "lines",
                                showlegend = False,
                                marker_color = "red"
                        ))
                        fig.add_trace(go.Scatter(
                                x = sorted_group.exercise,
                                y = sorted_group.disaggregated_ci_upper,
                                mode = "lines",
                                line = dict(width=0),
                                showlegend = False
                        ))
                        fig.add_trace(go.Scatter(
                                x = sorted_group.exercise,
                                y = sorted_group.disaggregated_ci_lower,
                                mode = "lines",
                                line = dict(width=0),
                                fill = "tonexty",
                                fillcolor = "rgba(255, 0, 0, 0.15)",
                                showlegend = False
                        ))
        return fig

def get_table(results: dict[str, dict], segregated):
        if not segregated:
                results = results["aggregated"]
                results_table = pd.DataFrame({
                        "Age Group": ["[10 - 50]"],
                        "Estimate": [results["beta_2"]],
                        "Pr(>|t|)": [results["p_value"]],
                        "R²": [results["r_squared"]]
                })
                return results_table
        age_group = []
        beta = []
        p_value = []
        r_squared = []
        results = results["segregated"]
        for age, measures in results.items():
                age_group.append(age)
                beta.append(measures["beta_2"])
                p_value.append(measures["p_value"])
                r_squared.append(measures["r_squared"])
        results_table = pd.DataFrame({
                "Age Group": age_group,
                "Estimate": beta,
                "Pr(>|t|)": p_value,
                "R²": r_squared
        })
        return results_table
