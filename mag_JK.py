import streamlit as st
import pandas as pd # Dodano pandas do czystszego wyświetlania danych

# --- Ustawienia Strony i Mikołaj (Santa Claus) ---

st.set_page_config(page_title="Prosty Magazyn (Streamlit + Ilość)", layout="wide")

# Wstawienie kodu HTML/CSS dla Mikołaja w rogu
santa_style = """
<style>
/* Klasa do pozycjonowania Mikołaja */
.santa-fixed {
    position: fixed;
    bottom: 20px; /* Odległość od dołu */
    right: 20px; /* Odległość od prawej */
    font-size: 60px; /* Rozmiar emoji */
    z-index: 1000; /* Zawsze na wierzchu */
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3); /* Lekki cień dla estetyki */
    pointer-events: none; /* Umożliwia klikanie pod nim */
}
</style>
<div class="santa-fixed">🎅</div>
"""
st.markdown(santa_style, unsafe_allow_html=True)


# --- Inicjalizacja Magazynu (Słownik Towarów) ---

# Magazyn jest teraz słownikiem: {"NAZWA_TOWARU": ilość_int}
if 'inventory' not in st.session_state:
    st.session_state.inventory = {
        "LAPTOP": 5, 
        "MONITOR": 10, 
        "KLAWIATURA": 2
    } # Przykładowe początkowe towary z ilościami

# --- Funkcje Magazynu ---

def add_item(item_name, quantity):
    """Dodaje towar i zadaną ilość do magazynu. Sumuje ilość, jeśli towar istnieje."""
    if item_name and quantity > 0:
        # Konwersja na wielkie litery i usunięcie białych znaków
        standardized_name = item_name.strip().upper()
        
        if standardized_name in st.session_state.inventory:
            st.session_state.inventory[standardized_name] += quantity
            st.success(f"Zwiększono ilość **{standardized_name}** o **{quantity}**. Nowa ilość: **{st.session_state.inventory[standardized_name]}**.")
        else:
            st.session_state.inventory[standardized_name] = quantity
            st.success(f"Dodano nowy towar: **{standardized_name}** w ilości **{quantity}**.")
    elif quantity <= 0:
        st.error("Ilość do dodania musi być większa od zera.")
    else:
        st.error("Wprowadź nazwę towaru.")

def remove_item(item_name):
    """Usuwa cały towar (klucz) z magazynu."""
    standardized_name = item_name.strip().upper()
    if standardized_name in st.session_state.inventory:
        current_quantity = st.session_state.inventory.pop(standardized_name)
        st.info(f"Usunięto cały towar: **{standardized_name}** (Ilość przed usunięciem: {current_quantity}).")
    else:
        st.warning(f"Towar **{standardized_name}** nie znaleziony w magazynie.")

# --- Interfejs Streamlit ---

st.title("📦 Prosty Magazyn z Ilościami")
st.markdown("Aplikacja do zarządzania inwentarzem wykorzystująca słownik w pamięci (`st.session_state`).")

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Towar")

with st.form("add_form", clear_on_submit=True):
    
    # Podział na kolumny dla nazwy i ilości
    col1, col2 = st.columns([3, 1])
    
    with col1:
        new_item = st.text_input("Nazwa nowego towaru:", key="new_item_input")
    with col2:
        # Zgodnie z prośbą, pole do wpisania ilości
        new_quantity = st.number_input("Ilość do dodania:", min_value=1, value=1, step=1, key="new_quantity_input")

    submit_add = st.form_submit_button("Dodaj do Magazynu")

    if submit_add:
        # Wywołanie funkcji z nazwą i ilością
        add_item(new_item, new_quantity)

# --- Sekcja Usuwania Towaru ---
st.header("➖ Usuń Towar (Cała Pozycja)")

# Tworzymy listę towarów do wyboru
available_items = list(st.session_state.inventory.keys())

items_to_remove = st.selectbox(
    "Wybierz towar do całkowitego usunięcia:",
    options=["--- Wybierz ---"] + sorted(available_items),
    key="remove_item_select"
)

# Button do usunięcia
if st.button("Usuń Wybrany Towar z Magazynu", disabled=(items_to_remove == "--- Wybierz ---")):
    if items_to_remove != "--- Wybierz ---":
        remove_item(items_to_remove)

# --- Sekcja Aktualnego Magazynu ---
st.header("📚 Aktualny Magazyn")

if st.session_state.inventory:
    
    # Tworzenie Dataframe (tabeli) z danych słownika
    inventory_data = {
        "Nazwa Towaru": list(st.session_state.inventory.keys()),
        "Ilość": list(st.session_state.inventory.values())
    }
    df = pd.DataFrame(inventory_data)
    # Sortowanie alfabetyczne dla lepszej czytelności
    df = df.sort_values(by="Nazwa Towaru").reset_index(drop=True)

    # Wyświetlenie tabeli
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Obliczenia metryk
    total_items_count = sum(st.session_state.inventory.values())
    
    st.metric(label="Łączna Liczba Sztuk w Magazynie", value=total_items_count)
    st.caption(f"Liczba różnych pozycji towarowych: {len(st.session_state.inventory)}")
else:
    st.info("Magazyn jest pusty.")

# --- Informacja o braku zapisu ---
st.caption("⚠️ Uwaga: Dane są przechowywane tylko w pamięci serwera Streamlit (st.session_state) i zostaną utracone po jego zresetowaniu.")
