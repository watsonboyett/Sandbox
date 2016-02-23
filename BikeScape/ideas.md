

## General Goals

1. Bike every road in New Orleans.
2. Collect some data while riding.
	- Location
	- Road Quality
	- Traffic Quality (Speed/Volume)
	- Neighborhood Quality
	- Speed
	- (Images?)
	- (Sound/Loudness?)
3. Proudly look at the data later, but never do anything with it.
4. Okay, maybe do SOMETHING with it... Not sure what though.


## Design Ideas

### Automated Data Collection (from sensors)
- Location: GPS position (1 sec intervals?)
- Bike Speed: X,Y velocity from accelerometer
- Road Roughness: Z acceleration from accelerometer
- Images: Front/Rear cameras

#### Notes
- Could calculate velocity from time difference between GPS data points
- Accelerometer data is probably going to very noisy due to riding technique (e.g. "pumping the handlebars")
- When are images captured? (Periodically? By a trigger? Both?)
- What captures the images? (Phone? GoPro?) And where is it mounted?


### Manual Data Collection (from users)
- Road Quality: button/slider
- Traffic Quality: button/slider
- Neighborhood Quality: button/slider

#### Notes
- Buttons could be large swipe boxes 
	- three states: neutral (default), good, and bad
	- swipe left to set as good, swipe right to set as bad (or vice-versa)
- How long the input valid? 
	- until it's changed? 
	- until a sensors detect a turn or a rough road?
	- until a time limit is reached?
	- all of the above?


### User Features
- History Map
	- Show map of roads that have already been travelled
	- Possibly show different colors based on how long ago the roads were travelled (or time of day?)
- Adventure Mode
	- Allow users to enter destination
	- Provide a route that minimizes the raods they're already travelled
	- Allow users to set max travel time/distance constraints

#### Notes
- Mapping Tools
	- OsmSharp - Open source C# library for rendering maps (based on OpenStreetMap)
	- MapBox - PaaS for rendering maps (uses OSM data)


### Output Data
- Roads Travelled
- Raw Data: 
	- Speed Heatmap
	- Road/Traffic/Neighborhood Quality Heatmaps
- Processed Data: 
	- Speed Deviation Heatmap (i.e. how much faster/slower raods are than average speed)
	- Bikability Heatmap (combine road/traffic quality metrics)


## Version Roadmap

### Version One
- Log location from GPS
- Log speed from accelerometer
- Log road roughness from accelerometer
- Show swipe buttons for road/traffic/neighborhood quality (no auto-reset features)
- All data saved locally (on the phone, nothing online) as CSV file and exported somehow?
- Really crude interface

### Version Two
- Implement database for data logging (still offline)
- Show map of roads that have been travelled
- Slightly better interface

### Version Three
- Online database, supports multiple users
- Adventure Mode engaged!
- Real. Nice. Interface.
