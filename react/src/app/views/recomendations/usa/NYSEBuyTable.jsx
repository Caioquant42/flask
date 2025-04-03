import React, { useState, useEffect } from "react";
import {
  Table,
  styled,
  TableRow,
  TableBody,
  TableCell,
  TableHead,
  TableContainer,
  Tooltip
} from "@mui/material";
import { fetchNYSEBuyAnalysis } from "/src/__api__/db/apiService";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  fontWeight: 'bold',
  backgroundColor: theme.palette.primary.main,
  color: theme.palette.common.white,
  padding: '6px 8px',
  fontSize: '0.75rem',
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
}));

const StyledTableContainer = styled(TableContainer)({
  flexGrow: 1,
  display: 'flex',
  flexDirection: 'column',
  maxHeight: '100%',
  overflowY: 'auto',
});

const StyledTable = styled(Table)({
  minWidth: 'auto',
  "& .MuiTableCell-root": {
    padding: '4px 8px',
    fontSize: '0.7rem',
  },
});

export default function NYSEBuyTable() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await fetchNYSEBuyAnalysis();
        if (result && Array.isArray(result)) {
          setData(result.slice(0, 10)); // Only take the first 10 items
        } else {
          console.error("Invalid data format received from API");
          setData([]); // Set empty array if data is invalid
        }
      } catch (error) {
        console.error("Error fetching NASDAQ Strong Buy analysis:", error);
        setData([]); // Set empty array on error
      }
    };
    fetchData();
  }, []);

  return (
    <StyledTableContainer>
      <StyledTable size="small" aria-label="nyse buy analysis table">
        <TableHead>
          <TableRow>
            <StyledTableCell>Ticker</StyledTableCell>
            <StyledTableCell align="right">
              <Tooltip title="Número total de analistas que cobrem este ativo">
                <span>Analistas</span>
              </Tooltip>
            </StyledTableCell>
            <StyledTableCell align="right">Preço</StyledTableCell>
            <StyledTableCell align="right">
              <Tooltip title="Retorno mínimo esperado em 12 meses">
                <span>Min Ret</span>
              </Tooltip>
            </StyledTableCell>
            <StyledTableCell align="right">
              <Tooltip title="Retorno médio esperado em 12 meses">
                <span>Med Ret</span>
              </Tooltip>
            </StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((item, index) => (
            <StyledTableRow key={index}>
              <TableCell>{item.ticker}</TableCell>
              <TableCell align="right">{item.numberOfAnalystOpinions}</TableCell>
              <TableCell align="right">${parseFloat(item.currentPrice).toFixed(2)}</TableCell>
              <TableCell align="right">{item['% Distance to Low'].toFixed(1)}%</TableCell>
              <TableCell align="right">{item['% Distance to Median'].toFixed(1)}%</TableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </StyledTable>
    </StyledTableContainer>
  );
}