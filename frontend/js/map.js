// Initialize Leaflet map centered on Edinburgh
const map = L.map('map', {
    zoomControl: false
}).setView([55.9533, -3.1883], 13);

// Add custom zoom control position
L.control.zoom({ position: 'bottomright' }).addTo(map);

// Load CartoDB Positron Basemap (Clean desaturated background)
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
}).addTo(map);

// Global reference for active geojson layer
let studySitesLayer = null;
