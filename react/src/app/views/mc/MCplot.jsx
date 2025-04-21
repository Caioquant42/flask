import React, { useState } from 'react';
import axios from 'axios';
import { 
  Box, 
  Button, 
  Card, 
  CardContent, 
  Container, 
  Grid, 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  TextField, 
  Typography,
  Snackbar,
  Alert
} from '@mui/material';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  BarChart,
  Bar,
  ReferenceLine,
  ReferenceArea
} from 'recharts';
import { LoadingButton } from '@mui/lab';
import API_BASE_URL from "@/__api__/db/apiService";

const MCplot = ({ onDataReceived }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [selectedStock, setSelectedStock] = useState(null);
  const [formData, setFormData] = useState({
    stocks: 'PRIO3',
    period: 6,
    iterations: 1000,
    time_steps: 252
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info'
  });

  const handleInputChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'stocks' ? value : Number(value)
    }));
  };

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') return;
    setSnackbar(s => ({ ...s, open: false }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const { data } = await axios.post(`${API_BASE_URL}/bootstrap`, {
        stocks: formData.stocks,
        period: formData.period,
        iterations: formData.iterations,
        time_steps: formData.time_steps
      });

      setResults(data);
      const first = Object.keys(data)[0];
      setSelectedStock(first);
      onDataReceived?.(data);

      setSnackbar({
        open: true,
        message: 'Simulation completed successfully!',
        severity: 'success'
      });
    } catch (err) {
      setSnackbar({
        open: true,
        message: err.response?.data?.message || 'Error running simulation',
        severity: 'error'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getArrivalDistributionData = () => {
    if (!results || !selectedStock) return [];
    const arrivals = results[selectedStock].monte_carlo.all_arrivals || [];
    if (!arrivals.length) return [];

    const min = Math.min(...arrivals);
    const max = Math.max(...arrivals);
    const bins = 20;
    const size = (max - min) / bins;
    const bucket = Array.from({ length: bins }, (_, i) => ({
      min: min + i * size,
      max: min + (i + 1) * size,
      count: 0
    }));

    arrivals.forEach(v => {
      const idx = Math.min(Math.floor((v - min) / size), bins - 1);
      bucket[idx].count++;
    });

    return bucket.map(b => ({
      name: `${b.min.toFixed(2)}–${b.max.toFixed(2)}`,
      value: b.count,
      range: [b.min, b.max]
    }));
  };

  const getMonteCarloPathsData = () => {
    if (!results || !selectedStock) return [];
    return Array.from({ length: 5 }, (_, i) => ({
      name: `Path ${i + 1}`,
      steps: Array.from({ length: 10 }, (_, j) => ({
        step: j,
        value: results[selectedStock].monte_carlo.all_arrivals[i] * (j / 9)
      }))
    }));
  };

  const getMetricsData = () => {
    if (!results || !selectedStock) return [];
    const mc = results[selectedStock].monte_carlo;
    return [
      { name: 'Mean', value: mc.mean },
      { name: 'Median', value: mc.median },
      { name: 'Std Dev', value: mc.std },
      { name: 'Min', value: mc.min },
      { name: 'Max', value: mc.max },
      { name: '1%', value: mc.percentiles['1%'] },
      { name: '5%', value: mc.percentiles['5%'] },
      { name: '25% (Q1)', value: mc.percentiles['25%'] },
      { name: '75% (Q3)', value: mc.percentiles['75%'] },
      { name: '95%', value: mc.percentiles['95%'] },
      { name: '99%', value: mc.percentiles['99%'] },
      { name: 'IQR', value: mc.percentiles['75%'] - mc.percentiles['25%'] },
      { name: 'Current Price', value: results[selectedStock].cdf_values.S0 }
    ];
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Monte Carlo Simulation Analysis
      </Typography>

      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Simulation Parameters
          </Typography>
          <Box component="form" onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              {[
                { label: 'Stocks', name: 'stocks', type: 'text' },
                { label: 'Period (mo)', name: 'period', type: 'number' },
                { label: 'Iterations', name: 'iterations', type: 'number' },
                { label: 'Time Steps', name: 'time_steps', type: 'number' }
              ].map(({ label, name, type }) => (
                <Grid item xs={12} sm={6} md={3} key={name}>
                  <TextField
                    label={label}
                    name={name}
                    type={type}
                    value={formData[name]}
                    onChange={handleInputChange}
                    fullWidth
                    inputProps={type === 'number' ? { min: 1 } : {}}
                  />
                </Grid>
              ))}
              <Grid item xs={12}>
                <LoadingButton
                  type="submit"
                  variant="contained"
                  loading={isLoading}
                >
                  Run Simulation
                </LoadingButton>
              </Grid>
            </Grid>
          </Box>
        </CardContent>
      </Card>

      {results && (
        <>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            {Object.keys(results).map(stock => (
              <Grid item key={stock}>
                <Button
                  variant={stock === selectedStock ? 'contained' : 'outlined'}
                  onClick={() => setSelectedStock(stock)}
                >
                  {stock}
                </Button>
              </Grid>
            ))}
          </Grid>

          {selectedStock && (
            <Grid container spacing={3}>
              {/* Distribution */}
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Arrival Price Distribution – {selectedStock}
                    </Typography>
                    <Box sx={{ height: 400 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={getArrivalDistributionData()}
                          margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis
                            dataKey="name"
                            angle={-45}
                            textAnchor="end"
                            height={60}
                          />
                          <YAxis
                            label={{
                              value: 'Frequency',
                              angle: -90,
                              position: 'insideLeft'
                            }}
                          />
                          <Tooltip />
                          <Bar dataKey="value" fill="#8884d8" name="Freq" />
                          <ReferenceLine
                            x={0}
                            stroke="green"
                            label={{
                              value: `Current: ${results[selectedStock]
                                .cdf_values.S0.toFixed(2)}`,
                              position: 'top'
                            }}
                          />
                          <ReferenceArea
                            x1={getArrivalDistributionData().findIndex(
                              d =>
                                d.range[0] <=
                                  results[selectedStock].monte_carlo.percentiles[
                                    '25%'
                                  ] &&
                                d.range[1] >
                                  results[selectedStock].monte_carlo.percentiles[
                                    '25%'
                                  ]
                            )}
                            x2={getArrivalDistributionData().findIndex(
                              d =>
                                d.range[0] <=
                                  results[selectedStock].monte_carlo.percentiles[
                                    '75%'
                                  ] &&
                                d.range[1] >
                                  results[selectedStock].monte_carlo.percentiles[
                                    '75%'
                                  ]
                            )}
                            stroke="blue"
                            fill="blue"
                            fillOpacity={0.1}
                            label="IQR"
                          />
                        </BarChart>
                      </ResponsiveContainer>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>

              {/* Paths */}
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Monte Carlo Paths – {selectedStock}
                    </Typography>
                    <Box sx={{ height: 400 }}>
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                          margin={{
                            top: 20,
                            right: 30,
                            left: 20,
                            bottom: 60
                          }}
                        >
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis
                            label={{
                              value: 'Time Step',
                              position: 'insideBottomRight',
                              offset: -10
                            }}
                          />
                          <YAxis
                            label={{
                              value: 'Price',
                              angle: -90,
                              position: 'insideLeft'
                            }}
                          />
                          <Tooltip />
                          <Legend />
                          {getMonteCarloPathsData().map((path, i) => (
                            <Line
                              key={i}
                              type="monotone"
                              dataKey="value"
                              data={path.steps}
                              name={path.name}
                              stroke={`#${Math
                                .floor(Math.random() * 16777215)
                                .toString(16)}`}
                              activeDot={{ r: 8 }}
                            />
                          ))}
                        </LineChart>
                      </ResponsiveContainer>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>

              {/* Metrics */}
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Simulation Metrics – {selectedStock}
                    </Typography>
                    <TableContainer component={Paper}>
                      <Table>
                        <TableHead>
                          <TableRow>
                            <TableCell>Metric</TableCell>
                            <TableCell align="right">Value</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {getMetricsData().map(row => (
                            <TableRow key={row.name}>
                              <TableCell component="th" scope="row">
                                {row.name}
                              </TableCell>
                              <TableCell align="right">
                                {typeof row.value === 'number'
                                  ? row.value.toFixed(4)
                                  : row.value}
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          )}
        </>
      )}

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          onClose={handleSnackbarClose}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default MCplot;