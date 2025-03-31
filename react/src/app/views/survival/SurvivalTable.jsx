import React, { useState, useEffect } from "react";
import {
  Box,
  Table,
  TableRow,
  TableBody,
  TableCell,
  TableHead,
  TableContainer,
  CircularProgress,
  RadioGroup,
  FormControlLabel,
  Radio,
  FormControl,
  FormLabel,
  TablePagination,
  Paper,
  Typography,
} from "@mui/material";
import { fetchSurvivalAnalysis } from "/src/__api__/db/apiService";

const SurvivalTable = () => {
  const [survivalData, setSurvivalData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedThreshold, setSelectedThreshold] = useState('-0.03');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await fetchSurvivalAnalysis();
        console.log("Fetched survival data:", data);
        setSurvivalData(data);
        setLoading(false);
      } catch (error) {
        console.error("Failed to fetch survival data:", error);
        setError("Failed to load data. Please try again later.");
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleThresholdChange = (event) => {
    setSelectedThreshold(event.target.value);
    setPage(0);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const formatValue = (value, decimals = 2, isPercentage = false) => {
    if (value === undefined || isNaN(value)) return 'N/A';
    const formattedValue = Number(value).toFixed(decimals);
    return isPercentage ? `${formattedValue}%` : formattedValue;
  };

  const filteredData = Object.entries(survivalData).map(([ticker, data]) => {
    const thresholdData = data[selectedThreshold];
    if (thresholdData) {
      return {
        ticker,
        ...thresholdData
      };
    }
    return null;
  }).filter(Boolean);

  console.log("filteredData:", filteredData);

  const paginatedData = filteredData.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

  console.log("paginatedData:", paginatedData);

  if (loading) {
    return <Box display="flex" justifyContent="center"><CircularProgress /></Box>;
  }

  if (error) {
    return <Box color="error.main">{error}</Box>;
  }

  return (
    <Box>
      <FormControl component="fieldset" sx={{ mb: 2 }}>
        <FormLabel component="legend">Select Threshold</FormLabel>
        <RadioGroup
          row
          aria-label="threshold"
          name="threshold"
          value={selectedThreshold}
          onChange={handleThresholdChange}
        >
          <FormControlLabel value="-0.03" control={<Radio />} label="-3%" />
          <FormControlLabel value="-0.05" control={<Radio />} label="-5%" />
          <FormControlLabel value="-0.07" control={<Radio />} label="-7%" />
        </RadioGroup>
      </FormControl>

      {filteredData.length === 0 ? (
        <Typography>No data available for the selected threshold.</Typography>
      ) : (
        <>
          <TableContainer component={Paper}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Ticker</TableCell>
                  <TableCell align="right">Days Since Last Incident</TableCell>
                  <TableCell align="right">Tail Index</TableCell>
                  <TableCell align="right">Survival Probability</TableCell>
                  <TableCell align="right">Hazard Rate</TableCell>
                  <TableCell align="right">Cumulative Hazard</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {paginatedData.map((data) => (
                  <TableRow key={data.ticker}>
                    <TableCell component="th" scope="row">{data.ticker}</TableCell>
                    <TableCell align="right">{data.days_since_last_incident}</TableCell>
                    <TableCell align="right">{formatValue(data.tail_index, 4)}</TableCell>
                    <TableCell align="right">{formatValue(data.current_survival_probability * 100, 1, true)}</TableCell>
                    <TableCell align="right">{formatValue(data.current_hazard_rate * 100, 1, true)}</TableCell>
                    <TableCell align="right">{formatValue(data.current_cumulative_hazard, 4)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={filteredData.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </>
      )}
    </Box>
  );
};

export default SurvivalTable;