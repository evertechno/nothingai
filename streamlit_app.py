import streamlit as st
import google.generativeai as genai

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("AI Code Converter")
st.write("Convert code between different programming languages and options.")

# Select source and target languages
source_language = st.selectbox("Select the source language", 
                               ("Python", "JavaScript", "Java", "C++", "Go", "Ruby", "PHP", "Swift", "TypeScript", "Kotlin"))

target_language = st.selectbox("Select the target language", 
                               ("Python", "JavaScript", "Java", "C++", "Go", "Ruby", "PHP", "Swift", "TypeScript", "Kotlin"))

# Additional options for conversion
conversion_option = st.selectbox("Select the type of conversion", 
                                ("Full Program", "Function", "Class", "Method", "Variable"))

# Option to validate code before converting
validate_code = st.checkbox("Validate Code Before Converting", value=True)

# Code input field
code_input = st.text_area("Enter the code to be converted:", height=300)

# Button to generate converted code
if st.button("Convert Code"):
    if code_input:
        try:
            # Validate input code (basic syntax check)
            if validate_code:
                validation_prompt = f"Please check the syntax of this {source_language} code:\n\n{code_input}"
                validation_response = genai.GenerativeModel('gemini-1.5-flash').generate_content(validation_prompt)
                
                # If the model gives an error message about invalid code, display it
                if "error" in validation_response.text.lower():
                    st.error(f"Code Validation Error: {validation_response.text}")
                    return
                else:
                    st.success("Code syntax looks good!")

            # Prepare the prompt for AI code conversion
            conversion_prompt = f"Convert the following {source_language} {conversion_option.lower()} to {target_language}:\n\n{code_input}"

            # Load and configure the model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Generate response from the model
            response = model.generate_content(conversion_prompt)
            
            # Display the converted code in Streamlit
            st.write(f"Converted {source_language} {conversion_option} to {target_language}:")
            st.code(response.text, language=target_language.lower())
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some code to convert.")
