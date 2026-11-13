document.addEventListener('DOMContentLoaded', () => {
    const radios = document.querySelectorAll('input[name="layer"]');
    const sliderContainer = document.getElementById('slider-container');
    const prioritySlider = document.getElementById('priority-slider');
    const sliderLabel = document.getElementById('slider-label');
    const drawer = document.getElementById('info-drawer');
    const closeDrawerBtn = document.getElementById('close-drawer');

    let currentLayerMode = 'base';
    let currentSliderVal = 2;

    // Mock dataset representing 21 Edinburgh study sites
    const mockGeoJSON = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": { "type": "Polygon", "coordinates": [[[-3.19, 55.95], [-3.18, 55.95], [-3.18, 55.96], [-3.19, 55.96], [-3.19, 55.95]]] },
                "properties": { "name": "Meadows Park", "land_type": "greenspace", "trees": 1420, "carbon_stock": 88.5, "deprivation_percentile": 72 }
            },
            {
                "type": "Feature",
                "geometry": { "type": "Polygon", "coordinates": [[[-3.21, 55.94], [-3.20, 55.94], [-3.20, 55.95], [-3.21, 55.95], [-3.21, 55.94]]] },
                "properties": { "name": "Sighthill Brownspace", "land_type": "brownspace", "trees": 140, "carbon_stock": 18.2, "deprivation_percentile": 91 }
            }
        ]
    };

    function renderLayer() {
        if (studySitesLayer) {
            map.removeLayer(studySitesLayer);
        }

        studySitesLayer = L.geoJSON(mockGeoJSON, {
            style: (feature) => getSiteStyle(feature, currentLayerMode, currentSliderVal),
            onEachFeature: (feature, layer) => {
                layer.on('click', () => {
                    document.getElementById('park-title').innerText = feature.properties.name;
                    document.getElementById('metric-trees').innerText = feature.properties.trees.toLocaleString();
                    document.getElementById('metric-carbon').innerText = feature.properties.carbon_stock;
                    document.getElementById('metric-deprivation').innerText = feature.properties.deprivation_percentile;
                    drawer.classList.remove('hidden');
                });
            }
        }).addTo(map);
    }

    // Layer toggle event listeners
    radios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            currentLayerMode = e.target.value;
            if (currentLayerMode === 'priority') {
                sliderContainer.classList.remove('hidden');
            } else {
                sliderContainer.classList.add('hidden');
            }
            renderLayer();
        });
    });

    // Slider event listener
    prioritySlider.addEventListener('input', (e) => {
        currentSliderVal = parseInt(e.target.value);
        const descriptions = ["Carbon Heavy (0/4)", "Balanced Low (1/4)", "Balanced Mid (2/4)", "Balanced High (3/4)", "Equity Heavy (4/4)"];
        sliderLabel.innerText = descriptions[currentSliderVal];
        renderLayer();
    });

    closeDrawerBtn.addEventListener('click', () => {
        drawer.classList.add('hidden');
    });

    // Initial render call
    renderLayer();
});
