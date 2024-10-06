import pandas as pd
import folium
from flask import Flask, render_template

app = Flask(__name__)

# Add a route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # This will render the home page

@app.route('/map')
def show_map():
    # Load the Excel file
    excel_path = r"C:\Users\Devesh\Desktop\dm\is2.xlsx"  # Ensure this path is correct
    df = pd.read_excel(excel_path)  # Read the Excel file

    # Create a base map centered on the average latitude and longitude
    m = folium.Map(location=[df.iloc[:, 5].mean(), df.iloc[:, 6].mean()], zoom_start=7)

    # Loop through the DataFrame to add markers
    for index, row in df.iterrows():
        lat = row.iloc[5]  # Latitude from column F
        lon = row.iloc[6]  # Longitude from column G
        deaths_info = (
            f"Deaths A: {row['deaths_a']}<br>"
            f"Deaths B: {row['deaths_b']}<br>"
            f"Deaths (Civilians): {row['deaths_civilians']}<br>"
            f"Deaths (Unknown): {row['deaths_unknown']}"
        )
        
        # Add a marker for each location
        folium.Marker(
            location=[lat, lon],
            popup=deaths_info,
            icon=folium.Icon(color='red')  # Customize the color if needed
        ).add_to(m)

    # Save the map to an HTML file in the templates directory
    map_file_path = "templates/death_map.html"  # Ensure this is in the templates directory
    m.save(map_file_path)

    return render_template('death_map.html')

if __name__ == '__main__':
    app.run(debug=True)
