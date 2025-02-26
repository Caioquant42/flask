import React from 'react';
import Plot from 'react-plotly.js';

const VolSurface = ({ height, width }) => {
  // Mock data for PETR4 volatility surface
  const generateMockData = () => {
    const dates = ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01'];
    const daysToMaturity = [30, 60, 90, 120, 150, 180];
    const z_data = [];

    for (let i = 0; i < dates.length; i++) {
      const row = [];
      for (let j = 0; j < daysToMaturity.length; j++) {
        // Generate a mock volatility value
        // This is a simplified model and doesn't reflect real market behavior
        const baseVol = 0.3; // 30% base volatility
        const dateEffect = i * 0.01; // Slight increase over time
        const maturityEffect = j * 0.005; // Slight increase for longer maturities
        const randomness = (Math.random() - 0.5) * 0.05; // Add some randomness
        
        const vol = baseVol + dateEffect + maturityEffect + randomness;
        row.push(vol);
      }
      z_data.push(row);
    }

    return {
      x: dates,
      y: daysToMaturity,
      z: z_data
    };
  };

  const mockData = generateMockData();

  const data = [{
    x: mockData.x,
    y: mockData.y,
    z: mockData.z,
    type: 'surface',
    colorscale: 'Viridis',
    colorbar: {
      title: 'Implied Volatility',
      titleside: 'right'
    }
  }];

  const layout = {
    title: 'PETR4 Volatility Surface',
    autosize: false,
    width: width || 700,
    height: height || 700,
    scene: {
      xaxis: { title: 'Date' },
      yaxis: { title: 'Days to Maturity' },
      zaxis: { title: 'Implied Volatility (Annualized)' }
    },
    margin: {
      l: 65,
      r: 50,
      b: 65,
      t: 90,
    }
  };

  return (
    <Plot
      data={data}
      layout={layout}
    />
  );
};

export default VolSurface;