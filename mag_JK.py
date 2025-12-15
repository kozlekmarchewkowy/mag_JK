import streamlit as st

# --- Inicjalizacja Magazynu (Lista Towarów) ---

# Używamy st.session_state do przechowywania listy towarów.
# Jest to kluczowe, aby lista nie resetowała się po każdym odświeżeniu
# lub interakcji użytkownika w Streamlit.
if 'inventory' not in st.session_state:
    st.session_state.inventory = ["Laptop", "Monitor", "Klawiatura"] # Przykładowe początkowe towary

# --- Funkcje Magazynu ---

def add_item(item_name):
    """Dodaje towar do magazynu (listy) po konwersji na wielkie litery."""
    if item_name:
        # Konwersja na wielkie litery i usunięcie białych znaków
        standardized_name = item_name.strip().upper()
        if standardized_name not in st.session_state.inventory:
            st.session_state.inventory.append(standardized_name)
            st.success(f"Dodano: **{standardized_name}**")
        else:
            st.warning(f"Towar **{standardized_name}** jest już w magazynie.")
    else:
        st.error("Wprowadź nazwę towaru do dodania.")

def remove_item(item_name):
    """Usuwa towar z magazynu (listy) po konwersji na wielkie litery."""
    standardized_name = item_name.strip().upper()
    if standardized_name in st.session_state.inventory:
        st.session_state.inventory.remove(standardized_name)
        st.info(f"Usunięto: **{standardized_name}**")
    else:
        st.warning(f"Towar **{standardized_name}** nie znaleziony w magazynie.")

# --- Interfejs Streamlit ---

st.set_page_config(page_title="Prosty Magazyn (Streamlit + Lista)", layout="wide")

st.title("📦 Prosty Magazyn")
st.markdown("Aplikacja do zarządzania inwentarzem wykorzystująca listę w pamięci (`st.session_state`).")

# --- Sekcja Dodawania Towaru ---
st.header("➕ Dodaj Towar")

with st.form("add_form", clear_on_submit=True):
    new_item = st.text_input("Nazwa nowego towaru:", key="new_item_input")
    submit_add = st.form_submit_button("Dodaj do Magazynu")

    if submit_add:
        add_item(new_item)

# --- Sekcja Usuwania Towaru ---
st.header("➖ Usuń Towar")

# Możemy użyć selectbox dla towarów, które są faktycznie w magazynie
items_to_remove = st.selectbox(
    "Wybierz towar do usunięcia:",
    options=["--- Wybierz ---"] + sorted(st.session_state.inventory),
    key="remove_item_select"
)

# Button do usunięcia
if st.button("Usuń Wybrany Towar", disabled=(items_to_remove == "--- Wybierz ---")):
    # Sprawdzamy, czy wybrano faktyczny towar
    if items_to_remove != "--- Wybierz ---":
        remove_item(items_to_remove)

# --- Sekcja Aktualnego Magazynu ---
st.header("📚 Aktualny Magazyn")

if st.session_state.inventory:
    # Wyświetlenie listy towarów
    st.dataframe(
        {"Nazwa Towaru": sorted(st.session_state.inventory)},
        use_container_width=True,
        hide_index=True
    )
    st.metric(label="Łączna Liczba Towarów", value=len(st.session_state.inventory))
else:
    st.info("Magazyn jest pusty.")

# --- Informacja o braku zapisu ---
st.caption("⚠️ Uwaga: Dane są przechowywane tylko w pamięci serwera Streamlit i zostaną utracone po ponownym uruchomieniu aplikacji.")
