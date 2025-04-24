import string
import streamlit as st
import random

# ✅ Encapsulation: Password generation logic inside a class
class PasswordGenerator:
    def __init__(self, length, use_digits, use_special):
        self.length = length
        self.use_digits = use_digits
        self.use_special = use_special

    def generate(self):
        characters = string.ascii_letters

        if self.use_digits:
            characters += string.digits

        if self.use_special:
            characters += string.punctuation

        return ''.join(random.choice(characters) for _ in range(self.length))


# ✅ Abstraction: Main app class hides internal logic from UI
class PasswordApp:
    def __init__(self):
        st.title('Password Generator')

    def run(self):
        length = st.slider('Length of password:', min_value=6, max_value=24, value=12)
        use_digits = st.checkbox('Use digits')
        use_special = st.checkbox('Use special characters')

        if st.button('Generate a Password'):
            generator = PasswordGenerator(length, use_digits, use_special)
            password = generator.generate()

            st.write(f"Generated Password: {password}")
            st.write("----------------------------------------------------------------")
            st.info("Build By Subhan Kaladi🩷")


# ✅ Reusability: This class can be reused in other apps or APIs
if __name__ == "__main__":
    app = PasswordApp()
    app.run()
