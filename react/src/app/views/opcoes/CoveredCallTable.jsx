//src/app/views/opcoes/CoveredCallTable.jsx
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
  Modal,
  Paper,
  Typography,
  Fade,
  Backdrop,
  Button, // Added this import
  IconButton // Added this import since it's used in the modal
} from "@mui/material";
import ShowChartIcon from '@mui/icons-material/ShowChart';
import CloseIcon from '@mui/icons-material/Close';
import { fetchCoveredCalls } from "/src/__api__/db/apiService";
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

const CoveredCallTable = () => {
  const [coveredCallData, setCoveredCallData] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedMaturityRange, setSelectedMaturityRange] = useState('between_15_and_30_days');
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedCall, setSelectedCall] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await fetchCoveredCalls();
        setCoveredCallData(result);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const generatePayoffData = (call) => {
    if (!call) return [];
    
    const callStrike = call.strike;
    const spotPrice = call.spot_price;
    const callPremium = call.bid || call.close || 0;
    const pmResult = spotPrice - callPremium;

    // Determine price range for visualization
    const minPrice = spotPrice * 0.8;
    const maxPrice = spotPrice * 1.3;
    const step = (maxPrice - minPrice) / 100;

    return Array.from({ length: 101 }, (_, i) => {
      const price = minPrice + (i * step);
      let payoff;
      
      if (price <= callStrike) {
        // Below call strike: keep premium + stock appreciation
        payoff = callPremium + (price - spotPrice);
      } else {
        // Above call strike: max gain (strike - spot + premium)
        payoff = callStrike - spotPrice + callPremium;
      }
      
      return {
        price: Number(price.toFixed(2)),
        payoff: Number(payoff.toFixed(2))
      };
    });
  };

  const handleMaturityRangeChange = (event) => {
    setSelectedMaturityRange(event.target.value);
  };

  const handleOpenModal = (call) => {
    setSelectedCall(call);
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  if (loading) {
    return <CircularProgress />;
  }

  const selectedData = coveredCallData[selectedMaturityRange] || [];

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
              <StyledTableCell>Ação</StyledTableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {selectedData.map((call) => (
              <StyledTableRow key={call.symbol}>
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
                <TableCell>
                  <Tooltip title="Visualizar gráfico de payoff">
                    <PlotButton
                      variant="contained"
                      size="small"
                      onClick={() => handleOpenModal(call)}
                    >
                      <ShowChartIcon fontSize="small" />
                    </PlotButton>
                  </Tooltip>
                </TableCell>
              </StyledTableRow>
            ))}
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
                Payoff Structure: {selectedCall?.parent_symbol} (Covered Call)
              </Typography>
              <IconButton onClick={handleCloseModal} size="small">
                <CloseIcon />
              </IconButton>
            </Box>

            {selectedCall && (
              <Box sx={{ height: 400 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={generatePayoffData(selectedCall)}
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
                      x={selectedCall.spot_price}
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
                      x={selectedCall.strike}
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
                    
                    {/* Breakeven point */}
                    <ReferenceLine
                      x={selectedCall.spot_price - (selectedCall.bid || selectedCall.close || 0)}
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
                      y={selectedCall.strike - selectedCall.spot_price + (selectedCall.bid || selectedCall.close || 0)}
                      stroke="green"
                      strokeDasharray="3 3"
                      label={{
                        value: `Max Gain: R$ ${(selectedCall.strike - selectedCall.spot_price + (selectedCall.bid || selectedCall.close || 0)).toFixed(2)}`,
                        position: 'right',
                        fill: 'green',
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

            {selectedCall && (
              <Box mt={2}>
                <Typography variant="subtitle1" gutterBottom>
                  Detalhes da Estratégia Covered Call
                </Typography>
                
                <Box display="flex" flexWrap="wrap" gap={2}>
                  <Box flex="1" minWidth="200px">
                    <Typography variant="body2">
                      <strong>Ativo:</strong> {selectedCall.parent_symbol}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Preço Atual:</strong> R$ {selectedCall.spot_price?.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Vencimento:</strong> {selectedCall.due_date} ({selectedCall.days_to_maturity} dias)
                    </Typography>
                  </Box>
                  
                  <Box flex="1" minWidth="200px">
                    <Typography variant="body2">
                      <strong>Call (venda):</strong> {selectedCall.symbol} @ R$ {selectedCall.strike?.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Prêmio recebido:</strong> R$ {(selectedCall.bid || selectedCall.close)?.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Ponto de Equilíbrio (BE):</strong> R$ {(selectedCall.spot_price - (selectedCall.bid || selectedCall.close || 0)).toFixed(2)}
                    </Typography>
                  </Box>
                  
                  <Box flex="1" minWidth="200px">
                    <Typography variant="body2">
                      <strong>Ganho Máximo:</strong> R$ {(selectedCall.strike - selectedCall.spot_price + (selectedCall.bid || selectedCall.close || 0)).toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Proteção:</strong> {(selectedCall.protection * 100).toFixed(2)}%
                    </Typography>
                    <Typography variant="body2">
                      <strong>Taxa Embarcada:</strong> {(selectedCall.embedded_interest * 100).toFixed(2)}%
                    </Typography>
                    <Typography variant="body2">
                      <strong>Retorno Anualizado:</strong> {(selectedCall.annual_return * 100).toFixed(2)}%
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

export default CoveredCallTable;