import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo


# 💡 Class is used here – this is an example of **Encapsulation**
class TimeZoneApp:
    def __init__(self):
        # 💡 Data (time_zones) is encapsulated inside the class
        self.time_zones = [
            "UTC",
            "Asia/Karachi",
            "Europe/London",
            "Australia/Sydney",
            "Asia/Tokyo",
            "Europe/Berlin"
        ]

    def show_title(self):
        st.title("Time Zone App")

    def show_selected_timezones(self):
        st.subheader("Selected Timezones")
        selected = st.multiselect("Select TimeZones", self.time_zones, default=["UTC", "Asia/Karachi"])
        for tz in selected:
            current_time = datetime.now(ZoneInfo(tz)).strftime("%Y-%m-%d %I %H:%M:%S %p")
            st.write(f"**{tz}**: {current_time}")

    def convert_time_between_timezones(self):
        st.subheader("Convert Time Between Timezones")

        current_time = st.time_input("Current Time", value=datetime.now().time())
        from_tz = st.selectbox("From Timezone", self.time_zones, index=0)
        to_tz = st.selectbox("To Timezone", self.time_zones, index=1)

        if st.button("Current Time"):
            dt = datetime.combine(datetime.today(), current_time, tzinfo=ZoneInfo(from_tz))
            converted = dt.astimezone(ZoneInfo(to_tz)).strftime("%Y-%m-%d %I %H:%M:%S %p")
            st.success(f"Converted Time {to_tz}: {converted}")

    # 💡 All functions are grouped in a single class – showing **Encapsulation**
    def run(self):
        self.show_title()
        self.show_selected_timezones()
        self.convert_time_between_timezones()


# 💡 Object of the class is created – this is an example of **Abstraction**
if __name__ == "__main__":
    app = TimeZoneApp()  # 👆 Abstraction hides the complex code inside the class
    app.run()
