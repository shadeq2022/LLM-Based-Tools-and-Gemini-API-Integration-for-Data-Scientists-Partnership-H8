import streamlit as st
import pandas as pd
import numpy as np


# 1. Basic Text Components
st.title("Streamlit Basic Tutorial")
st.write("""
## Welcome to Streamlit!
This app will guide you through basic to advanced Streamlit components.
Each section demonstrates a different feature with explanations.
""")

# 2. Text Input
st.header("1. Text Input")
st.write("""
`st.text_input()` creates a simple text field where users can enter text.
The value is stored in the variable `user_input`.
""")
user_input = st.text_input("Enter your name", "Type here...")
st.write(f"Hello, {user_input}!")

# 3. Buttons
st.header("2. Buttons")
st.write("""
`st.button()` creates a clickable button. 
When clicked, it returns `True` once (then resets to `False`).
""")
if st.button("Click me!"):
    st.write("Button was clicked!")

# 4. Checkbox
st.header("3. Checkboxes")
st.write("""
`st.checkbox()` creates a toggle switch that returns `True` when checked.
""")
show_content = st.checkbox("Show secret message")
if show_content:
    st.write("You found the secret message!")

# 5. Select Box
st.header("4. Select Box")
st.write("""
`st.selectbox()` creates a dropdown menu for selecting one option.
""")
option = st.selectbox(
    "Choose your favorite color",
    ("Red", "Blue", "Green", "Yellow")
)
st.write(f"You selected: {option}")

# 6. Slider
st.header("5. Sliders")
st.write("""
`st.slider()` creates an interactive slider for selecting numeric values.
""")
age = st.slider("How old are you?", 0, 100, 25)
st.write(f"I'm {age} years old")

# 7. File Uploader
st.header("6. File Upload")
st.write("""
`st.file_uploader()` allows users to upload files to your app.
""")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write("File uploaded successfully!")

# 8. Progress Bar
st.header("7. Progress Indicators")
st.write("""
`st.progress()` shows a progress bar that you can update.
""")
import time
progress_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.01)
    progress_bar.progress(percent_complete + 1)
st.write("Progress complete!")

# 9. Sidebar
st.header("8. Sidebar")
st.write("""
`st.sidebar` creates a collapsible sidebar for additional controls.
""")
with st.sidebar:
    st.header("Sidebar Controls")
    st.write("Add widgets here to keep your main area clean.")
    if st.button("Sidebar Button"):
        st.write("Sidebar button clicked!")

# 10. Columns
st.header("9. Layout with Columns")
st.write("""
`st.columns()` helps organize content into multiple columns.
""")
col1, col2 = st.columns(2)
with col1:
    st.write("This is column 1")
    st.button("Button in column 1")
with col2:
    st.write("This is column 2")
    st.button("Button in column 2")

# 11. Expander
st.header("10. Expander")
st.write("""
`st.expander()` creates a collapsible section to hide/show content.
""")
with st.expander("Click to see more"):
    st.write("This content was hidden!")
    st.image("https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png", 
             width=200)

# 12. Markdown
st.header("11. Markdown")
st.write("""
You can use Markdown formatting with `st.markdown()`.
""")
st.markdown("""
### Markdown Examples:
- **Bold text**
- *Italic text*
- [Links](https://streamlit.io)
- `Code snippets`
""")

# 13. Success/Info/Warning/Error Messages
st.header("12. Status Messages")
st.write("""
Streamlit provides special functions for status messages:
- `st.success()`
- `st.info()`
- `st.warning()`
- `st.error()`
""")
st.success("This is a success message!")
st.info("This is an info message")
st.warning("This is a warning")
st.error("This is an error message")

# 14. Charts
st.header("13. Data Visualization with Charts")
st.write("""
Streamlit integrates seamlessly with popular plotting libraries like Matplotlib, Altair, and Plotly.
Here are some examples using dummy data.
""")

# Line Chart
st.subheader("Line Chart")
st.write("""
`st.line_chart()` displays a line chart. It's great for showing trends over time.
""")
chart_data = pd.DataFrame(
    np.random.randn(20, 3), columns=["a", "b", "c"]
)
st.line_chart(chart_data)

# Bar Chart
st.subheader("Bar Chart")
st.write("""
`st.bar_chart()` displays a bar chart, useful for comparing quantities across categories.
""")
bar_data = pd.DataFrame(
    np.random.rand(5, 2), columns=["apples", "bananas"]
)
st.bar_chart(bar_data)

# Area Chart
st.subheader("Area Chart")
st.write("""
`st.area_chart()` is similar to a line chart but fills the area below the lines.
""")
area_data = pd.DataFrame(
    np.random.randn(20, 3), columns=["a", "b", "c"]
)
st.area_chart(area_data)

# Scatter Plot (using st.pyplot for Matplotlib)
st.subheader("Scatter Plot (Matplotlib)")
st.write("""
For more complex plots, you can use `st.pyplot()` with Matplotlib.
""")
import matplotlib.pyplot as plt

x = np.random.randn(100)
y = np.random.randn(100)

fig, ax = plt.subplots()
ax.scatter(x, y)
st.pyplot(fig)

# 15. Dataframes and Descriptive Statistics
st.header("14. Dataframes and Descriptive Statistics")
st.write("""
Streamlit can display dataframes and provide descriptive statistics easily.
""")

# Create a dummy dataframe
data = {
    'col1': np.random.rand(10),
    'col2': np.random.randint(1, 100, 10),
    'col3': np.random.choice(['A', 'B', 'C'], 10)
}
df = pd.DataFrame(data)

st.subheader("Displaying a Dataframe")
st.write("""
`st.dataframe()` displays an interactive table.
""")
st.dataframe(df)

st.subheader("Displaying a Static Table")
st.write("""
`st.table()` displays a static table.
""")
st.table(df)

st.subheader("Descriptive Statistics")
st.write("""
You can easily get descriptive statistics for your dataframe using `.describe()`.
""")
st.write(df.describe())