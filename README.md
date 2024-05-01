## Overview
This project aims to collect district boundary files for various political and administrative districts within Los Angeles County. The collected data will be processed into shapefiles and contributed to Hack for LA.

## Districts Covered
- Assembly
- Senate
- Neighborhood
- Supervisors
- Congressional
- City Clerk

## Data Collection Process
The data collection process is facilitated using the [GeoHub LA County Website](https://geohub.lacity.org/search?collection=Dataset) and district API. This API provides access to geospatial datasets related to Los Angeles County.

### Steps:
1. **Authentication**: No Key Necessary.
2. **Requesting Data**: Use the appropriate API endpoints to request boundary files for each of the listed districts.
3. **Data Processing**: Once the boundary files are obtained, they are processed into shapefiles.
4. **Data Storage**: Shape files to be stored in Hack for L.A. GitHub or [Google Drive](https://drive.google.com/drive/folders/1KsIfAFmp0ArLauvHY1k9wRc9ZXaPDahe).
5. **Automation**: Use GitHub Actions workflow to automate the retrieval and processing of shape files every other month.