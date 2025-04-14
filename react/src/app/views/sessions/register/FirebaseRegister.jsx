// src/app/views/sessions/register/FirebaseRegister.jsx
import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useSnackbar } from "notistack";
import { Formik } from "formik";
import * as Yup from "yup";

import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import Grid from "@mui/material/Grid2";
import Button from "@mui/material/Button";
import Checkbox from "@mui/material/Checkbox";
import TextField from "@mui/material/TextField";
import styled from "@mui/material/styles/styled";
import LoadingButton from "@mui/lab/LoadingButton";
import useTheme from "@mui/material/styles/useTheme";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Radio from "@mui/material/Radio";
import Divider from "@mui/material/Divider";
import Typography from "@mui/material/Typography";

// GLOBAL CUSTOM COMPONENTS
import MatxDivider from "app/components/MatxDivider";
import { Paragraph } from "app/components/Typography";
// GLOBAL CUSTOM HOOKS
import useAuth from "app/hooks/useAuth";

// STYLED COMPONENTS
const ContentBox = styled("div")(({ theme }) => ({
  height: "100%",
  padding: "32px",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  backgroundColor: theme.palette.background.default
}));

const IMG = styled("img")({ width: "100%" });

const GoogleButton = styled(Button)(({ theme }) => ({
  color: "rgba(0, 0, 0, 0.87)",
  backgroundColor: "#e0e0e0",
  boxShadow: theme.shadows[0],
  "&:hover": { backgroundColor: "#d5d5d5" }
}));

const RegisterRoot = styled("div")({
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  background: "#1A2038",
  minHeight: "100vh !important",
  "& .card": { maxWidth: 750, margin: 16, borderRadius: 12 }
});

const PlanBox = styled(Box)(({ theme, selected }) => ({
  padding: "1rem",
  border: `1px solid ${selected ? theme.palette.primary.main : theme.palette.divider}`,
  borderRadius: "8px",
  backgroundColor: selected ? theme.palette.primary.light + '10' : 'transparent',
  cursor: 'pointer',
  transition: 'all 0.3s ease',
  marginBottom: '1rem'
}));

// initial login credentials
const initialValues = {
  email: "",
  password: "",
  remember: true,
  role: "FREE" // Default role
};

// form field validation schema
const validationSchema = Yup.object().shape({
  password: Yup.string()
    .min(6, "A senha deve ter 6 caracteres no mínimo.")
    .required("A senha é obrigatória."),
  email: Yup.string().email("Email inválido").required("Email é obrigatório"),
  role: Yup.string().required("Selecione um plano")
});

export default function FirebaseRegister() {
  const theme = useTheme();
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();
  const [loading, setLoading] = useState(false);
  const { createUserWithEmail, signInWithGoogle } = useAuth();

  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const handleGoogleRegister = async () => {
    try {
      setLoading(true);
      await signInWithGoogle();
      navigate("/");
      enqueueSnackbar("Login realizado com sucesso!", { variant: "success" });
    } catch (e) {
      console.error(e);
      setLoading(false);
      enqueueSnackbar("Erro ao fazer login com Google", { variant: "error" });
    }
  };

  const handleFormSubmit = async (values) => {
    try {
      setLoading(true);
      setEmailError("");
      setPasswordError("");
      
      await createUserWithEmail(values.email, values.password, values.role);
      navigate("/");
      enqueueSnackbar("Cadastro realizado com sucesso!", { variant: "success" });
    } catch (error) {
      setLoading(false);
      console.error("Erro no registro:", error);
      
      if (error.code === "auth/email-already-in-use") {
        setEmailError("Este e-mail já está em uso.");
      } else if (error.code === "auth/invalid-email") {
        setEmailError("Endereço de e-mail inválido.");
      } else if (error.code === "auth/weak-password") {
        setPasswordError("A senha é muito fraca.");
      } else {
        enqueueSnackbar("Ocorreu um erro durante o cadastro: " + error.message, { variant: "error" });
      }
    }
  };

  // Função para renderizar os planos
  const renderPlanOption = (formikProps, value, title, description, price) => {
    const isSelected = formikProps.values.role === value;
    
    return (
      <PlanBox 
        selected={isSelected} 
        onClick={() => formikProps.setFieldValue('role', value)}
        sx={{ border: isSelected ? `2px solid ${theme.palette.primary.main}` : undefined }}
      >
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">{title}</Typography>
          <Typography variant="h6" color="primary">{price}</Typography>
        </Box>
        <Typography variant="body2" color="text.secondary" mt={1}>
          {description}
        </Typography>
      </PlanBox>
    );
  };

  return (
    <RegisterRoot>
      <Card className="card">
        <Grid container>
          <Grid size={{ md: 6, xs: 12 }}>
            <ContentBox>
              <IMG src="/assets/images/illustrations/posting_photo.svg" alt="Photo" />
            </ContentBox>
          </Grid>

          <Grid size={{ md: 6, xs: 12 }}>
            <Box px={4} pt={4}>
              <GoogleButton
                fullWidth
                variant="contained"
                onClick={handleGoogleRegister}
                startIcon={<img src="/assets/images/logos/google.svg" alt="google" />}>
                Entrar com o Google
              </GoogleButton>
            </Box>

            <MatxDivider sx={{ mt: 3, px: 4 }} text="Ou" />

            <Box p={4} height="100%">
              <Formik
                onSubmit={handleFormSubmit}
                initialValues={initialValues}
                validationSchema={validationSchema}>
                {(formikProps) => {
                  const { values, errors, touched, handleChange, handleBlur, handleSubmit } = formikProps;
                  return (
                    <form onSubmit={handleSubmit}>
                      <TextField
                        fullWidth
                        size="small"
                        type="email"
                        name="email"
                        label="Email"
                        variant="outlined"
                        onBlur={handleBlur}
                        value={values.email}
                        onChange={handleChange}
                        helperText={touched.email && errors.email || emailError}
                        error={Boolean((errors.email && touched.email) || emailError)}
                        sx={{ mb: 3 }}
                      />

                      <TextField
                        fullWidth
                        size="small"
                        name="password"
                        type="password"
                        label="Senha"
                        variant="outlined"
                        onBlur={handleBlur}
                        value={values.password}
                        onChange={handleChange}
                        helperText={touched.password && errors.password || passwordError}
                        error={Boolean((errors.password && touched.password) || passwordError)}
                        sx={{ mb: 3 }}
                      />

                      <Typography variant="subtitle1" fontWeight="bold" mb={2}>
                        Escolha seu plano
                      </Typography>
                      
                      {renderPlanOption(
                        formikProps,
                        "FREE",
                        "Plano Gratuito",
                        "Acesso básico às funcionalidades da plataforma",
                        "Grátis"
                      )}
                      
                      {renderPlanOption(
                        formikProps,
                        "BASIC",
                        "Plano Básico",
                        "Acesso a recursos intermediários e suporte básico",
                        "R$ 29,90/mês"
                      )}
                      
                      {renderPlanOption(
                        formikProps,
                        "PRO",
                        "Plano Pro",
                        "Acesso completo a todas as funcionalidades e suporte prioritário",
                        "R$ 79,90/mês"
                      )}
                      
                      {errors.role && touched.role && (
                        <Typography color="error" variant="caption">
                          {errors.role}
                        </Typography>
                      )}

                      <Divider sx={{ my: 3 }} />

                      <Box display="flex" alignItems="center" gap={1}>
                        <Checkbox
                          size="small"
                          name="remember"
                          onChange={handleChange}
                          checked={values.remember}
                          sx={{ padding: 0 }}
                        />

                        <Paragraph fontSize={13}>
                          Eu li e concordo com os termos de serviço.
                        </Paragraph>
                      </Box>

                      <LoadingButton
                        type="submit"
                        color="primary"
                        loading={loading}
                        variant="contained"
                        sx={{ my: 2 }}
                        fullWidth>
                        Cadastre-se
                      </LoadingButton>

                      <Paragraph>
                        Já possui conta?
                        <NavLink
                          to="/session/signin"
                          style={{ color: theme.palette.primary.main, marginLeft: 5 }}>
                          Entrar
                        </NavLink>
                      </Paragraph>
                    </form>
                  );
                }}
              </Formik>
            </Box>
          </Grid>
        </Grid>
      </Card>
    </RegisterRoot>
  );
}