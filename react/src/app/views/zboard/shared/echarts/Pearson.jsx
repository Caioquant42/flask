import React from 'react';
import { useTheme } from "@mui/material/styles";
import ReactEcharts from "echarts-for-react";

const Pearson = ({ height, color = [] }) => {
  const theme = useTheme();

  // Mock data for Pearson correlations
  const mockData = [
    { date: '2023-01', CDI: 0.2, Dolar: -0.3, Ouro: 0.1, SP500: 0.5 },
    { date: '2023-02', CDI: 0.25, Dolar: -0.35, Ouro: 0.15, SP500: 0.55 },
    { date: '2023-03', CDI: 0.3, Dolar: -0.4, Ouro: 0.2, SP500: 0.6 },
    { date: '2023-04', CDI: 0.35, Dolar: -0.45, Ouro: 0.25, SP500: 0.65 },
    { date: '2023-05', CDI: 0.4, Dolar: -0.5, Ouro: 0.3, SP500: 0.7 },
    { date: '2023-06', CDI: 0.45, Dolar: -0.55, Ouro: 0.35, SP500: 0.75 },
    { date: '2023-07', CDI: 0.5, Dolar: -0.6, Ouro: 0.4, SP500: 0.8 },
    { date: '2023-08', CDI: 0.55, Dolar: -0.65, Ouro: 0.45, SP500: 0.85 },
    { date: '2023-09', CDI: 0.6, Dolar: -0.7, Ouro: 0.5, SP500: 0.9 },
  ];

  const option = {
    title: {
      text: 'Correlação de Pearson do IBOV',
      left: 'center',
      textStyle: {
        color: theme.palette.text.primary,
        fontFamily: theme.typography.fontFamily
      }
    },
    grid: { top: "10%", bottom: "15%", left: "3%", right: "3%" },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        let result = `${params[0].axisValue}<br/>`;
        params.forEach(param => {
          result += `${param.seriesName}: ${param.value.toFixed(2)}<br/>`;
        });
        return result;
      }
    },
    legend: {
      data: ['CDI', 'Dólar', 'Ouro', 'S&P 500'],
      bottom: 0
    },
    xAxis: {
      type: "category",
      data: mockData.map(item => item.date),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        fontSize: 12,
        fontFamily: theme.typography.fontFamily,
        color: theme.palette.text.secondary
      }
    },
    yAxis: {
      type: "value",
      min: -1,
      max: 1,
      interval: 0.2,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: {
        lineStyle: { color: theme.palette.text.secondary, opacity: 0.15 }
      },
      axisLabel: {
        color: theme.palette.text.secondary,
        fontSize: 12,
        fontFamily: theme.typography.fontFamily,
        formatter: '{value}'
      }
    },
    series: [
      {
        name: 'CDI',
        data: mockData.map(item => item.CDI),
        type: "line",
        smooth: true,
        symbolSize: 6,
        lineStyle: { width: 2 }
      },
      {
        name: 'Dólar',
        data: mockData.map(item => item.Dolar),
        type: "line",
        smooth: true,
        symbolSize: 6,
        lineStyle: { width: 2 }
      },
      {
        name: 'Ouro',
        data: mockData.map(item => item.Ouro),
        type: "line",
        smooth: true,
        symbolSize: 6,
        lineStyle: { width: 2 }
      },
      {
        name: 'S&P 500',
        data: mockData.map(item => item.SP500),
        type: "line",
        smooth: true,
        symbolSize: 6,
        lineStyle: { width: 2 }
      }
    ]
  };

  return <ReactEcharts style={{ height: height }} option={{ ...option, color: [...color] }} />;
}

export default Pearson;