import React from 'react';
import Plot from 'react-plotly.js';
import { useState, useEffect } from 'react';
import { set } from 'lodash';

function SignalPlot({ data, title }) {
    const colors = ['Red', 'Green', 'Blue'];
    const [plotWidth, setPlotWidth] = useState(600);
    const [plotHeight, setPlotHeight] = useState(400);

    const traces = data.map((channelData, i) => ({
        x: channelData[0],
        y: channelData[1],
        type: 'scatter',
        mode: 'lines',
        name: colors[i],
        line: { color: colors[i].toLowerCase() },
    }));

    function calculateParentWidth(id) {
        const parentWidth = document.getElementById(id).parentElement.clientWidth;
        return parentWidth;
    }
    function calculateParentHeight(id) {
        const parentHeight = document.getElementById(id).parentElement.clientHeight;
        return parentHeight;
    }
    
    useEffect(() => {
        const parentWidth = calculateParentWidth('myPlotContainer'); // Replace with your actual container ID
        const plotWidth = parentWidth * 0.9; // Set the desired percentage (e.g., 90%)
        const plotHeight = calculateParentHeight('myPlotContainer') * 0.9; // Set the desired percentage (e.g., 90%)

        if(plotHeight > 300) {
            setPlotWidth(plotWidth);
            setPlotHeight(plotHeight);
        }
        console.log('plotWidth', plotWidth);
        console.log('plotHeight', plotHeight);
    }, []);

    return (
        <div style={{ width: '100%', height: '100%' }} id="myPlotContainer">
            <Plot
                data={traces}
                layout={{
                    title: `${title} Signal`,
                    autosize: false,
                    width: plotWidth,
                    height: plotHeight
                }}
                
            />
        </div>
    );
}

export default SignalPlot;
