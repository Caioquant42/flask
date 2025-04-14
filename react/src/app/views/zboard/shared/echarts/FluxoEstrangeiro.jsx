import React, { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';
import { fetchFLUXOendpoint } from "/src/__api__/db/apiService";
import { 
  Box, 
  CircularProgress, 
  Typography, 
  useTheme, 
  Slider, 
  Stack,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper
} from '@mui/material';

const FluxoEstrangeiro = () => {
  const theme = useTheme();
  const chartRef1 = useRef(null);
  const chartRef2 = useRef(null);
  const chartRef3 = useRef(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dateRange, setDateRange] = useState([0, 100]); // Percentual do intervalo de datas
  const [filteredData, setFilteredData] = useState([]);
  const [chart3Instance, setChart3Instance] = useState(null);
  const [dateLabels, setDateLabels] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetchFLUXOendpoint();
        console.log("API response:", response);
        if (response.error) {
          throw new Error(response.error);
        }
        
        // Assuming the response structure is { fluxo_ddm: [...] }
        const data = response.fluxo_ddm || [];
        
        const formattedData = data.map(item => {
          const parseValue = (value) => {
            if (typeof value === 'string') {
              // Handle negative numbers and different formats
              const numStr = value.replace(/[^\d,-]/g, '')  // Remove all non-digit, non-comma, non-minus
                                  .replace('.', '')         // Remove thousand separators
                                  .replace(',', '.');       // Convert decimal comma to dot
              return parseFloat(numStr) || 0;
            }
            return typeof value === 'number' ? value : 0;
          };

          return {
            date: new Date(item.Data.split('/').reverse().join('-')),
            Estrangeiro: parseValue(item.Estrangeiro),
            PF: parseValue(item.PF),
            Institucional: parseValue(item.Institucional),
            IF: parseValue(item.IF),
            Outros: parseValue(item.Outros),
            Todos: parseValue(item.Todos)
          };
        });
        
        formattedData.sort((a, b) => a.date - b.date);
        
        const finalData = formattedData.map(item => ({
          ...item,
          date: item.date.toISOString().split('T')[0]
        }));

        setChartData(finalData);
        setFilteredData(finalData);
        setDateLabels(finalData.map(item => item.date));
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

  // Atualiza os dados filtrados quando o intervalo de datas muda
  useEffect(() => {
    if (chartData.length > 0) {
      const startIndex = Math.floor(chartData.length * (dateRange[0] / 100));
      const endIndex = Math.floor(chartData.length * (dateRange[1] / 100));
      
      // Garantir que pelo menos um item seja selecionado
      const filteredSlice = chartData.slice(
        startIndex, 
        endIndex < chartData.length ? endIndex + 1 : chartData.length
      );
      
      setFilteredData(filteredSlice);
      
      // Atualiza o gráfico 3 se ele já estiver criado
      if (chart3Instance) {
        updateChart3(chart3Instance, filteredSlice);
      }
    }
  }, [dateRange, chartData]);

  const updateChart3 = (chart, data) => {
    const series = [
      { name: 'Estrangeiro', key: 'Estrangeiro', color: '#4CAF50' },
      { name: 'Pessoa Física', key: 'PF', color: '#FFA726' },
      { name: 'Institucional', key: 'Institucional', color: '#2196F3' },
      { name: 'Inst. Financeira', key: 'IF', color: '#9C27B0' },
      { name: 'Outros', key: 'Outros', color: '#FF5722' }
    ];

    const cumulativeData = {};
    series.forEach(s => {
      cumulativeData[s.key] = [];
      let sum = 0;
      data.forEach(item => {
        sum += item[s.key];
        cumulativeData[s.key].push(sum);
      });
    });

    chart.setOption({
      xAxis: {
        data: data.map(item => item.date)
      },
      series: series.map(s => ({
        name: s.name,
        data: cumulativeData[s.key]
      }))
    });
  };

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
          filteredData.forEach(item => {
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
            data: filteredData.map(item => item.date),
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
        setChart3Instance(chart);
        return chart;
      };

      const charts = [
        createBarChart(chartRef1, 'Fluxo Estrangeiro e Pessoa Física', [
          { name: 'Estrangeiro', key: 'Estrangeiro', color: '#4CAF50' },
          { name: 'Pessoa Física', key: 'PF', color: '#FFA726' }
        ]),

        createBarChart(chartRef2, 'Fluxo Institucional, Inst. Financeira e Outros', [
          { name: 'Institucional', key: 'Institucional', color: '#2196F3' },
          { name: 'Inst. Financeira', key: 'IF', color: '#9C27B0' },
          { name: 'Outros', key: 'Outros', color: '#FF5722' }
        ]),

        createLineChart(chartRef3, 'Fluxo Acumulado', [
          { name: 'Estrangeiro', key: 'Estrangeiro', color: '#4CAF50' },
          { name: 'Pessoa Física', key: 'PF', color: '#FFA726' },
          { name: 'Institucional', key: 'Institucional', color: '#2196F3' },
          { name: 'Inst. Financeira', key: 'IF', color: '#9C27B0' },
          { name: 'Outros', key: 'Outros', color: '#FF5722' }
        ])
      ];

      const handleResize = () => charts.forEach(chart => chart.resize());
      window.addEventListener('resize', handleResize);

      return () => {
        window.removeEventListener('resize', handleResize);
        charts.forEach(chart => chart.dispose());
      };
    }
  }, [chartData, filteredData, theme]);

  const handleDateRangeChange = (event, newValue) => {
    setDateRange(newValue);
  };

  // Função para formatar as marcas do slider
  const formatSliderLabel = (value) => {
    if (dateLabels.length === 0) return '';
    const index = Math.floor(dateLabels.length * (value / 100));
    if (index >= dateLabels.length) return dateLabels[dateLabels.length - 1];
    return dateLabels[index];
  };

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
      
      {/* Controle de período para o gráfico de Fluxo Acumulado */}
      <Paper 
        elevation={2} 
        sx={{ 
          p: 3, 
          mb: 2, 
          borderRadius: 2,
          backgroundColor: theme.palette.background.paper
        }}
      >
        <Typography variant="subtitle1" gutterBottom>
          Filtrar período para Fluxo Acumulado
        </Typography>
        
        <Box px={2} py={1}>
          <Slider
            value={dateRange}
            onChange={handleDateRangeChange}
            valueLabelDisplay="auto"
            valueLabelFormat={formatSliderLabel}
            min={0}
            max={100}
            sx={{ 
              '& .MuiSlider-valueLabel': {
                backgroundColor: theme.palette.primary.main,
              }
            }}
          />
          
          <Box display="flex" justifyContent="space-between" mt={1}>
            <Typography variant="caption" color="textSecondary">
              {formatSliderLabel(dateRange[0])}
            </Typography>
            <Typography variant="caption" color="textSecondary">
              {formatSliderLabel(dateRange[1])}
            </Typography>
          </Box>
        </Box>
      </Paper>
      
      <div ref={chartRef3} style={{ width: '100%', height: '400px' }} />
    </Box>
  );
};

export default FluxoEstrangeiro;