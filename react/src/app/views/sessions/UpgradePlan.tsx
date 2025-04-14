// src/app/views/sessions/UpgradePlan.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Check } from 'lucide-react';
import styled from '@mui/material/styles/styled';
import useAuth from 'app/hooks/useAuth';

const Container = styled('div')({
  minHeight: '100vh',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: '#f9fafb',
  padding: '24px',
});

const Content = styled('div')({
  maxWidth: '1200px',
  width: '100%',
  textAlign: 'center',
});

const Title = styled('h2')({
  fontSize: '2rem',
  fontWeight: 'bold',
  color: '#1f2937',
});

const Subtitle = styled('p')({
  fontSize: '1.25rem',
  color: '#6b7280',
  marginBottom: '2rem',
});

const PlanGrid = styled('div')({
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
  gap: '1.5rem',
});

const PlanCard = styled('div')<{ highlighted?: boolean }>(({ highlighted }) => ({
  padding: '2rem',
  borderRadius: '1rem',
  backgroundColor: highlighted ? '#2563eb' : '#ffffff',
  color: highlighted ? '#ffffff' : '#1f2937',
  boxShadow: highlighted ? '0 10px 15px rgba(37, 99, 235, 0.2)' : '0 4px 6px rgba(0, 0, 0, 0.1)',
  transform: highlighted ? 'scale(1.05)' : 'scale(1)',
  transition: 'transform 0.3s ease',
}));

const PlanTitle = styled('h3')({
  fontSize: '1.5rem',
  fontWeight: 'bold',
});

const PlanPrice = styled('p')({
  fontSize: '2rem',
  fontWeight: 'bold',
  margin: '1rem 0',
});

const FeatureList = styled('ul')({
  listStyleType: 'none',
  padding: 0,
  margin: '1rem 0',
});

const FeatureItem = styled('li')({
  display: 'flex',
  alignItems: 'center',
  marginBottom: '0.5rem',
});

const FeatureText = styled('span')({
  marginLeft: '0.5rem',
  fontSize: '1rem',
});

const ActionButton = styled('button')<{ highlighted?: boolean }>(({ highlighted }) => ({
  marginTop: '1.5rem',
  padding: '0.75rem 1.5rem',
  borderRadius: '0.5rem',
  backgroundColor: highlighted ? '#ffffff' : '#2563eb',
  color: highlighted ? '#2563eb' : '#ffffff',
  fontWeight: 'bold',
  cursor: 'pointer',
  transition: 'background-color 0.3s ease',
  '&:hover': {
    backgroundColor: highlighted ? '#e5e7eb' : '#1d4ed8',
  },
}));

function UpgradePlan() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const plans = [
    {
      title: 'Free',
      price: 'R$0',
      features: ['Dashboard básico', 'Long & Short', 'Opções', 'Machine Learning'],
      role: 'FREE',
    },
    {
      title: 'Basic',
      price: 'R$29,90/mês',
      features: ['Todos os recursos Free', 'Portfólio', 'Fundamentos'],
      role: 'BASIC',
      highlighted: true,
    },
    {
      title: 'Pro',
      price: 'R$59,90/mês',
      features: ['Todos os recursos Basic', 'Recomendações', 'Screener'],
      role: 'PRO',
    },
  ];

  const currentPlan = plans.find((plan) => plan.role === user?.role) || plans[0];

  return (
    <Container>
      <Content>
        <Title>Upgrade Your Plan</Title>
        <Subtitle>
          Você está tentando acessar uma funcionalidade que não está disponível no seu plano atual.
          {user?.role && ` Seu plano atual é ${currentPlan.title}.`}
        </Subtitle>
        <PlanGrid>
          {plans.map((plan, index) => (
            <PlanCard key={index} highlighted={plan.highlighted}>
              <PlanTitle>{plan.title}</PlanTitle>
              <PlanPrice>{plan.price}</PlanPrice>
              <FeatureList>
                {plan.features.map((feature, idx) => (
                  <FeatureItem key={idx}>
                    <Check size={18} color={plan.highlighted ? '#dbeafe' : '#2563eb'} />
                    <FeatureText>{feature}</FeatureText>
                  </FeatureItem>
                ))}
              </FeatureList>
              <ActionButton
                highlighted={plan.highlighted}
                onClick={() => navigate('/pricing')}
              >
                {user?.role === plan.role ? 'Seu Plano Atual' : 'Escolher Plano'}
              </ActionButton>
            </PlanCard>
          ))}
        </PlanGrid>
      </Content>
    </Container>
  );
}

export default UpgradePlan;