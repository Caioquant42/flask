import React from 'react';
import { useTheme } from "@mui/material/styles";
import ReactEcharts from "echarts-for-react";

const Performance = ({ height, color = [] }) => {
  const theme = useTheme();

  // Mock data for asset performance (percentage change)
  const mockData = [
    { date: '2023-01-01', IBOV: 0, CDI: 0, Dolar: 0, Ouro: 0, SP500: 0 },
    { date: '2023-02-01', IBOV: 2.5, CDI: 1.0, Dolar: -1.5, Ouro: 3.0, SP500: 1.8 },
    { date: '2023-03-01', IBOV: 5.0, CDI: 2.1, Dolar: -3.0, Ouro: 5.5, SP500: 3.5 },
    { date: '2023-04-01', IBOV: 4.2, CDI: 3.2, Dolar: -2.0, Ouro: 7.0, SP500: 5.2 },
    { date: '2023-05-01', IBOV: 6.8, CDI: 4.3, Dolar: -4.5, Ouro: 8.5, SP500: 6.0 },
    { date: '2023-06-01', IBOV: 8.5, CDI: 5.4, Dolar: -5.0, Ouro: 10.0, SP500: 7.8 },
    { date: '2023-07-01', IBOV: 7.0, CDI: 6.5, Dolar: -3.5, Ouro: 12.5, SP500: 9.5 },
    { date: '2023-08-01', IBOV: 9.5, CDI: 7.6, Dolar: -6.0, Ouro: 15.0, SP500: 11.0 },
    { date: '2023-09-01', IBOV: 11.0, CDI: 8.7, Dolar: -7.5, Ouro: 17.5, SP500: 12.5 },
  ];

  const option = {
    title: {
      text: 'Performance Relativa dos Ativos',
      left: 'center',
      textStyle: {
        color: theme.palette.text.primary,
        fontFamily: theme.typography.fontFamily
      }
    },
    grid: { top: "10%", bottom: "10%", left: "3%", right: "3%" },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        let result = `${params[0].axisValue}<br/>`;
        params.forEach(param => {
          result += `${param.seriesName}: ${param.value.toFixed(2)}%<br/>`;
        });
        return result;
      }
    },
    legend: {
      data: ['IBOV', 'CDI', 'Dólar', 'Ouro', 'S&P 500'],
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
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: {
        lineStyle: { color: theme.palette.text.secondary, opacity: 0.15 }
      },
      axisLabel: {
        color: theme.palette.text.secondary,
        fontSize: 12,
        fontFamily: theme.typography.fontFamily,
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: 'IBOV',
        data: mockData.map(item => item.IBOV),
        type: "line",
        smooth: true,
        symbolSize: 6,
        lineStyle: { width: 2 }
      },
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

export default Performance;