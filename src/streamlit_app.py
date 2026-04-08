import streamlit as st
from pathlib import Path
from estimation import execute_regressions, generate_data
from plots import get_figure, get_table

st.set_page_config(page_title="Simpson's Paradox", layout="wide")

tab1, tab2, tab3 = st.tabs(["Simpson's Paradox", "Code", "References"])

with tab1:

        st.markdown(
"""
# Simpson's Paradox Explained

Simpson's paradox posits that, when we calculate correlations in aggregated data for a given population, we may find a positive (negative) correlation, but when the data are disaggregated, the correlation may have the opposite sign.

In this case, we simulate data such that we have a confounding variable, namely age. If age has an effect both on exercise and cholesterol, not taking it into account when performing our estimation will render us a biased estimator of the correlation between cholesterol and exercise. In this case, the bias is large enough that it reverts the sign: our correlation initially is positive, but when we segregate by age, the correlation is negative.

The data generating process is illustrated by the DAG further down below.
"""
        )
        col1, col2 = st.columns([1, 2])
        st.write("---")

        with col1:
                st.markdown("### Options")
                segregated = st.checkbox(label="Segregate by age")
                fit_line = st.checkbox(label="Show regression line", value=True)
                st.write("---")
                st.markdown("### Data Controls")
                seed = st.number_input("Random seed", min_value=0, max_value=9999, value=42, step=1)
                n_samples = st.slider("Sample size", min_value=100, max_value=5000, value=1000, step=100)

        @st.cache(allow_output_mutation=True)
        def load_data(n, seed):
                data = generate_data(n=n, seed=seed)
                results, results_data = execute_regressions(data)
                return results, results_data

        results, results_data = load_data(n_samples, seed)

        all_age_groups = sorted(results_data["age_groups"].unique())
        with col1:
                selected_groups = st.multiselect(
                        "Age groups to display",
                        options=all_age_groups,
                        default=all_age_groups
                )

        if selected_groups:
                filtered_data = results_data[results_data["age_groups"].isin(selected_groups)]
                filtered_results = {
                        "aggregated": results["aggregated"],
                        "segregated": {k: v for k, v in results["segregated"].items() if k in selected_groups}
                }
        else:
                filtered_data = results_data
                filtered_results = results

        fig = get_figure(filtered_data, segregated, fit_line)
        table = get_table(filtered_results, segregated)

        with col1:
                st.markdown("### Regression Results")
                st.table(table)

        with col2:
                st.markdown("### Scatter Plot")
                st.plotly_chart(fig, use_container_width=True)
                st.write("---")
                st.markdown("### DAG")
                if segregated:
                        st.image("assets/segregated.png")
                else:
                        st.image("assets/aggregated.png")

with tab2:
        st.markdown("### Code")
        st.markdown("Our code is hosted in the following GitHub repository: https://github.com/alexanderquispe/python-dashboard-class-AQ")
        st.write("---")

        src_dir = Path(__file__).parent

        with st.expander("streamlit_app.py"):
                st.code(src_dir.joinpath("streamlit_app.py").read_text(), language="python")

        with st.expander("estimation.py"):
                st.code(src_dir.joinpath("estimation.py").read_text(), language="python")

        with st.expander("plots.py"):
                st.code(src_dir.joinpath("plots.py").read_text(), language="python")

with tab3:
        st.markdown("""
### References:

Glymour, Madelyn, Judea Pearl, and Nicholas P. Jewell. Causal inference in statistics: A primer. John Wiley & Sons, 2016.
"""
)
