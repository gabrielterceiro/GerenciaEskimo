# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily
from IPython.display import display

# Set time period
start = datetime(2017, 1, 1)
end = datetime(2023, 2, 16)

# Create Point for Santos, SP
location = Point(-23.9694, -46.3353)
#location.radius=90000

# Get daily data for 2018
data = Daily(location, start, end)
data = data.fetch()

# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg', 'tmax', 'tmin'])
plt.show()


'''# Import Meteostat library
from meteostat import S///////////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAtations

# Get nearby weather stations
stations = Stations()
stations = stations.nearby(-23.9694, -46.3353)
station = stations.fetch(10)

# Print DataFrame
display(station.to_string())'''