
import streamlit as st
import pandas as pd
import bibtexparser
from io import StringIO

# Función para leer archivos BIBTEX y convertirlos en un DataFrame
def bibtex_to_dataframe(bibtex_content):
    bib_database = bibtexparser.loads(bibtex_content)
    entries = bib_database.entries
    return pd.DataFrame(entries)

# Título de la aplicación
st.title("Unir archivos BIBTEX de Scopus y Web of Science")

# Subir archivos de Scopus y Web of Science
scopus_file = st.file_uploader("Sube el archivo Scopus (.bib)", type=["bib"])
wos_file = st.file_uploader("Sube el archivo Web of Science (.bib)", type=["bib"])

if scopus_file and wos_file:
    # Leer los archivos cargados
    scopus_content = StringIO(scopus_file.getvalue().decode("utf-8"))
    wos_content = StringIO(wos_file.getvalue().decode("utf-8"))
    
    # Convertir a DataFrames
    scopus_df = bibtex_to_dataframe(scopus_content.read())
    wos_df = bibtex_to_dataframe(wos_content.read())
    
    # Unir los dos DataFrames y eliminar duplicados
    combined_df = pd.concat([scopus_df, wos_df], ignore_index=True).drop_duplicates()

    # Guardar la base de datos combinada en un archivo Excel
    combined_df.to_excel("database.xlsx", index=False)

    # Botón para descargar el archivo Excel
    st.success("¡Archivos combinados con éxito!")
    st.download_button(
        label="Descargar archivo Excel",
        data=open("database.xlsx", "rb"),
        file_name="database.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Por favor sube los archivos BIBTEX de Scopus y Web of Science.")
