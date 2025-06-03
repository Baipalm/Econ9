import streamlit as st

st.title('How can you apply inquiry based learning to Economics')
st.header('Abstract')
st.markdown('''This site is made as an economic analysis project. The goal is to find a way to apply inquiry based learning to Economics. 
To accomplish this goal we've decided to construct a website which guides you through classic economic concepts such as the production possibility curve, supply and demand,etc.
If a person who does not knwo any economics is able to grasp intuitively how the concepts work on their own then we consider ourselves to be successful. The site consists of two 
modes, questions and experimentations.''')
st.header('How to use this site')
st.markdown('''The site consists of two 
modes, - questions   
- experimentations.''')
st.write("**Questions look like this**")

with st.expander("Click to show answer"):
    st.write("""
   For questions spend time thinking about the answers, use the graph to help but make sure to not peak unless you get very stuck :)""")
st.markdown('')

st.write('Graphs with widgets are like this')
import streamlit as st

st.title("Slider-Controlled Text Reveal")

# 1) Define the full text you want to reveal
full_text = """\
Be sure to play around with the graphs and experiment. Follow your curiosity!.\
"""

# 2) Compute the maximum “slider value” = length of the string
max_chars = len(full_text)

# 3) Render a slider from 0→max_chars
#    As you move the slider, the app reruns and displays text[:n_chars]
n_chars = st.slider(
    label="Reveal how many characters:",
    min_value=0,
    max_value=max_chars,
    value=0,
)

# 4) Show only the first n_chars of full_text
#    (You can also slice by words or sentences if you prefer.)
st.write(full_text[:n_chars])

