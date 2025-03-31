import React, { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';
import { fetchFLUXOendpoint } from "/src/__api__/db/apiService";
import { Box, CircularProgress, Typography, useTheme } from '@mui/material';

const FluxoEstrangeiro = () => {
  const theme = useTheme();
  const chartRef1 = useRef(null);
  const chartRef2 = useRef(null);
  const chartRef3 = useRef(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetchFLUXOendpoint();
        if (response.error) {
          throw new Error(response.error);
        }
        
        const data = response.fluxo_ddm; // Access the fluxo_ddm array
        
        const formattedData = data.map(item => ({
          date: new Date(item.Data.split('/').reverse().join('-')),
          Estrangeiro: parseFloat(item.Estrangeiro.replace(' mi', '').replace(',', '.')),
          Institucional: parseFloat(item.Institucional.replace(' mi', '').replace(',', '.')),
          Outros: parseFloat(item.Outros.replace(' mi', '').replace(',', '.')),
          Todos: parseFloat(item.Todos.replace(' mi', '').replace(',', '.'))
        }));
        
        formattedData.sort((a, b) => a.date - b.date);
        
        const finalData = formattedData.map(item => ({
          ...item,
          date: item.date.toISOString().split('T')[0]
        }));

        setChartData(finalData);
        setError(null);
      } catch (error) {
        console.error("Error fetching data:", error);
        setError("Falha ao carregar dados. Por favor, tente novamente mais tarde.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []); 

  useEffect(() => {
    if (chartData.length) {
      const createBarChart = (chartRef, title, series) => {
        const chart = echarts.init(chartRef.current);
        const option = {
          title: { 
            text: title, 
            left: 'center',
            textStyle: {
              color: theme.palette.text.primary,
              fontFamily: theme.typography.fontFamily,
              fontSize: 16,
              fontWeight: 500
            }
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            formatter: function(params) {
              let result = `${params[0].axisValue}<br/>`;
              params.forEach(param => {
                result += `${param.marker} ${param.seriesName}: ${param.data.value.toFixed(2)} mi<br/>`;
              });
              return result;
            }
          },
          legend: {
            data: series.map(s => ({
              name: s.name,
              itemStyle: { color: s.color }
            })),
            bottom: 0,
            padding: [0, 0, 25, 0],
            textStyle: {
              color: theme.palette.text.secondary,
              fontSize: 12
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            containLabel: true
          },
          toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
              mark: { show: true },
              dataView: { show: true, readOnly: false },
              magicType: { show: true, type: ['line', 'bar', 'stack'] },
              restore: { show: true },
              saveAsImage: { show: true }
            }
          },
          xAxis: [{
            type: 'category',
            axisTick: { show: false },
            data: chartData.map(item => item.date),
            axisLabel: { 
              rotate: 45,
              color: theme.palette.text.secondary,
              fontSize: 11
            }
          }],
          yAxis: [{
            type: 'value',
            name: 'Milhões',
            axisLabel: {
              color: theme.palette.text.secondary,
              fontSize: 11
            },
            splitLine: {
              lineStyle: {
                color: theme.palette.divider,
                opacity: 0.5
              }
            }
          }],
          series: series.map(s => ({
            name: s.name,
            type: 'bar',
            data: chartData.map(item => ({
              value: item[s.key],
              itemStyle: { color: s.color }
            })),
            barWidth: 15,
            emphasis: { focus: 'series' }
          }))
        };
        chart.setOption(option);
        return chart;
      };

      const createLineChart = (chartRef, title, series) => {
        const chart = echarts.init(chartRef.current);
        
        const cumulativeData = {};
        series.forEach(s => {
          cumulativeData[s.key] = [];
          let sum = 0;
          chartData.forEach(item => {
            sum += item[s.key];
            cumulativeData[s.key].push(sum);
          });
        });

        const option = {
          title: { 
            text: title,
            left: 'center',
            textStyle: {
              color: theme.palette.text.primary,
              fontFamily: theme.typography.fontFamily,
              fontSize: 16,
              fontWeight: 500
            }
          },
          tooltip: {
            trigger: 'axis',
            formatter: function(params) {
              let result = `${params[0].axisValue}<br/>`;
              params.forEach(param => {
                result += `${param.marker} ${param.seriesName}: ${param.data.toFixed(2)} mi<br/>`;
              });
              return result;
            }
          },
          legend: {
            data: series.map(s => ({
              name: s.name,
              itemStyle: { color: s.color }
            })),
            bottom: 0,
            padding: [0, 0, 25, 0],
            textStyle: {
              color: theme.palette.text.secondary,
              fontSize: 12
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            containLabel: true
          },
          toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
              mark: { show: true },
              dataView: { show: true, readOnly: false },
              magicType: { show: true, type: ['line', 'bar'] },
              restore: { show: true },
              saveAsImage: { show: true }
            }
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: chartData.map(item => item.date),
            axisLabel: { 
              rotate: 45,
              color: theme.palette.text.secondary,
              fontSize: 11
            }
          },
          yAxis: {
            type: 'value',
            name: 'Milhões (Acumulado)',
            axisLabel: {
              color: theme.palette.text.secondary,
              fontSize: 11
            },
            splitLine: {
              lineStyle: {
                color: theme.palette.divider,
                opacity: 0.5
              }
            }
          },
          series: series.map(s => ({
            name: s.name,
            type: 'line',
            data: cumulativeData[s.key],
            itemStyle: { color: s.color },
            smooth: true,
            symbol: 'none'
          }))
        };
        chart.setOption(option);
        return chart;
      };

      const charts = [
        createBarChart(chartRef1, 'Fluxo Estrangeiro e Institucional', [
          { name: 'Estrangeiro', key: 'Estrangeiro', color: '#4CAF50' },
          { name: 'Institucional', key: 'Institucional', color: '#2196F3' }
        ]),
        createBarChart(chartRef2, 'Outros e Todos', [
          { name: 'Outros', key: 'Outros', color: '#9C27B0' },
          { name: 'Todos', key: 'Todos', color: '#FFA726' }
        ]),
        createLineChart(chartRef3, 'Fluxo Acumulado', [
          { name: 'Estrangeiro', key: 'Estrangeiro', color: '#4CAF50' },
          { name: 'Institucional', key: 'Institucional', color: '#2196F3' },
          { name: 'Outros', key: 'Outros', color: '#9C27B0' },
          { name: 'Todos', key: 'Todos', color: '#FFA726' }
        ])
      ];

      const handleResize = () => charts.forEach(chart => chart.resize());
      window.addEventListener('resize', handleResize);

      return () => {
        window.removeEventListener('resize', handleResize);
        charts.forEach(chart => chart.dispose());
      };
    }
  }, [chartData, theme]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="400px">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <div ref={chartRef1} style={{ width: '100%', height: '400px', marginBottom: '20px' }} />
      <div ref={chartRef2} style={{ width: '100%', height: '400px', marginBottom: '20px' }} />
      <div ref={chartRef3} style={{ width: '100%', height: '400px' }} />
    </Box>
  );
};

export default FluxoEstrangeiro;