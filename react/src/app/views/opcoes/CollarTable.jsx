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
    backgroundColor: 'rgba(128, 0, 128, 0.1)',
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
    const callPremium = call.bid || call.close || 0;
    const putPremium = put.ask || put.close || 0;
    const netPremium = callPremium - putPremium;
    const pmResult = spotPrice - callPremium + putPremium;

    // Calculate break-even point
    const breakEven = pmResult;
    
    // Calculate max gain and max loss
    const maxGain = callStrike - pmResult;
    const maxLoss = putStrike - pmResult;

    // Determine price range for visualization
    const minPrice = Math.min(putStrike, spotPrice * 0.8);
    const maxPrice = Math.max(callStrike, spotPrice * 1.2);
    const step = (maxPrice - minPrice) / 100;

    return Array.from({ length: 101 }, (_, i) => {
      const price = minPrice + (i * step);
      let payoff;
      
      if (price <= putStrike) {
        // Below put strike: maximum loss
        payoff = maxLoss;
      } else if (price >= callStrike) {
        // Above call strike: maximum gain
        payoff = maxGain;
      } else {
        // Between strikes: linear payoff
        payoff = price - pmResult;
      }
      
      return {
        price: Number(price.toFixed(2)),
        payoff: Number(payoff.toFixed(2))
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
                        <TableCell>{put.pm_result?.toFixed(2) ?? 'N/A'}</TableCell>
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
                Payoff Structure: {selectedStrategy?.call?.parent_symbol} (Collar)
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
                      label={{ value: 'Stock Price (R$)', position: 'insideBottomRight', offset: -10 }}
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
                    
                    {/* Current spot price */}
                    <ReferenceLine
                      x={selectedStrategy.call.spot_price}
                      stroke="green"
                      strokeWidth={2}
                      label={{ 
                        value: 'Spot', 
                        position: 'top',
                        fill: 'green',
                        fontSize: 12,
                        fontWeight: 'bold'
                      }}
                    />
                    
                    {/* Call strike */}
                    <ReferenceLine
                      x={selectedStrategy.call.strike}
                      stroke="blue"
                      strokeWidth={1.5}
                      strokeDasharray="5 5"
                      label={{ 
                        value: 'Call Strike', 
                        position: 'top',
                        fill: 'blue',
                        fontSize: 12
                      }}
                    />
                    
                    {/* Put strike */}
                    <ReferenceLine
                      x={selectedStrategy.put.strike}
                      stroke="red"
                      strokeWidth={1.5}
                      strokeDasharray="5 5"
                      label={{ 
                        value: 'Put Strike', 
                        position: 'top',
                        fill: 'red',
                        fontSize: 12
                      }}
                    />
                    
                    {/* Breakeven point */}
                    <ReferenceLine
                      x={selectedStrategy.put.pm_result}
                      stroke="purple"
                      strokeWidth={1.5}
                      strokeDasharray="3 3"
                      label={{ 
                        value: 'BE', 
                        position: 'top',
                        fill: 'purple',
                        fontSize: 12
                      }}
                    />
                    
                    {/* Maximum gain line */}
                    <ReferenceLine
                      y={selectedStrategy.put.total_gain}
                      stroke="green"
                      strokeDasharray="3 3"
                      label={{
                        value: `Max Gain: R$ ${selectedStrategy.put.total_gain?.toFixed(2)}`,
                        position: 'right',
                        fill: 'green',
                        fontSize: 12
                      }}
                    />
                    
                    {/* Maximum loss line */}
                    <ReferenceLine
                      y={selectedStrategy.put.total_risk}
                      stroke="red"
                      strokeDasharray="3 3"
                      label={{
                        value: `Max Loss: R$ ${selectedStrategy.put.total_risk?.toFixed(2)}`,
                        position: 'right',
                        fill: 'red',
                        fontSize: 12
                      }}
                    />
                    
                    {/* Payoff line */}
                    <Line
                      type="monotone"
                      dataKey="payoff"
                      stroke="#8884d8"
                      strokeWidth={3}
                      dot={false}
                      activeDot={{ r: 8 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            )}

            {selectedStrategy && (
              <Box mt={2}>
                <Typography variant="subtitle1" gutterBottom>
                  Detalhes da Estratégia Collar
                </Typography>
                
                <Box display="flex" flexWrap="wrap" gap={2}>
                  <Box flex="1" minWidth="200px">
                    <Typography variant="body2">
                      <strong>Ativo:</strong> {selectedStrategy.call.parent_symbol}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Preço Atual:</strong> R$ {selectedStrategy.call.spot_price?.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Vencimento:</strong> {selectedStrategy.call.due_date} ({selectedStrategy.call.days_to_maturity} dias)
                    </Typography>
                  </Box>
                  
                  <Box flex="1" minWidth="200px">
                    <Typography variant="body2">
                      <strong>Call (venda):</strong> {selectedStrategy.call.symbol} @ R$ {selectedStrategy.call.strike?.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Prêmio recebido:</strong> R$ {(selectedStrategy.call.bid || selectedStrategy.call.close)?.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Put (compra):</strong> {selectedStrategy.put.symbol} @ R$ {selectedStrategy.put.strike?.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Prêmio pago:</strong> R$ {(selectedStrategy.put.ask || selectedStrategy.put.close)?.toFixed(2)}
                    </Typography>
                  </Box>
                  
                  <Box flex="1" minWidth="200px">
                    <Typography variant="body2">
                      <strong>Prêmio Líquido:</strong> R$ {((selectedStrategy.call.bid || selectedStrategy.call.close || 0) - (selectedStrategy.put.ask || selectedStrategy.put.close || 0))?.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Ganho Máximo:</strong> R$ {selectedStrategy.put.total_gain?.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Risco Máximo:</strong> R$ {selectedStrategy.put.total_risk?.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Relação Ganho/Risco:</strong> {selectedStrategy.put.gain_to_risk_ratio?.toFixed(4) || 'N/A'}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Ponto de Equilíbrio (BE):</strong> R$ {selectedStrategy.put.pm_result?.toFixed(2)}
                    </Typography>
                  </Box>
                </Box>
              </Box>
            )}
          </ModalContent>
        </Fade>
      </Modal>
    </Box>
  );
};

export default ITMCollarTable;