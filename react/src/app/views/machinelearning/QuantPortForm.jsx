// QuantPortForm.jsx
import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Snackbar,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tooltip
} from '@mui/material';
import { styled } from "@mui/material/styles";
import axios from 'axios';
import API_BASE_URL from "@/__api__/db/apiService";

const StyledButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(2, 0),
}));

// ---- table styling from AgendaTable.jsx ----
const StyledTableCell = styled(TableCell)(({ theme }) => ({
  fontWeight: 'bold',
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.common.white,
  padding: '6px 8px',
  fontSize: '0.75rem',
  textAlign: 'center',
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
}));

const StyledTableContainer = styled(TableContainer)({
  flexGrow: 1,
  maxHeight: 360,
  overflowY: 'auto',
});

const StyledTable = styled(Table)({
  minWidth: 'auto',
  "& .MuiTableCell-root": {
    padding: '4px 8px',
    fontSize: '0.7rem',
  },
});
// ---------------------------------------------

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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setParams(p => ({ ...p, [name]: parseInt(value, 10) }));
  };

  const handleAprender = async () => {
    setIsLoading(true);
    try {
      const resp = await axios.post(`${API_BASE_URL}/quant_port`, params);
      if (resp.data.error) throw new Error(resp.data.error);

      setMlnsupportData(resp.data.mlnsupport);
      setMcportData(resp.data.mcport);
      setSnackbar({ open: true, message: 'Dados processados com sucesso!', severity: 'success' });
    } catch (err) {
      console.error(err);
      setSnackbar({
        open: true,
        message: `Erro: ${err.message || 'Ocorreu um erro inesperado'}`,
        severity: 'error'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSnackbarClose = (_, reason) => {
    if (reason === 'clickaway') return;
    setSnackbar(s => ({ ...s, open: false }));
  };

  // sort port data descending
  const sortedMcportData = Object.entries(mcportData).sort(([, a], [, b]) => b - a);

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', p: 2 }}>
      {Object.entries(params).map(([key, val]) => (
        <Tooltip key={key} title={paramDescriptions[key]} arrow placement="top-start">
          <TextField
            fullWidth
            margin="normal"
            name={key}
            label={key.replace('_',' ').toUpperCase()}
            type="number"
            value={val}
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

      {/* MLN Support Table */}
      {mlnsupportData.length > 0 && (
        <StyledTableContainer component={Paper} sx={{ mt: 2 }}>
          <StyledTable size="small" aria-label="mlnsupport results">
            <TableHead>
              <TableRow>
                <StyledTableCell>Ativo</StyledTableCell>
                <StyledTableCell>Frequência</StyledTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {mlnsupportData.map((row, i) => (
                <StyledTableRow key={i}>
                  <TableCell align="center">{row.ATIVO}</TableCell>
                  <TableCell align="center">{row.FREQ}</TableCell>
                </StyledTableRow>
              ))}
            </TableBody>
          </StyledTable>
        </StyledTableContainer>
      )}

      {/* Monte Carlo Port Table */}
      {sortedMcportData.length > 0 && (
        <StyledTableContainer component={Paper} sx={{ mt: 2 }}>
          <StyledTable size="small" aria-label="mcport results">
            <TableHead>
              <TableRow>
                <StyledTableCell>Ativo</StyledTableCell>
                <StyledTableCell>Valor</StyledTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {sortedMcportData.map(([key, val], i) => (
                <StyledTableRow key={i}>
                  <TableCell align="center">{key}</TableCell>
                  <TableCell align="center">{val.toFixed(0)}</TableCell>
                </StyledTableRow>
              ))}
            </TableBody>
          </StyledTable>
        </StyledTableContainer>
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
          variant="filled"
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}