import React from 'react';
import Plot from 'react-plotly.js';

const PlotComponent = () => {
    // Generate fake data
    const x = Array.from({length: 100}, (_, i) => i);
    const y = x.map(val => Math.sin(val / 10));

    // Create plot data object
    const plotData = [
        {
            x,
            y,
            type: 'scatter',
            mode: 'lines',
            line: {color: 'blue'},
        },
    ];

    return <Plot data={plotData} editable={false}/>;
};

export default PlotComponent;