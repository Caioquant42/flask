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
import { fetchITMCOLLARView } from "/src/__api__/db/apiService";


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

const GlowingStyledTableRow = styled(StyledTableRow)(({ theme, isHighest }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  ...(isHighest && {
    animation: `$glowing 1.5s infinite alternate`,
    backgroundColor: 'rgba(128, 0, 128, 0.1)', // Light purple background
  }),
  '@keyframes glowing': {
    '0%': { boxShadow: '0 0 5px #800080' },
    '100%': { boxShadow: '0 0 20px #800080' },
  },
}));
const ITMCollarTable = () => {
  const [collarData, setCollarData] = useState({});
  const [loading, setLoading] = useState(true);
  const [expandedRows, setExpandedRows] = useState({});
  const [selectedMaturityRange, setSelectedMaturityRange] = useState('between_15_and_30_days');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await fetchITMCOLLARView();
        setCollarData(result.intrinsic);
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

  const handleMaturityRangeChange = (event) => {
    setSelectedMaturityRange(event.target.value);
  };

  const renderCallRow = (call) => {
    const highestPut = call.puts.reduce((max, put) => 
      (put.gain_to_risk_ratio > (max?.gain_to_risk_ratio || -Infinity) ? put : max), null);

    return (
      <React.Fragment key={call.symbol}>
        <StyledTableRow>
          <TableCell>
            <IconButton size="small" onClick={() => handleExpandRow(call.symbol)}>
              {expandedRows[call.symbol] ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
            </IconButton>
          </TableCell>
          <TableCell>{call.parent_symbol}</TableCell>
          <TableCell>{call.symbol}</TableCell>
          <TableCell>{call.strike?.toFixed(2) ?? 'N/A'}</TableCell>
          <TableCell>{call.category}</TableCell>
          <TableCell>{call.due_date}</TableCell>
          <TableCell>{call.days_to_maturity}</TableCell>
          <TableCell>{call.spot_price}</TableCell>
          <TableCell>{call.close?.toFixed(2) ?? 'N/A'}</TableCell>
          <TableCell>{call.bid?.toFixed(2) ?? 'N/A'}</TableCell>
          <TableCell>{call.ask?.toFixed(2) ?? 'N/A'}</TableCell>
          <TableCell>{call.bid_volume ?? 'N/A'}</TableCell>
          <TableCell>{call.ask_volume ?? 'N/A'}</TableCell>
          <TableCell>{call.intrinsic_value?.toFixed(2) ?? 'N/A'}</TableCell>
          <TableCell>{call.extrinsic_value?.toFixed(2) ?? 'N/A'}</TableCell>
          <TableCell>{call.pm?.toFixed(2) ?? 'N/A'}</TableCell>
          <TableCell>{(call.protection * 100).toFixed(2)}%</TableCell>
          <TableCell>{(call.embedded_interest * 100).toFixed(2)}%</TableCell>
          <TableCell>{(call.annual_return * 100).toFixed(2)}%</TableCell>
        </StyledTableRow>
        <TableRow>
          <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={19}>
            <Collapse in={expandedRows[call.symbol]} timeout="auto" unmountOnExit>
              <Box margin={1}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <StyledTableCell>Opção</StyledTableCell>
                      <StyledTableCell>Strike</StyledTableCell>
                      <StyledTableCell>Close</StyledTableCell>
                      <StyledTableCell>Bid</StyledTableCell>
                      <StyledTableCell>Ask</StyledTableCell>
                      <StyledTableCell>Bid Volume</StyledTableCell>
                      <StyledTableCell>Ask Volume</StyledTableCell>
                      <StyledTableCell>VE</StyledTableCell>
                      <StyledTableCell>Taxa</StyledTableCell>
                      <StyledTableCell>Retorno Anual</StyledTableCell>
                      <StyledTableCell>PM Final</StyledTableCell>
                      <StyledTableCell>Ganho(R$)</StyledTableCell>
                      <StyledTableCell>Risco(R$)</StyledTableCell>
                      <StyledTableCell>G/R</StyledTableCell>
                      <StyledTableCell>spot_to_call_strike</StyledTableCell>
                      <StyledTableCell>spot_to_put_strike</StyledTableCell>
                      <StyledTableCell>spot_to_pm</StyledTableCell>
                      <StyledTableCell>BE</StyledTableCell>
                      <StyledTableCell>pm_to_profit</StyledTableCell>
                      <StyledTableCell>pm_to_loss</StyledTableCell>
                      <StyledTableCell>score</StyledTableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {call.puts.map((put) => (
                      <GlowingStyledTableRow 
                        key={put.symbol} 
                        isHighest={put === highestPut}
                      >
                        <TableCell>{put.symbol}</TableCell>
                        <TableCell>{put.strike?.toFixed(2) ?? 'N/A'}</TableCell>
                        <TableCell>{put.close?.toFixed(2) ?? 'N/A'}</TableCell>
                        <TableCell>{put.bid?.toFixed(2) ?? 'N/A'}</TableCell>
                        <TableCell>{put.ask?.toFixed(2) ?? 'N/A'}</TableCell>
                        <TableCell>{put.bid_volume ?? 'N/A'}</TableCell>
                        <TableCell>{put.ask_volume ?? 'N/A'}</TableCell>
                        <TableCell>{put.extrinsic_value_result?.toFixed(4) ?? 'N/A'}</TableCell>
                        <TableCell>{(put.embedded_interest_result * 100).toFixed(2)}%</TableCell>
                        <TableCell>{(put.annual_return_result * 100).toFixed(2)}%</TableCell>
                        <TableCell>{put.pm_result?.toFixed(2) ?? 'N/A'}</TableCell>
                        <TableCell>{put.total_gain?.toFixed(2) ?? 'N/A'}</TableCell>
                        <TableCell>{put.total_risk?.toFixed(2) ?? 'N/A'}</TableCell>
                        <TableCell>{put.gain_to_risk_ratio?.toFixed(4) ?? 'no risk'}</TableCell>
                        <TableCell>{(put.spot_variation_to_max_return * 100).toFixed(2)}%</TableCell>
                        <TableCell>{(put.spot_variation_to_stoploss * 100).toFixed(2)}%</TableCell>
                        <TableCell>{(put.spot_variation_to_pm_result * 100).toFixed(2)}%</TableCell>
                        <TableCell>{((1 + put.spot_variation_to_pm_result) * call.spot_price).toFixed(2)}</TableCell>
                        <TableCell>{(put.pm_distance_to_profit * 100).toFixed(2)}%</TableCell>
                        <TableCell>{(put.pm_distance_to_loss * 100).toFixed(2)}%</TableCell>
                        <TableCell>{put.combined_score?.toFixed(4) ?? 'N/A'}</TableCell>
                      </GlowingStyledTableRow>
                    ))}
                  </TableBody>
                </Table>
              </Box>
            </Collapse>
          </TableCell>
        </TableRow>
      </React.Fragment>
    );
  };

  if (loading) {
    return <CircularProgress />;
  }

  const selectedData = collarData[selectedMaturityRange] || [];

  return (
    <Box>
      <FormControl component="fieldset" sx={{ mb: 2 }}>
        <FormLabel component="legend">Select Maturity Range</FormLabel>
        <RadioGroup
          row
          aria-label="maturity-range"
          name="maturity-range"
          value={selectedMaturityRange}
          onChange={handleMaturityRangeChange}
        >
          <FormControlLabel value="less_than_14_days" control={<Radio />} label="<= 14 days" />
          <FormControlLabel value="between_15_and_30_days" control={<Radio />} label="15-30 days" />
          <FormControlLabel value="between_30_and_60_days" control={<Radio />} label="31-60 days" />
          <FormControlLabel value="more_than_60_days" control={<Radio />} label="> 60 days" />
        </RadioGroup>
      </FormControl>

      <StyledTableContainer>
        <StyledTable>
          <TableHead>
            <TableRow>
              <StyledTableCell />
              <StyledTableCell>Ativo</StyledTableCell>
              <StyledTableCell>Opção</StyledTableCell>              
              <StyledTableCell>Strike</StyledTableCell>
              <StyledTableCell>Tipo</StyledTableCell>
              <StyledTableCell>Venc.</StyledTableCell>
              <StyledTableCell>Dias até Venc.</StyledTableCell>
              <StyledTableCell>À vista</StyledTableCell>              
              <StyledTableCell>Close</StyledTableCell>
              <StyledTableCell>Bid</StyledTableCell>
              <StyledTableCell>Ask</StyledTableCell>
              <StyledTableCell>Bid Volume</StyledTableCell>
              <StyledTableCell>Ask Volume</StyledTableCell>
              <StyledTableCell>VI</StyledTableCell>
              <StyledTableCell>VE</StyledTableCell>
              <StyledTableCell>PM</StyledTableCell>
              <StyledTableCell>Defesa</StyledTableCell>
              <StyledTableCell>Taxa</StyledTableCell>
              <StyledTableCell>Retorno Anual</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {selectedData.map((call) => renderCallRow(call))}
          </TableBody>
        </StyledTable>
      </StyledTableContainer>
    </Box>
  );
};

export default ITMCollarTable;