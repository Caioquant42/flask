import React from 'react';
import { Grid, Card, CardContent } from '@mui/material';
import MCplot from './MCplot';
import { styled } from '@mui/material/styles';

const ContentBox = styled('div')(({ theme }) => ({
  margin: '30px',
  [theme.breakpoints.down('sm')]: {
    margin: '16px',
  },
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  height: 'fit-content',
}));

const MCplotPage = ({ onDataReceived, isLoading, setIsLoading }) => {
  const handleDataReceived = (data) => {
    console.log('Data received in MCplotPage:', data);
    if (onDataReceived) {
      onDataReceived(data);
    }
  };

  return (
    <ContentBox>
      <Grid container spacing={3} justifyContent="left">
        <Grid item xs={12} sm={10} md={8}>
          <Card elevation={3}>
            <CardContent>
              <MCplot  
                onDataReceived={handleDataReceived}
                isLoading={isLoading}
                setIsLoading={setIsLoading}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </ContentBox>
  );
};

export default MCplotPage;