// FrequencyPage.jsx
import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';
import QuantPortForm from './QuantPortForm';

const paramDescriptions = {
  nret_mln: "Número de retornos para a função mlnsupport",
  nclusters: "Número de clusters para a função mlnsupport",
  period_ret: "Período de retornos para ambas as funções",
  ret_mc: "Limiar de retorno para a função mcport",
  n_sim_mc: "Número de simulações para a função mcport",
  tam_port: "Tamanho do portfólio para a função mcport"
};

export default function FrequencyPage() {
  return (
    <Container maxWidth="md">
      <Typography variant="h4" component="h1" gutterBottom>
        Análise de Frequência
      </Typography>
      
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Sobre esta Aplicação
        </Typography>
        <Typography paragraph>
          Esta aplicação realiza uma análise quantitativa de portfólio utilizando técnicas de aprendizado de máquina e simulação de Monte Carlo. Ela combina duas abordagens principais:
        </Typography>
        <Typography paragraph>
          1. <strong>MLN Support (Machine Learning Network Support):</strong> Utiliza clustering para identificar padrões nos retornos dos ativos e determinar quais têm maior probabilidade de superar o mercado.
        </Typography>
        <Typography paragraph>
          2. <strong>Monte Carlo Port:</strong> Simula múltiplos cenários de portfólio para otimizar a alocação de ativos com base em critérios de risco e retorno.
        </Typography>
        <Typography paragraph>
          O resultado é uma análise que combina a robustez do aprendizado de máquina com a flexibilidade das simulações de Monte Carlo para fornecer insights valiosos sobre a composição ideal do portfólio.
        </Typography>
      </Paper>

      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Parâmetros
        </Typography>
        {Object.entries(paramDescriptions).map(([key, description]) => (
          <Box key={key} sx={{ mb: 2 }}>
            <Typography variant="subtitle1" component="h3">
              {key.replace('_', ' ').toUpperCase()}
            </Typography>
            <Typography variant="body2">{description}</Typography>
          </Box>
        ))}
      </Paper>

      <QuantPortForm />
    </Container>
  );
}