import streamlit as st
import requests
import json

st.title("Xi Jinping Network Analysis")

# Input form
topic = st.text_input("Enter a topic to analyze")

if st.button("Analyze"):
    if topic:
        with st.spinner("Analyzing..."):
            try:
                # Make request to backend
                response = requests.post(
                    "http://127.0.0.1:5003/api/analyze",
                    json={"topic": topic, "options": {"depth": "quick"}}
                )
                response.raise_for_status()
                data = response.json()

                # Display results
                st.subheader("Research Summary")
                st.write(data["research"]["summary"])

                st.subheader("Key Insights")
                for insight in data["research"]["key_insights"]:
                    st.markdown(f"- {insight}")

                st.subheader("Main Themes")
                for theme in data["combined_analysis"]["main_themes"]:
                    st.markdown(f"- {theme}")

                st.subheader("Key Findings")
                for finding in data["combined_analysis"]["key_findings"]:
                    st.markdown(f"- {finding}")

                st.subheader("Recommendations")
                for rec in data["combined_analysis"]["recommendations"]:
                    st.markdown(f"- {rec}")

                st.subheader("Sources")
                for source in data["research"]["sources"]:
                    st.markdown(f"- {source}")

                st.subheader("Raw Response")
                st.json(data)

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to backend: {str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a topic to analyze")
