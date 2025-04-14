// src/app/auth/RoleBasedGuard.jsx
import { Navigate, useLocation } from "react-router-dom";
// HOOK
import useAuth from "app/hooks/useAuth";

export default function RoleBasedGuard({ children, allowedRoles }) {
  const { isAuthenticated, user } = useAuth();
  const { pathname } = useLocation();

  // Verificar se o usuário está autenticado
  if (!isAuthenticated) {
    return <Navigate replace to="/session/signin" state={{ from: pathname }} />;
  }

  // Verificar se o usuário tem a role permitida
  // allowedRoles é um array como authRoles.pro que contém ["SA", "ADMIN", "PRO"]
  const userHasRequiredRole = user && user.role && allowedRoles.includes(user.role);

  if (!userHasRequiredRole) {
    // Redirecionar para uma página de acesso negado ou dashboard limitado
    return <Navigate replace to="/session/upgradeplan" />;
  }

  // Se o usuário tem permissão, renderizar os componentes filhos
  return <>{children}</>;
}