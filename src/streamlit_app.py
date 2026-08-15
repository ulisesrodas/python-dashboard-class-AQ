import streamlit as st
from pathlib import Path
from estimation import execute_regressions, generate_data
from plots import get_figure, get_table

st.set_page_config(page_title="Simpson's Paradox", layout="wide")

tab1, tab2, tab3 = st.tabs(["Paradoja de Simpson", "Código", "Referencias"])

# Relleno de información al tab1:
with tab1:

        st.markdown(
"""
# Paradoja de Simpson

La paradoja de Simpson establece que, al calcular correlaciones en datos agregados de una población determinada, podemos encontrar una correlación positiva (o negativa), pero al desagregar los datos, la correlación puede presentar el signo opuesto.

En este caso, simulamos datos que incluyen una variable de confusión: la edad. Si la edad influye tanto en el ejercicio como en el colesterol, no tenerla en cuenta al realizar la estimación dará lugar a un estimador sesgado de la correlación entre el colesterol y el ejercicio. Aquí, el sesgo es lo suficientemente grande como para invertir el signo: la correlación inicial es positiva, pero al segmentar los datos por edad, la correlación resulta negativa.

El proceso de generación de datos se ilustra mediante el DAG que aparece más abajo.
"""
        )
        col1, col2 = st.columns([1, 2])
        st.write("---")

        with col1:
                st.markdown("### Opciones")
                segregated = st.checkbox(label="Segregados por edad")
                fit_line = st.checkbox(label="Mostrar línea de regresión", value=True)
                st.write("---")
                st.markdown("### Controles de Datos")
                seed = st.number_input("Semilla aleatoria", min_value=0, max_value=9999, value=42, step=1)
                n_samples = st.slider("Tamaño de la muestra", min_value=100, max_value=5000, value=1000, step=100)

        @st.cache_data
        def load_data(n, seed):
                data = generate_data(n=n, seed=seed)
                results, results_data = execute_regressions(data)
                return results, results_data

        results, results_data = load_data(n_samples, seed)

        all_age_groups = sorted(results_data["age_groups"].unique())
        with col1:
                selected_groups = st.multiselect(
                        "Grupos de edad",
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
                st.markdown("### Resultados de la Regresión")
                st.table(table)

        with col2:
                st.markdown("### Diagrama de Dispersión")
                st.plotly_chart(fig, use_container_width=True)
                st.write("---")
                st.markdown("### DAG")
                if segregated:
                        st.image("assets/segregated.png")
                else:
                        st.image("assets/aggregated.png")

with tab2:
        st.markdown("### Código")
        st.markdown("El código está alojado en el siguiente repositorio de GitHub: https://github.com/alexanderquispe/python-dashboard-class-AQ")
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
### Referencias:

Glymour, Madelyn, Judea Pearl, and Nicholas P. Jewell. Causal inference in statistics: A primer. John Wiley & Sons, 2016.
"""
)
