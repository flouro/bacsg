import streamlit as st
import pandas as pd

# Constants for BAC calculation
LEGAL_BAC_LIMIT = 0.08  # Legal limit in Singapore
ALCOHOL_DENSITY = 0.789  # g/ml, density of alcohol
METABOLISM_RATE = 0.015  # Average alcohol metabolism rate

# BAC calculation function
def calculate_bac(drinks, weight, gender, hours_since_last_drink):
    total_grams_alcohol = sum(d['ABV %'] * d['Volume (ml)'] * ALCOHOL_DENSITY / 100 for d in drinks)
    print(f"totalgramsalcohol:{total_grams_alcohol}")
    body_water_constant = 0.68 if gender == 'Male' else 0.55
    
    # Adjusted Metabolism calculation
    metabolism_loss = METABOLISM_RATE * hours_since_last_drink * 1000 * body_water_constant

    weight_grams = weight * 1000 * body_water_constant
    bac = (total_grams_alcohol - metabolism_loss) / weight_grams *100
    return max(bac, 0)  # Ensure BAC is not negative

# Title for the application
st.title('Blood Alcohol Content Tracker')

# Collect user's physiological details for BAC calculation
with st.form("user_details_form"):
    st.write("Enter Your Details")
    weight = st.number_input('Weight (in kilograms)', min_value=0.0, format="%.2f", key='user_weight')
    gender = st.radio('Gender', ('Male', 'Female'), key='user_gender')
    hours = st.number_input('Hours since last drink', min_value=0.0, format="%.1f", key='hours_since_last_drink')

    submit_details = st.form_submit_button('Save Details')
    if submit_details:
        st.session_state['user_details'] = {
            'Weight': weight,
            'Gender': gender,
            'Hours since last drink': hours
        }
        st.success('Details saved!')

# Creating a form for alcohol intake data input
with st.form("alcohol_input"):
    st.write("Enter the details of your drink")

    abv = st.number_input('Alcohol by Volume (ABV %)', min_value=0.0, format="%.2f", key='drink_abv')
    volume = st.number_input('Volume of alcohol per drink (in ml)', min_value=0.0, format="%.2f", key='drink_volume')
    quantity = st.number_input('Quantity of drinks', min_value=0, step=1, key='drink_quantity')

    add_drink = st.form_submit_button('Add Drink')
    if add_drink:
        if 'drinks' not in st.session_state:
            st.session_state['drinks'] = []
        for _ in range(int(quantity)):
            st.session_state['drinks'].append({
                'ABV %': abv,
                'Volume (ml)': volume
            })
    if 'drinks' in st.session_state and st.session_state['drinks']:
        st.write("Drinks Consumed:")
        st.write(pd.DataFrame(st.session_state['drinks']))

# Button to calculate BAC
if st.button('Calculate BAC') and 'user_details' in st.session_state and 'drinks' in st.session_state and st.session_state['drinks']:
    bac = calculate_bac(
        st.session_state['drinks'],
        st.session_state['user_details']['Weight'],
        st.session_state['user_details']['Gender'],
        st.session_state['user_details']['Hours since last drink']
    )
    st.write(f"Your Blood Alcohol Content (BAC) is: {bac:.4f}")
    if bac > LEGAL_BAC_LIMIT:
        st.error("Your BAC is above the legal limit in Singapore (0.08%). Do not drive.")
    else:
        st.success("Your BAC is within the legal limit in Singapore. Please still consider your ability to drive safely.")
    st.session_state['drinks'] = []

st.markdown("""
    <h2 style='text-align: center;'>
        Made by <a href='https://placeholder-website.com' style='font-weight: bold; color: deepskyblue; text-decoration: none;'>
        <span style='color: white; background-color: MediumSeaGreen; border-radius: 12px; padding: 3px 8px; box-shadow: 1px 1px 3px grey;'> Jones </span></a>
    </h2>
    """, unsafe_allow_html=True)

