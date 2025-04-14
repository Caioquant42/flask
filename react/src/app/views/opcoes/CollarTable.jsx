//src/app/views/opcoes/CollarTable.jsx
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
  Collapse,
  IconButton,
  Button,
  Modal,
  Paper,
  Typography,
  Fade,
  Backdrop
} from "@mui/material";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import CloseIcon from '@mui/icons-material/Close';
import { fetchITMCOLLARView } from "/src/__api__/db/apiService";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ReferenceLine, ResponsiveContainer } from 'recharts';


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

const PlotButton = styled(Button)(({ theme }) => ({
  minWidth: '40px',
  padding: '2px 8px',
  fontSize: '0.65rem',
  marginLeft: '4px',
  backgroundColor: theme.palette.info.main,
  color: theme.palette.common.white,
  '&:hover': {
    backgroundColor: theme.palette.info.dark,
  },
}));

const ModalContent = styled(Paper)(({ theme }) => ({
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '80%',
  maxWidth: 800,
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[24],
  padding: theme.spacing(3),
  borderRadius: theme.shape.borderRadius,
  outline: 'none',
}));

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
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedStrategy, setSelectedStrategy] = useState(null);


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

  const generatePayoffData = (call, put) => {
    if (!call || !put) return [];
    
    const callStrike = call.strike;
    const putStrike = put.strike;
    const spotPrice = call.spot_price;
    const callPremium = call.bid || 0;
    const putPremium = put.ask || 0;
    const netPremium = callPremium - putPremium;

    const minPrice = Math.min(putStrike * 0.9, spotPrice * 0.9);
    const maxPrice = Math.max(callStrike * 1.1, spotPrice * 1.1);
    const step = (maxPrice - minPrice) / 50;

    return Array.from({ length: 50 }, (_, i) => {
      const price = minPrice + (i * step);
      const callPayoff = price > callStrike ? -(price - callStrike) : 0;
      const putPayoff = price < putStrike ? (putStrike - price) : 0;
      const totalPayoff = callPayoff + putPayoff + netPremium;
      
      return {
        price: Number(price.toFixed(2)),
        payoff: Number(totalPayoff.toFixed(2))
      };
    });
  };

  const handleExpandRow = (symbol) => {
    setExpandedRows((prev) => ({ ...prev, [symbol]: !prev[symbol] }));
  };

  const handleMaturityRangeChange = (event) => {
    setSelectedMaturityRange(event.target.value);
  };

  const handleOpenModal = (call, put) => {
    setSelectedStrategy({ call, put });
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
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
                      <StyledTableCell>Ação</StyledTableCell>
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
                        <TableCell>
                          <Tooltip title="Visualizar gráfico de payoff">
                            <PlotButton
                              variant="contained"
                              size="small"
                              onClick={() => handleOpenModal(call, put)}
                            >
                              <ShowChartIcon fontSize="small" />
                            </PlotButton>
                          </Tooltip>
                        </TableCell>
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

      <Modal
        open={modalOpen}
        onClose={handleCloseModal}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{ timeout: 500 }}
      >
        <Fade in={modalOpen}>
          <ModalContent>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6">
                Payoff Structure: {selectedStrategy?.call?.parent_symbol}
              </Typography>
              <IconButton onClick={handleCloseModal} size="small">
                <CloseIcon />
              </IconButton>
            </Box>

            {selectedStrategy && (
              <Box sx={{ height: 400 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={generatePayoffData(selectedStrategy.call, selectedStrategy.put)}
                    margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="price"
                      label={{ value: 'Stock Price', position: 'insideBottomRight', offset: -10 }}
                    />
                    <YAxis
                      label={{ value: 'Payoff (R$)', angle: -90, position: 'insideLeft' }}
                    />
                    <RechartsTooltip
                      formatter={(value) => [`${value} R$`, 'Payoff']}
                      labelFormatter={(label) => `Price: R$ ${label}`}
                    />
                    <Legend />
                    <ReferenceLine y={0} stroke="#000" strokeDasharray="3 3" />
                    <ReferenceLine
                      x={selectedStrategy.call.spot_price}
                      stroke="green"
                      label={{ value: 'Spot', position: 'top' }}
                    />
                    <ReferenceLine
                      x={selectedStrategy.call.strike}
                      stroke="blue"
                      label={{ value: 'Call Strike', position: 'top' }}
                    />
                    <ReferenceLine
                      x={selectedStrategy.put.strike}
                      stroke="red"
                      label={{ value: 'Put Strike', position: 'bottom' }}
                    />
                    <Line
                      type="monotone"
                      dataKey="payoff"
                      stroke="#8884d8"
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            )}

            {selectedStrategy && (
              <Box mt={2}>
                <Typography variant="body2">
                  <strong>Call Strike:</strong> R$ {selectedStrategy.call.strike?.toFixed(2)} | 
                  <strong> Put Strike:</strong> R$ {selectedStrategy.put.strike?.toFixed(2)} | 
                  <strong> Net Premium:</strong> R$ {((selectedStrategy.call.bid || 0) - (selectedStrategy.put.ask || 0))?.toFixed(2)}
                </Typography>
                <Typography variant="body2" mt={1}>
                  <strong>Call Premium (recebido):</strong> R$ {(selectedStrategy.call.bid || selectedStrategy.call.close)?.toFixed(2)} | 
                  <strong> Put Premium (pago):</strong> R$ {(selectedStrategy.put.ask || selectedStrategy.put.close)?.toFixed(2)}
                </Typography>
                <Typography variant="body2" mt={1}>
                  <strong>Ganho Máximo:</strong> R$ {selectedStrategy.put.total_gain?.toFixed(2)} | 
                  <strong> Risco Máximo:</strong> R$ {selectedStrategy.put.total_risk?.toFixed(2)} | 
                  <strong> G/R:</strong> {selectedStrategy.put.gain_to_risk_ratio?.toFixed(4) || 'N/A'}
                </Typography>
              </Box>
            )}
          </ModalContent>
        </Fade>
      </Modal>
    </Box>
  );
};

export default ITMCollarTable;