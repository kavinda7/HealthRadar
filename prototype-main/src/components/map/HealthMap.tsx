import { useEffect, useRef, useState, useCallback } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { MapLegend } from "./MapLegend";
import { toast } from "sonner";

// Set the Mapbox token directly
const MAPBOX_TOKEN = "pk.eyJ1Ijoia2F2aW5kYTciLCJhIjoiY21hbGdpNW93MDlsMzJqc2YycWZ6OHJkcyJ9.tm_RLXFjx0D9jFhzNGcUWQ";

interface Location {
  name: string;
  coordinates: [number, number];
  zoom: number;
}

interface HealthMapProps {
  diseaseType: string;
  location: string;
}

export function HealthMap({ diseaseType, location }: HealthMapProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);

  const locations: Record<string, Location> = {
    "Oulu": { 
      name: "Oulu", 
      coordinates: [25.4701, 65.0124], 
      zoom: 11
    },
    "Helsinki": { 
      name: "Helsinki", 
      coordinates: [24.9384, 60.1699], 
      zoom: 11
    },
    "Tampere": { 
      name: "Tampere", 
      coordinates: [23.7610, 61.4978], 
      zoom: 11
    },
    "Turku": { 
      name: "Turku", 
      coordinates: [22.2688, 60.4518], 
      zoom: 11
    },
    "Jyväskylä": { 
      name: "Jyväskylä", 
      coordinates: [25.7472, 62.2426], 
      zoom: 11
    },
  };

  const generateRandomPoints = useCallback((center: [number, number], count: number, radius: number) => {
    const points = [];
    
    for (let i = 0; i < count; i++) {
      // Random angle
      const angle = Math.random() * 2 * Math.PI;
      // Random radius (with square root for uniform distribution)
      const r = radius * Math.sqrt(Math.random());
      
      // Convert to Cartesian coordinates
      const x = center[0] + r * Math.cos(angle);
      const y = center[1] + r * Math.sin(angle);
      
      // Random intensity based on disease
      let intensity;
      switch (diseaseType) {
        case "Influenza":
          // Higher intensities during winter/pollution
          intensity = Math.floor(Math.random() * 8) + 3; 
          break;
        case "Norovirus":
          // Medium to high intensity in moist areas
          intensity = Math.floor(Math.random() * 6) + 4;
          break;
        case "COVID-19":
          // Higher in dense areas
          intensity = Math.floor(Math.random() * 7) + 3;
          break;
        case "Heatstroke":
          // Very high in urban centers during heat
          intensity = Math.floor(Math.random() * 5) + 5;
          break;
        default:
          intensity = Math.floor(Math.random() * 10) + 1;
      }

      points.push({
        type: "Feature",
        properties: { intensity },
        geometry: {
          type: "Point",
          coordinates: [x, y]
        }
      });
    }

    return {
      type: "FeatureCollection" as const,
      features: points
    };
  }, [diseaseType]);

  const generateSymptomReports = useCallback((center: [number, number], count: number, radius: number) => {
    const reports = [];
    const symptoms: Record<string, string[]> = {
      "Influenza": ["Fever", "Cough", "Sore Throat", "Nasal Congestion"],
      "Norovirus": ["Nausea", "Vomiting", "Diarrhea", "Headache"],
      "COVID-19": ["Fever", "Cough", "Nasal Congestion", "Fatigue"],
      "Heatstroke": ["Headache", "Nausea", "Dizziness", "Confusion"]
    };
    
    const currentSymptoms = symptoms[diseaseType] || symptoms["Influenza"];
    
    for (let i = 0; i < count; i++) {
      // Random angle
      const angle = Math.random() * 2 * Math.PI;
      // Random radius (with square root for uniform distribution)
      const r = radius * Math.sqrt(Math.random()) * 0.7; // Keep reports closer to center
      
      // Convert to Cartesian coordinates
      const x = center[0] + r * Math.cos(angle);
      const y = center[1] + r * Math.sin(angle);
      
      // Random symptom and severity
      const symptom = currentSymptoms[Math.floor(Math.random() * currentSymptoms.length)];
      const severityLevel = ["Low", "Medium", "High"][Math.floor(Math.random() * 3)];
      let color;
      
      switch (severityLevel) {
        case "Low":
          color = "#4ade80"; // green
          break;
        case "Medium":
          color = "#facc15"; // yellow
          break;
        case "High":
          color = "#ef4444"; // red
          break;
        default:
          color = "#4ade80";
      }

      reports.push({
        type: "Feature",
        properties: { 
          symptom,
          severity: severityLevel,
          color
        },
        geometry: {
          type: "Point",
          coordinates: [x, y]
        }
      });
    }

    return {
      type: "FeatureCollection" as const,
      features: reports
    };
  }, [diseaseType]);

  useEffect(() => {
    if (!mapContainerRef.current) return;
    
    mapboxgl.accessToken = MAPBOX_TOKEN;

    if (!map.current) {
      try {
        map.current = new mapboxgl.Map({
          container: mapContainerRef.current,
          style: "mapbox://styles/mapbox/light-v11",
          center: locations[location]?.coordinates || locations["Oulu"].coordinates,
          zoom: locations[location]?.zoom || 11,
        });
        
        map.current.addControl(new mapboxgl.NavigationControl(), "top-right");
        
        map.current.on("load", () => {
          updateMapData();
        });
      } catch (error) {
        console.error("Error initializing map:", error);
        toast.error("Failed to initialize map. Please check your Mapbox token.");
      }
    } else {
      // If map exists, just update location
      map.current.flyTo({
        center: locations[location]?.coordinates || locations["Oulu"].coordinates,
        zoom: locations[location]?.zoom || 11,
        essential: true,
        duration: 1000
      });
      
      // After animation, update the data
      setTimeout(() => {
        updateMapData();
      }, 1000);
    }

    return () => {
      // This will run when the component unmounts
    };
  }, [location, diseaseType]);

  const updateMapData = () => {
    if (!map.current || !map.current.loaded()) return;
    
    const currentLocation = locations[location] || locations["Oulu"];
    const heatmapData = generateRandomPoints(currentLocation.coordinates, 100, 0.05);
    const reportsData = generateSymptomReports(currentLocation.coordinates, 15, 0.05);
    
    // Add or update heatmap source and layer
    if (map.current.getSource('heatmap-data')) {
      // @ts-ignore
      map.current.getSource('heatmap-data').setData(heatmapData);
    } else {
      map.current.addSource('heatmap-data', {
        type: 'geojson',
        data: heatmapData
      });
      
      map.current.addLayer({
        id: 'heatmap-layer',
        type: 'heatmap',
        source: 'heatmap-data',
        paint: {
          'heatmap-weight': [
            'interpolate', ['linear'], ['get', 'intensity'],
            0, 0,
            10, 1
          ],
          'heatmap-intensity': 1,
          'heatmap-color': [
            'interpolate', ['linear'], ['heatmap-density'],
            0, 'rgba(0, 0, 255, 0)',
            0.2, 'rgb(94, 232, 129)',  // green
            0.5, 'rgb(250, 204, 21)',  // yellow
            0.8, 'rgb(239, 68, 68)'    // red
          ],
          'heatmap-radius': 30,
          'heatmap-opacity': 0.7
        }
      });
    }
    
    // Handle symptom reports (markers)
    // First, remove existing markers if any
    const existingMarkers = document.querySelectorAll('.symptom-marker');
    existingMarkers.forEach(marker => marker.remove());
    
    // Add new markers
    reportsData.features.forEach(feature => {
      const { properties, geometry } = feature;
      const { symptom, severity, color } = properties;
      
      // Create marker element
      const markerEl = document.createElement('div');
      markerEl.className = 'symptom-marker';
      markerEl.style.width = '15px';
      markerEl.style.height = '15px';
      markerEl.style.backgroundColor = color;
      markerEl.style.borderRadius = '50%';
      markerEl.style.border = '2px solid white';
      markerEl.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)';
      
      // Add tooltip using a popup
      const popup = new mapboxgl.Popup({
        closeButton: false,
        closeOnClick: false,
        offset: 15,
        className: 'symptom-popup'
      }).setHTML(`
        <div class="p-2">
          <strong>${symptom}</strong>
          <div class="text-sm">Severity: <span style="color:${color}">${severity}</span></div>
        </div>
      `);
      
      // Add marker to map
      new mapboxgl.Marker(markerEl)
        .setLngLat(geometry.coordinates as [number, number])
        .setPopup(popup)
        .addTo(map.current!);
    });
    
    toast.info(`Updated map data for ${location} - ${diseaseType}`);
  };

  return (
    <div className="relative w-full h-full">
      <div ref={mapContainerRef} className="map-container" style={{ height: '400px' }} />
      <MapLegend diseaseType={diseaseType} />
    </div>
  );
}
