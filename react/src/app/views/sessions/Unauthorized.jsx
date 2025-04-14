// src/app/views/sessions/Unauthorized.jsx
import { useNavigate } from "react-router-dom";
import { 
  Button, 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from "@mui/material";
import styled from "@mui/material/styles/styled";
import { Check as CheckIcon } from "lucide-react";
import useAuth from "app/hooks/useAuth";

const FlexBox = styled(Box)({
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  flexDirection: "column",
  minHeight: "100vh",
  padding: "24px"
});

const PlanCard = styled(Card)(({ theme, featured }) => ({
  height: "100%",
  display: "flex",
  flexDirection: "column",
  ...(featured && {
    border: `2px solid ${theme.palette.primary.main}`,
    boxShadow: theme.shadows[10]
  })
}));

export default function Unauthorized() {
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const plans = [
    {
      title: "Free",
      price: "R$0",
      features: [
        "Dashboard básico",
        "Long & Short",
        "Opções",
        "Machine Learning"
      ],
      role: "FREE"
    },
    {
      title: "Basic",
      price: "R$29,90/mês",
      features: [
        "Todos os recursos Free",
        "Portfólio",
        "Fundamentos"
      ],
      role: "BASIC",
      featured: true
    },
    {
      title: "Pro",
      price: "R$59,90/mês",
      features: [
        "Todos os recursos Basic",
        "Recomendações",
        "Screener"
      ],
      role: "PRO"
    },
  ];

  const currentPlan = plans.find(plan => plan.role === user?.role) || plans[0];
  
  return (
    <FlexBox>
      <Box sx={{ maxWidth: 900, width: "100%", textAlign: "center", mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Acesso Não Autorizado
        </Typography>
        
        <Typography variant="body1" color="text.secondary" paragraph>
          Você está tentando acessar uma funcionalidade que não está disponível no seu plano atual.
          {user?.role && ` Seu plano atual é ${currentPlan.title}.`}
        </Typography>
        
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate("/zboard/dashboard")}
          sx={{ mb: 4 }}
        >
          Voltar ao Dashboard
        </Button>
        
        <Typography variant="h5" gutterBottom>
          Conheça nossos planos e obtenha acesso a mais recursos:
        </Typography>
      </Box>
      
      <Grid container spacing={3} sx={{ maxWidth: 1200 }}>
        {plans.map((plan, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <PlanCard featured={plan.featured}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h5" component="h2" gutterBottom>
                  {plan.title}
                </Typography>
                <Typography variant="h4" color="primary" gutterBottom>
                  {plan.price}
                </Typography>
                <List dense>
                  {plan.features.map((feature, idx) => (
                    <ListItem key={idx} disableGutters>
                      <ListItemIcon sx={{ minWidth: 30 }}>
                        <CheckIcon size={18} color="primary" />
                      </ListItemIcon>
                      <ListItemText primary={feature} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
              <Box p={2} pt={0}>
                <Button 
                  fullWidth 
                  variant={plan.featured ? "contained" : "outlined"}
                  color="primary"
                  onClick={() => navigate("/pricing")}
                >
                  {user?.role === plan.role ? "Seu Plano Atual" : "Escolher Plano"}
                </Button>
              </Box>
            </PlanCard>
          </Grid>
        ))}
      </Grid>
    </FlexBox>
  );
}