## Airline

#### UniqueCarrier
Unique Carrier Code. When the same code has been used by multiple carriers, a numeric suffix is used for earlier users, for example, PA, PA(1), PA(2). Use this field for analysis across a range of years.
  ##### L_UNIQUE_CARRIERS
    Code    Description
    02Q     Titan Airways
    04Q     Tradewind Aviation
    05Q     Comlux Aviation, AG


#### AirlineID
An identification number assigned by US DOT to identify a unique airline (carrier). A unique airline (carrier) is defined as one holding and reporting under the same DOT certificate regardless of its Code, Name, or holding company/corporation.
  ##### L_AIRLINE_ID
    Code    Description
    19031   Mackey International Inc.: MAC
    19032	Munz Northern Airlines Inc.: XY
    19033	Cochise Airlines Inc.: COC
    19034	Golden Gate Airlines Inc.: GSA
    19035	Aeromech Inc.: RZZ


**Carrier**: For analysis, use the Unique Carrier Code.

**TailNum**: Tail Number

**FlightNum**: Flight Number

## Origin
#### OriginAirportID
Origin Airport, Airport ID. An identification number assigned by US DOT to identify a unique airport. **Use this field for airport analysis across a range of years because an airport can change its airport code and airport codes can be reused.**
###### L_AIRPORT_ID
    Code	Description
    10001	Afognak Lake, AK: Afognak Lake Airport
    10003	Granite Mountain, AK: Bear Creek Mining Strip


#### OriginCityMarketID
Origin Airport, City Market ID. City Market ID is an identification number assigned by US DOT to identify a city market. Use this field to consolidate airports serving the same city market.


 #### OriginWac
 Origin Airport, World Area Code
 #####L_WORLD_AREA_CODES
    Origin Airport, World Area Code
    Code	Description
    21	    New Jersey
    22	    New York
    312	    Bolivia
    316	    Brazil

## Departure Performance
 * **CRSDepTime**	CRS Departure Time (local time: hhmm)
    * _will need to parse HHMM's, add to date_
    * _note is local time - may need to get get timezones?_
 * **DepTime**	Actual Departure Time (local time: hhmm)
 * **DepDelay**	Difference in minutes between scheduled and actual departure time. Early departures show negative numbers.
 * **DepDelayMinutes**	Difference in minutes between scheduled and actual departure time. Early departures set to 0.
 	* will remove
 * **DepDel15**	Departure Delay Indicator, 15 Minutes or More (1=Yes)
  	* will remove
 * **DepartureDelayGroups**	Departure Delay intervals, every (15 minutes from <-15 to >180)
  	* will remove - prefer to make own bins
 * **DepTimeBlk**	CRS Departure Time Block, Hourly Intervals
  	* will remove - prefer to make own bins
 * **TaxiOut**	Taxi Out Time, in Minutes
 * **WheelsOff**	Wheels Off Time (local time: hhmm)
    * Deptime + TaxiOut = WheelsOff

## Arrival performance
* **WheelsOn**	Wheels On Time (local time: hhmm)
* **TaxiIn**	Taxi In Time, in Minutes
* **CRSArrTime**	CRS Arrival Time (local time: hhmm)
    * _Computerized Reservations Systems arrival time_
* **ArrTime**	Actual Arrival Time (local time: hhmm)
* **ArrDelay**	Difference in minutes between scheduled and actual arrival time. Early arrivals show negative numbers.
* **ArrDelayMinutes**	Difference in minutes between scheduled and actual arrival time. Early arrivals set to 0.
    * will remove - redundant
* **ArrDel15**	Arrival Delay Indicator, 15 Minutes or More (1=Yes)
    * will remove - prefer to make own bins
* **ArrivalDelayGroups**	Arrival Delay intervals, every (15-minutes from <-15 to >180)
    * will remove - prefer to make own bins
* **ArrTimeBlk**	CRS Arrival Time Block, Hourly Intervals		

## Cancellations and Diversions
* Cancelled	Cancelled Flight Indicator (1=Yes)
* CancellationCode	Specifies The Reason For Cancellation
    ##### CANCELLATION.CSV
        Code	Description
        A	Carrier
        B	Weather
        C	National Air System
        D	Security
* Diverted	Diverted Flight Indicator (1=Yes)

##Flight Summaries
* CRSElapsedTime	CRS Elapsed Time of Flight, in Minutes
* ActualElapsedTime	Elapsed Time of Flight, in Minutes
* AirTime	Flight Time, in Minutes
* Flights	Number of Flights
* Distance	Distance between airports (miles)
* DistanceGroup	Distance Intervals, every 250 Miles, for Flight Segment

##Cause of Delay (**Data starts 6/2003**)
* CarrierDelay	Carrier Delay, in Minutes
    * Air Carrier: The cause of the cancellation or delay was due to circumstances within the airline's control (e.g. maintenance or crew problems, aircraft cleaning, baggage loading, fueling, etc.).
* WeatherDelay	Weather Delay, in Minutes
    * Extreme Weather: Significant meteorological conditions (actual or forecasted) that, in the judgment of the carrier, delays or prevents the operation of a flight such as tornado, blizzard or hurricane.
* NASDelay	National Air System Delay, in Minutes
    * National Aviation System (NAS): Delays and cancellations attributable to the national aviation system that refer to a broad set of conditions, such as non-extreme weather conditions, airport operations, heavy traffic volume, and air traffic control.
* SecurityDelay	Security Delay, in Minutes
    * Security: Delays or cancellations caused by evacuation of a terminal or concourse, re-boarding of aircraft because of security breach, inoperative screening equipment and/or long lines in excess of 29 minutes at screening areas.
* LateAircraftDelay	Late Aircraft Delay, in Minutes
    * Late-arriving aircraft: A previous flight with same aircraft arrived late, causing the present flight to depart late.


##Gate Return Information at Origin Airport (Data starts 10/2008)
* FirstDepTime	First Gate Departure Time at Origin Airport
* TotalAddGTime	Total Ground Time Away from Gate for Gate Return or Cancelled Flight
* LongestAddGTime	Longest Time Away from Gate for Gate Return or Cancelled Flight

##Diverted Airport Information (Data starts 10/2008)
* DivAirportLandings	Number of Diverted Airport Landings
* DivReachedDest	Diverted Flight Reaching Scheduled Destination Indicator (1=Yes)
* DivActualElapsedTime	Elapsed Time of Diverted Flight Reaching
Scheduled Destination, in Minutes. The ActualElapsedTime column remains NULL for all diverted flights.
* DivArrDelay	Difference in minutes between scheduled and actual arrival time for a diverted flight reaching scheduled destination. The ArrDelay column remains NULL for all diverted flights.
* DivDistance	Distance between scheduled destination and final diverted airport (miles). Value will be 0 for diverted flight reaching scheduled destination.
* Div1Airport	Diverted Airport Code1
* Div1AirportID	Airport ID of Diverted Airport 1. Airport ID is a Unique Key for an Airport
* Div1AirportSeqID	Airport Sequence ID of Diverted Airport 1. Unique Key for Time Specific Information for an Airport
* Div1WheelsOn	Wheels On Time (local time: hhmm) at Diverted Airport Code1
* Div1TotalGTime	Total Ground Time Away from Gate at Diverted Airport Code1
* Div1LongestGTime	Longest Ground Time Away from Gate at Diverted Airport Code1
* Div1WheelsOff	Wheels Off Time (local time: hhmm) at Diverted Airport Code1
* Div1TailNum	Aircraft Tail Number for Diverted Airport Code1
* Div2Airport	Diverted Airport Code2
* Div2AirportID	Airport ID of Diverted Airport 2. Airport ID is a Unique Key for an Airport
* Div2AirportSeqID	Airport Sequence ID of Diverted Airport 2. Unique Key for Time Specific Information for an Airport
* Div2WheelsOn	Wheels On Time (local time: hhmm) at Diverted Airport Code2
* Div2TotalGTime	Total Ground Time Away from Gate at Diverted Airport Code2
* Div2LongestGTime	Longest Ground Time Away from Gate at Diverted Airport Code2
* Div2WheelsOff	Wheels Off Time (local time: hhmm) at Diverted Airport Code2
* Div2TailNum	Aircraft Tail Number for Diverted Airport Code2
* Div3Airport	Diverted Airport Code3
* Div3AirportID	Airport ID of Diverted Airport 3. Airport ID is a Unique Key for an Airport
* Div3AirportSeqID	Airport Sequence ID of Diverted Airport 3. Unique Key for Time Specific Information for an Airport
* Div3WheelsOn	Wheels On Time (local time: hhmm) at Diverted Airport Code3
* Div3TotalGTime	Total Ground Time Away from Gate at Diverted Airport Code3
* Div3LongestGTime	Longest Ground Time Away from Gate at Diverted Airport Code3
* Div3WheelsOff	Wheels Off Time (local time: hhmm) at Diverted Airport Code3
* Div3TailNum	Aircraft Tail Number for Diverted Airport Code3
* Div4Airport	Diverted Airport Code4
* Div4AirportID	Airport ID of Diverted Airport 4. Airport ID is a Unique Key for an Airport
* Div4AirportSeqID	Airport Sequence ID of Diverted Airport 4. Unique Key for Time Specific Information for an Airport
* Div4WheelsOn	Wheels On Time (local time: hhmm) at Diverted Airport Code4
* Div4TotalGTime	Total Ground Time Away from Gate at Diverted Airport Code4
* Div4LongestGTime	Longest Ground Time Away from Gate at Diverted Airport Code4
* Div4WheelsOff	Wheels Off Time (local time: hhmm) at Diverted Airport Code4
* Div4TailNum	Aircraft Tail Number for Diverted Airport Code4
* Div5Airport	Diverted Airport Code5
* Div5AirportID	Airport ID of Diverted Airport 5. Airport ID is a Unique Key for an Airport
* Div5AirportSeqID	Airport Sequence ID of Diverted Airport 5. Unique Key for Time Specific Information for an Airport
* Div5WheelsOn	Wheels On Time (local time: hhmm) at Diverted Airport Code5
* Div5TotalGTime	Total Ground Time Away from Gate at Diverted Airport Code5
* Div5LongestGTime	Longest Ground Time Away from Gate at Diverted Airport Code5
* Div5WheelsOff	Wheels Off Time (local time: hhmm) at Diverted Airport Code5
* Div5TailNum	Aircraft Tail Number for Diverted Airport Code5





### aviation support tables
##### http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=288&DB_Short_Name=Aviation%20Support%20Tables
SYS_FIELD_NAME	 FIELD_DESC
AIRPORT_SEQ_ID	An identification number assigned by US DOT to identify a unique airport at a given point of time.  Airport attributes, such as airport name or coordinates, may change over time.
AIRPORT_ID	An identification number assigned by US DOT to identify a unique airport.  Use this field for airport analysis across a range of years because an airport can change its airport code and airport codes can be reused.
AIRPORT	A three character alpha-numeric code issued by the U.S. Department of Transportation which is the official designation of the airport.  The airport code is not always unique to a specific airport because airport codes can change or can be reused.
DISPLAY_AIRPORT_NAME	Airport Name
DISPLAY_AIRPORT_CITY_NAME_FULL	Airport City Name with either U.S. State or Country
AIRPORT_WAC_SEQ_ID2	Unique Identifier for a World Area Code (WAC) at a given point of time for the Physical Location of the Airport.  See World Area Codes support table.
AIRPORT_WAC	World Area Code for the Physical Location of the Airport
AIRPORT_COUNTRY_NAME	Country Name for the Physical Location of the Airport
AIRPORT_COUNTRY_CODE_ISO	Two-character ISO Country Code for the Physical Location of the Airport
AIRPORT_STATE_NAME	State Name for the Physical Location of the Airport
AIRPORT_STATE_CODE	State Abbreviation for the Physical Location of the Airport
AIRPORT_STATE_FIPS	FIPS (Federal Information Processing Standard) State Code for the Physical Location of the Airport
CITY_MARKET_SEQ_ID	An identification number assigned by US DOT to identify a city market at a given point of time.  City Market attributes may change over time.  For example the country associated with the city market can change over time due to geopolitical changes.
CITY_MARKET_ID	An identification number assigned by US DOT to identify a city market.  Use this field to consolidate airports serving the same city market.
DISPLAY_CITY_MARKET_NAME_FULL	City Market Name with either U.S. State or Country
CITY_MARKET_WAC_SEQ_ID2	Unique Identifier for a World Area Code (WAC) at a given point of time for the City Market.  See World Area Codes support table.
CITY_MARKET_WAC	World Area Code for the City Market
LAT_DEGREES	Latitude, Degrees
LAT_HEMISPHERE	Latitude, Hemisphere
LAT_MINUTES	Latitude, Minutes
LAT_SECONDS	Latitude, Seconds
LATITUDE	Latitude
LON_DEGREES	Longitude, Degrees
LON_HEMISPHERE	Longitude, Hemisphere
LON_MINUTES	Longitude, Minutes
LON_SECONDS	Longitude, Seconds
LONGITUDE	Longitude
UTC_LOCAL_TIME_VARIATION	Time Zone at the Airport
AIRPORT_START_DATE	Start Date of Airport Attributes
AIRPORT_THRU_DATE	End Date of Airport Attributes (Active = NULL)
AIRPORT_IS_CLOSED	Indicates if the airport is closed (1 = Yes).  If yes, the airport is closed is on the AirportEndDate.
AIRPORT_IS_LATEST	Indicates if this row contains the latest attributes for the Airport (1 = Yes)