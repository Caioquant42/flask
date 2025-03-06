import React, { useState, useEffect } from "react";
import {
  Box,
  Table,
  styled,
  TableRow,
  TableBody,
  TableCell,
  TableHead,
  TableContainer,
  Tooltip,
  CircularProgress,
  RadioGroup,
  FormControlLabel,
  Radio,
  FormControl,
  FormLabel,
  TablePagination,
  TableSortLabel,
  Collapse,
  IconButton,
} from "@mui/material";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { fetchCOLLAR30View, fetchCOLLAR60View, fetchCOLLARABOVE60View } from "/src/__api__/db/apiService";


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

const OptionsTable = () => {
  const [data30, setData30] = useState([]);
  const [data60, setData60] = useState([]);
  const [dataAbove60, setDataAbove60] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedRows, setExpandedRows] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [result30, result60, resultAbove60] = await Promise.all([
          fetchCOLLAR30View(),
          fetchCOLLAR60View(),
          fetchCOLLARABOVE60View(),
        ]);
        setData30(result30.slice(0, 20));
        setData60(result60.slice(0, 20));
        setDataAbove60(resultAbove60.slice(0, 20));
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleExpandRow = (symbol) => {
    setExpandedRows((prev) => ({ ...prev, [symbol]: !prev[symbol] }));
  };

  const renderCallRow = (call) => (
    <React.Fragment key={call.symbol}>
      <StyledTableRow>
        <TableCell>
          <IconButton size="small" onClick={() => handleExpandRow(call.symbol)}>
            {expandedRows[call.symbol] ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
        <TableCell>{call.symbol}</TableCell>
        <TableCell>{call.parent_symbol}</TableCell>
        <TableCell>{call.spot_price}</TableCell>
        <TableCell>{call.category}</TableCell>
        <TableCell>{call.due_date}</TableCell>
        <TableCell>{call.days_to_maturity}</TableCell>
        <TableCell>{call.strike?.toFixed(2) ?? 'N/A'}</TableCell>
        <TableCell>{call.bid?.toFixed(2) ?? 'N/A'}</TableCell>
        <TableCell>{call.ask?.toFixed(2) ?? 'N/A'}</TableCell>
        <TableCell>{call.bid_volume ?? 'N/A'}</TableCell>
        <TableCell>{call.ask_volume ?? 'N/A'}</TableCell>
        <TableCell>{call.intrinsic_value?.toFixed(4) ?? 'N/A'}</TableCell>
        <TableCell>{call.extrinsic_value?.toFixed(4) ?? 'N/A'}</TableCell>
        <TableCell>{call.pm?.toFixed(2) ?? 'N/A'}</TableCell>
        <TableCell>{call.protection?.toFixed(4) ?? 'N/A'}</TableCell>
        <TableCell>{call.embedded_interest?.toFixed(4) ?? 'N/A'}</TableCell>
        <TableCell>{call.annual_return?.toFixed(4) ?? 'N/A'}</TableCell>
      </StyledTableRow>
      <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={16}>
          <Collapse in={expandedRows[call.symbol]} timeout="auto" unmountOnExit>
            <Box margin={1}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <StyledTableCell>Symbol</StyledTableCell>
                    <StyledTableCell>Strike</StyledTableCell>
                    <StyledTableCell>Close</StyledTableCell>
                    <StyledTableCell>Bid</StyledTableCell>
                    <StyledTableCell>Ask</StyledTableCell>
                    <StyledTableCell>Bid Volume</StyledTableCell>
                    <StyledTableCell>Ask Volume</StyledTableCell>
                    <StyledTableCell>Extrinsic Value</StyledTableCell>
                    <StyledTableCell>Embedded Interest</StyledTableCell>
                    <StyledTableCell>Annual Return</StyledTableCell>
                    <StyledTableCell>PM Result</StyledTableCell>
                    <StyledTableCell>Total Gain</StyledTableCell>
                    <StyledTableCell>Total Risk</StyledTableCell>
                    <StyledTableCell>Gain to Risk Ratio</StyledTableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {call.puts.map((put) => (
                    <StyledTableRow key={put.symbol}>
                      <TableCell>{put.symbol}</TableCell>
                      <TableCell>{put.strike?.toFixed(2) ?? 'N/A'}</TableCell>
                      <TableCell>{put.close?.toFixed(2) ?? 'N/A'}</TableCell>
                      <TableCell>{put.bid?.toFixed(2) ?? 'N/A'}</TableCell>
                      <TableCell>{put.ask?.toFixed(2) ?? 'N/A'}</TableCell>
                      <TableCell>{put.bid_volume ?? 'N/A'}</TableCell>
                      <TableCell>{put.ask_volume ?? 'N/A'}</TableCell>
                      <TableCell>{put.extrinsic_value_result?.toFixed(4) ?? 'N/A'}</TableCell>
                      <TableCell>{put.embedded_interest_result?.toFixed(4) ?? 'N/A'}</TableCell>
                      <TableCell>{put.annual_return_result?.toFixed(4) ?? 'N/A'}</TableCell>
                      <TableCell>{put.pm_result?.toFixed(4) ?? 'N/A'}</TableCell>
                      <TableCell>{put.total_gain?.toFixed(4) ?? 'N/A'}</TableCell>
                      <TableCell>{put.total_risk?.toFixed(4) ?? 'N/A'}</TableCell>
                      <TableCell>{put.gain_to_risk_ratio?.toFixed(4) ?? 'N/A'}</TableCell>
                    </StyledTableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </React.Fragment>
  );

  const renderTable = (data, title) => (
    <Box mb={4}>
      <h2>{title}</h2>
      <StyledTableContainer>
        <StyledTable>
          <TableHead>
            <TableRow>
              <StyledTableCell />
              <StyledTableCell>Symbol</StyledTableCell>
              <StyledTableCell>Parent Symbol</StyledTableCell>
              <StyledTableCell>Spot Price</StyledTableCell>
              <StyledTableCell>Category</StyledTableCell>
              <StyledTableCell>Due Date</StyledTableCell>
              <StyledTableCell>Days to Maturity</StyledTableCell>
              <StyledTableCell>Strike</StyledTableCell>
              <StyledTableCell>Bid</StyledTableCell>
              <StyledTableCell>Ask</StyledTableCell>
              <StyledTableCell>Bid Volume</StyledTableCell>
              <StyledTableCell>Ask Volume</StyledTableCell>
              <StyledTableCell>Intrinsic Value</StyledTableCell>
              <StyledTableCell>Extrinsic Value</StyledTableCell>
              <StyledTableCell>PM</StyledTableCell>
              <StyledTableCell>Protection</StyledTableCell>
              <StyledTableCell>Embedded Interest</StyledTableCell>
              <StyledTableCell>Annual Return</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((call) => renderCallRow(call))}
          </TableBody>
        </StyledTable>
      </StyledTableContainer>
    </Box>
  );

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      {renderTable(data30, "Options < 30 days")}
      {renderTable(data60, "Options 30-60 days")}
      {renderTable(dataAbove60, "Options > 60 days")}
    </Box>
  );
};

export default OptionsTable;