import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Map, { Source, Layer, NavigationControl } from 'react-map-gl/mapbox';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import 'mapbox-gl/dist/mapbox-gl.css';
import api from '../api';

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;

// Default layer styles for GeoJSON
const polygonLayer = {
  id: 'site-polygons',
  type: 'fill',
  paint: {
    'fill-color': '#088',
    'fill-opacity': 0.4
  }
};
const polygonLine = {
  id: 'site-polygons-line',
  type: 'line',
  paint: {
    'line-color': '#000',
    'line-width': 2
  }
};

export default function Dashboard() {
  const { projectId } = useParams();
  
  const [sites, setSites] = useState([]);
  const [selectedSite, setSelectedSite] = useState(null);
  const [metrics, setMetrics] = useState([]);
  
  // Highcharts config
  const chartOptions = {
    title: { text: selectedSite ? `Analytics for ${selectedSite.name}` : 'Select a site...' },
    xAxis: { type: 'datetime' },
    yAxis: { title: { text: 'Measurement' } },
    series: [
      {
        name: 'Carbon Tons',
        data: metrics.filter(m => m.metric_type === 'carbon_tons').map(m => [new Date(m.timestamp).getTime(), m.value]),
      },
      {
        name: 'Biodiversity Index',
        data: metrics.filter(m => m.metric_type === 'biodiversity_index').map(m => [new Date(m.timestamp).getTime(), m.value]),
      }
    ]
  };

  useEffect(() => {
    // Fetch sites for this project
    const fetchSites = async () => {
      try {
        const response = await api.get(`/projects/${projectId}/sites`);
        setSites(response.data);
      } catch (err) {
        console.error("Error fetching sites:", err);
      }
    };
    if (projectId) fetchSites();
  }, [projectId]);

  const fetchMetricsForSite = async (site) => {
    setSelectedSite(site);
    try {
      const resp = await api.get(`/sites/${site.id}/analytics`);
      setMetrics(resp.data);
    } catch (err) {
      console.error("Error fetching metrics:", err);
    }
  };

  const geojson = {
    type: 'FeatureCollection',
    features: sites.map(site => ({
      type: 'Feature',
      geometry: site.geometry,
      properties: { ...site, geometry: undefined } // store site details in properties
    }))
  };

  const handleMapClick = (e) => {
    if (e.features && e.features.length > 0) {
      const clickedFeature = e.features[0];
      if (clickedFeature.properties && clickedFeature.properties.id) {
        fetchMetricsForSite(clickedFeature.properties);
      }
    }
  };

  return (
    <div className="container-fluid mt-4">
      <div className="row">
        <div className="col-md-7">
          <div className="card shadow-sm mb-3">
            <div className="card-header bg-primary text-white d-flex justify-content-between">
              <h5 className="mb-0">Project Web Map</h5>
              <button className="btn btn-sm btn-light">Add Site</button>
            </div>
            <div className="card-body p-0" style={{ height: '500px' }}>
              <Map
                initialViewState={{
                  longitude: -122.4,
                  latitude: 37.8,
                  zoom: 9
                }}
                mapStyle="mapbox://styles/mapbox/streets-v11"
                mapboxAccessToken={MAPBOX_TOKEN}
                interactiveLayerIds={['site-polygons']}
                onClick={handleMapClick}
              >
                <NavigationControl position="top-left" />
                <Source id="sites-data" type="geojson" data={geojson}>
                  <Layer {...polygonLayer} />
                  <Layer {...polygonLine} />
                </Source>
              </Map>
            </div>
          </div>
        </div>
        <div className="col-md-5">
           <div className="card shadow-sm h-100">
             <div className="card-header bg-secondary text-white">
               <h5 className="mb-0">Site Analytics</h5>
             </div>
             <div className="card-body">
               {selectedSite ? (
                 <HighchartsReact highcharts={Highcharts} options={chartOptions} />
               ) : (
                 <div className="d-flex align-items-center justify-content-center h-100 text-muted">
                    <p>Click on a polygon to view Analytics</p>
                 </div>
               )}
             </div>
           </div>
        </div>
      </div>
    </div>
  );
}
