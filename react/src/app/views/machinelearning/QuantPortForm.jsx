import React, { useState } from 'react';
import { 
  Box, TextField, Button, Snackbar, Alert, 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper,
  Tooltip
} from '@mui/material';
import { styled } from "@mui/material/styles";
import axios from 'axios';

const StyledButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(2, 0),
}));

const paramDescriptions = {
  nret_mln: "Number of returns for mlnsupport function",
  nclusters: "Number of clusters for mlnsupport function",
  period_ret: "Period of returns for both functions",
  ret_mc: "Return threshold for mcport function",
  n_sim_mc: "Number of simulations for mcport function",
  tam_port: "Portfolio size for mcport function"
};

export default function QuantPortForm() {
  const [params, setParams] = useState({
    nret_mln: 15,
    nclusters: 4,
    period_ret: 2,
    ret_mc: 7,
    n_sim_mc: 1000,
    tam_port: 5
  });
  const [isLoading, setIsLoading] = useState(false);
  const [mlnsupportData, setMlnsupportData] = useState([]);
  const [mcportData, setMcportData] = useState({});
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info'
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setParams(prevParams => ({
      ...prevParams,
      [name]: parseInt(value, 10)
    }));
  };

  const handleAprender = async () => {
    try {
      setIsLoading(true);
      const response = await axios.post('http://127.0.0.1:5000/api/quant_port', params);
      
      console.log('API Response:', response.data);
      
      if (response.data.error) {
        throw new Error(response.data.error);
      }
      
      setMlnsupportData(response.data.mlnsupport);
      setMcportData(response.data.mcport);
      
      setSnackbar({
        open: true,
        message: 'Dados processados com sucesso!',
        severity: 'success'
      });
    } catch (error) {
      console.error('Error processing data:', error);
      setSnackbar({
        open: true,
        message: `Erro: ${error.message || 'Ocorreu um erro inesperado'}`,
        severity: 'error'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <Box sx={{ maxWidth: 600, margin: 'auto', padding: 2 }}>
      {Object.entries(params).map(([key, value]) => (
        <Tooltip key={key} title={paramDescriptions[key]} arrow placement="top-start">
          <TextField
            fullWidth
            margin="normal"
            name={key}
            label={key.replace('_', ' ').toUpperCase()}
            type="number"
            value={value}
            onChange={handleInputChange}
          />
        </Tooltip>
      ))}

      <StyledButton 
        variant="contained" 
        color="primary" 
        onClick={handleAprender}
        disabled={isLoading}
        fullWidth
      >
        {isLoading ? 'Processando...' : 'Aprender'}
      </StyledButton>

      {mlnsupportData.length > 0 && (
        <TableContainer component={Paper} sx={{ marginTop: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Ativo</TableCell>
                <TableCell>Frequência</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {mlnsupportData.map((row, index) => (
                <TableRow key={index}>
                  <TableCell>{row.ATIVO}</TableCell>
                  <TableCell>{row.FREQ}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {Object.keys(mcportData).length > 0 && (
        <TableContainer component={Paper} sx={{ marginTop: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Ativo</TableCell>
                <TableCell>Valor</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {Object.entries(mcportData).map(([key, value], index) => (
                <TableRow key={index}>
                  <TableCell>{key}</TableCell>
                  <TableCell>{value}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleSnackbarClose} severity={snackbar.severity} sx={{ width: '100%' }} variant="filled">
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}