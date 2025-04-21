import React from 'react';
import { Box, Typography, Paper, Container } from '@mui/material';
import CoveredCallTable from './CoveredCallTable'; // We'll assume this is the component you created earlier

const CoveredCallPage = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Covered Call Strategy Options
        </Typography>
        <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
          <Typography variant="h6" gutterBottom>
            Market Overview
          </Typography>
          <Typography variant="body1" paragraph>
            This page displays the best covered call opportunities across different time frames.
            Covered calls provide income through premium collection while offering some downside protection.
          </Typography>
          <Typography variant="body2" paragraph sx={{ fontStyle: 'italic' }}>
            Key metrics shown include annualized return, protection level, and premium received.
          </Typography>
          <CoveredCallTable />
        </Paper>
      </Box>
    </Container>
  );
};

export default CoveredCallPage;