import streamlit as st
import plotly.graph_objects as go

"""
# CO2: Car steel production vs in-service

Exploring quoted claim [here](https://cleantechnica.com/2021/08/19/first-fossil-free-steel-delivered-to-volvo-cars-in-sweden/) that 35% of an internal combustion engine car's CO2 production comes from steel production at manufacturing. 

I have gone with UK-based values with sources jsut taking the top one Google throws out - see the little question mark tooltips by each slider. 

Edit `/app.py` to customize this app to your heart's desire :heart: or play with the sliders below. 
"""

MPG_US = 'mpg (US)'
MPG_UK = 'mpg (UK)'
L_100KM = 'L/100km'

in_service = {
    MPG_US : {
        'label' : 'Fuel efficiency, MPG (US gallons)',
        'unit_d' : 'miles',
        'unit_v' : 'gallon (US)',
        'efficiency': {
            'def' : int(36 /1.2), 
            'max' : 100,
            'source' : 'https://www.nimblefins.co.uk/cheap-car-insurance/average-mpg'
        },
        'co2_per_vol' : {
            'def' : 8.89,#kg/gal
            'max' : 20.0,
            'source' : 'https://www.eia.gov/environment/emissions/co2_vol_mass.php'
        },
        'longevity': {
            'def' : 100000,
            'max' : 300000
        }
    },
    MPG_UK : {
        'label' : 'Fuel efficiency, MPG (UK gallons)',
        'unit_d' : 'miles',
        'unit_v' : 'gallon (UK)',
        'efficiency': {
            'def' : 36, 
            'max' : 100,
            'source' : 'https://www.nimblefins.co.uk/cheap-car-insurance/average-mpg'
        },
        'co2_per_vol' : {
            'def' : 8.89 * 1.2, # convservsion us gal to uk
            'max' : 20.0,
            'source' : 'https://www.eia.gov/environment/emissions/co2_vol_mass.php'
        },
        'longevity': {
            'def' : 100000,
            'max' : 300000
        }
    },
    L_100KM : {
        'label' : 'Fuel efficiency, L/100km',
        'unit_d' : 'km',
        'unit_v' : 'litre',
        'efficiency': {
            'def' : int(282.481/36),
            'max' : 30,
            'source' : 'https://www.nimblefins.co.uk/cheap-car-insurance/average-mpg'
        },
        'co2_per_vol' : {
            'def' : 8.89 * 0.26, # us gal to litres
            'max' : 20.0,
            'source' : 'https://www.eia.gov/environment/emissions/co2_vol_mass.php'
        },
        'longevity': {
            'def' : 200000,
            'max' : 500000
        }
        
    }
}


with st.echo(code_location='below'):

    st.header("Production")
    mass_steel_car = st.slider("Mass of steel in car (kg)",
        0,
        3000,
        900,
        help='https://www.worldsteel.org/steel-by-topic/steel-markets/automotive.html'
    )

    percent_steel = st.slider(
        "Percentage steel, by weight (%)",
        0,100,
        65,
        help = 'https://www.worldautosteel.org/life-cycle-thinking/recycling/'
    )

    percent_recycled = st.slider(
        "% recycled steel",
        0,
        100,
        25,
        help = 'https://www.worldautosteel.org/life-cycle-thinking/recycling/'
    )
    
    co2_steel = st.slider(
        "Tonnes of CO2 per tonne of steel (blast furnace)", 
        0.0, 
        5.0, 
        1.85,
        help = 'https://www.mckinsey.com/industries/metals-and-mining/our-insights/decarbonization-challenge-for-steel'
    )


    # ~~~~~~~~~~~~~~~~~~~~~~~~

    st.header("In-Service")
    st.text("This is the CO2 produced by the vehicle over lifetime, prior to being scrapped")
    st.text("Only includes the CO2 produced from burning fuel in a petrol internal combustion engine (ICE)")

    units = st.radio(
        "Units",
        (MPG_UK,L_100KM,MPG_US )
    )



    fuel_usage = st.slider(in_service[units]['label'], 
        0, 
        in_service[units]['efficiency']['max'],
        in_service[units]['efficiency']['def'],
        help = in_service[units]['efficiency']['source']
    )
    co2_per_vol = st.slider(
        f"kg CO2 per {in_service[units]['unit_v']} of fuel", 
        value = in_service[units]['co2_per_vol']['def'],
        max_value = in_service[units]['co2_per_vol']['max'],
        help = in_service[units]['co2_per_vol']['source']
    )

    distance = st.slider(
        f"Car longevity ({in_service[units]['unit_d']})",
        0,
        in_service[units]['longevity']['max'],
        in_service[units]['longevity']['def']
    )

    if units == MPG_UK or units == MPG_US:
        M_service = ((distance / fuel_usage) * co2_per_vol)/1000 
    else: 
        M_service = distance *(fuel_usage/100) * co2_per_vol/1000



    M_production = (mass_steel_car * (1-percent_recycled/100) * co2_steel)/1000 # mass (tonnes) CO2 from production

    colors = ['gold', 'mediumturquoise']

    fig = go.Figure(data=[go.Pie(labels=['Production','In-service'],
                                values=[M_production,M_service])])
    fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))


    st.plotly_chart(
        fig
    )

