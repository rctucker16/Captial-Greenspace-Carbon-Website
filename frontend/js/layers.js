// Style configurations based on active layer toggle
function getSiteStyle(feature, activeLayer, sliderStep = 2) {
    if (activeLayer === 'base') {
        const type = feature.properties.land_type;
        return {
            fillColor: type === 'greenspace' ? '#22c55e' : type === 'brownspace' ? '#a16207' : '#94a3b8',
            weight: 1,
            opacity: 1,
            color: 'white',
            fillOpacity: 0.6
        };
    } else if (activeLayer === 'carbon') {
        // Layer 1: Purple Gradient (High carbon = dark purple)
        const carbon = feature.properties.carbon_stock || 0;
        return {
            fillColor: carbon > 75 ? '#581c87' : carbon > 40 ? '#7e22ce' : '#c084fc',
            weight: 1,
            color: '#ffffff',
            fillOpacity: 0.7
        };
    } else if (activeLayer === 'deprivation') {
        // Layer 2: Deprivation Choropleth
        const dep = feature.properties.deprivation_percentile || 50;
        return {
            fillColor: dep > 80 ? '#b91c1c' : dep > 50 ? '#f97316' : '#fef08a',
            weight: 1,
            color: '#ffffff',
            fillOpacity: 0.65
        };
    } else if (activeLayer === 'priority') {
        // Layer 3: Pre-computed 5-step priority slider styling
        const prioritySteps = ['#fee2e2', '#fca5a5', '#f87171', '#dc2626', '#991b1b'];
        return {
            fillColor: prioritySteps[sliderStep],
            weight: 1.5,
            color: '#7f1d1d',
            fillOpacity: 0.75
        };
    }
}
