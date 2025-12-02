# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 10:00:47 2025

@author: abdirahmaan.barkhad
"""

import streamlit as st
import random
import pandas as pd

# Custom CSS for green button
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 12em;
        font-size: 18px;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FITNESS FUNCTION (målhöjd = 5.5 m)
# =========================================================
def fitness(height, target=5.5):
    """
    Fitness baseras på hur nära giraffen är målhöjden (5.5 m).
    Max fitness = 1.0 när höjd = target.
    """
    diff = abs(height - target)
    fitness_value = max(0.0, 1.0 - (diff / target))  # Normaliserad fitness
    return fitness_value

# =========================================================
# GA COMPONENTS
# =========================================================
def initialize_population(size, hmin, hmax):
    return [random.uniform(hmin, hmax) for _ in range(size)]

def select_parent(population):
    fits = [fitness(h) for h in population]
    total_fit = sum(fits)
    if total_fit == 0:
        return random.choice(population)

    r = random.uniform(0, total_fit)
    c = 0
    for indiv, fit in zip(population, fits):
        c += fit
        if c >= r:
            return indiv

def crossover(p1, p2, rate):
    if random.random() > rate:
        return p1, p2
    a = random.random()
    c1 = a * p1 + (1 - a) * p2
    c2 = a * p2 + (1 - a) * p1
    return c1, c2

def mutate(value, rate, strength):
    if random.random() < rate:
        value += random.uniform(-strength, strength)
    return value

# =========================================================
# STREAMLIT UI
# =========================================================
st.title("🦒 Giraffe Evolution Simulator")
st.write("""
Use this tool to simulate giraffe height evolution using a Genetic Algorithm.  
Simulatorn strävar efter en optimal giraffhöjd på 5,5 meter.
""")

# ------------------------
# INPUT PANEL
# ------------------------
st.header("Simulation Settings")
col1, col2 = st.columns(2)

with col1:
    pop_size = st.number_input("Population Size", 2, 500, 20)
    generations = st.number_input("Number of Generations", 1, 500, 30)
    init_min = st.number_input("Initial Height Minimum (m)", 0.1, 10.0, 2.9)
    init_max = st.number_input("Initial Height Maximum (m)", 0.1, 10.0, 3.9)

with col2:
    mutation_rate = st.slider("Mutation Rate", 0.0, 1.0, 0.1)
    mutation_strength = st.slider("Mutation Strength (meters)", 0.0, 2.0, 0.12)
    crossover_rate = st.slider("Crossover Rate", 0.0, 1.0, 0.2)

# ------------------------
# IMAGE PLACEHOLDER
# ------------------------
st.subheader("MEME")
st.image(
    "https://raw.githubusercontent.com/abarkhadle999-cpu/giraffe-simulator/main/short%20neck%20giraffe%20meme.gif",
    caption="Giraffe MEME",
    use_column_width=True
)

# =========================================================
# RUN SIMULATION
# =========================================================
if st.button("Run Evolution Simulation"):
    population = initialize_population(pop_size, init_min, init_max)
    best_list = []

    for gen in range(generations):
        new_pop = []

        while len(new_pop) < pop_size:
            p1 = select_parent(population)
            p2 = select_parent(population)

            c1, c2 = crossover(p1, p2, crossover_rate)
            c1 = mutate(c1, mutation_rate, mutation_strength)
            c2 = mutate(c2, mutation_rate, mutation_strength)

            new_pop.extend([c1, c2])

        population = new_pop[:pop_size]

        best = max(population, key=lambda h: fitness(h))
        best_fit = fitness(best)

        best_list.append([gen+1, best, best_fit])

    df = pd.DataFrame(best_list, columns=["Generation", "Best Height (m)", "Fitness"])

    st.success("Simulation Completed!")
    st.line_chart(df.set_index("Generation")["Best Height (m)"])

# =========================================================
# Visa resultat och spara CSV
# =========================================================
st.subheader("Best Height per Generation")

if 'df' in locals():
    st.dataframe(df)

    # -----------------------------
    # SAVE RESULTS BUTTON (CSV)
    # -----------------------------
    st.subheader("Save Results (CSV)")

    # Sortera dataframe efter Generation
    df_sorted = df.sort_values("Generation")

    # Skapa CSV i minnet
    import io
    csv_data = df_sorted.to_csv(index=False).encode("utf-8")

    # Nedladdningsknapp
    st.download_button(
        label="Download CSV File",
        data=csv_data,
        file_name="giraffe_evolution_results.csv",
        mime="text/csv"
    )

else:
    st.warning("Data finns inte än. Kör först simuleringen för att generera data.")




