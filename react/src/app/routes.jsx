// src/app/routes.jsx
import { lazy } from "react";
import { Navigate } from "react-router-dom";

import AuthGuard from "./auth/AuthGuard";
import RoleBasedGuard from "./auth/RoleBasedGuard";
import { authRoles } from "./auth/authRoles";

import Loadable from "./components/Loadable";
import MatxLayout from "./components/MatxLayout/MatxLayout";
import sessionRoutes from "./views/sessions/session-routes";
import recomendationsRoutes from "app/views/recomendations/recommendations-routes";
import screenerRoutes from "app/views/screener/screener-routes";
import zboardRoutes from "app/views/zboard/zboard-routes";
import volatilidadeRoutes from "app/views/volatilidade/volatilidade-routes";
import rrgRoutes from "app/views/rrg/rrg-routes";
import survivalRoutes from "app/views/survival/survival-routes";
import portfolioRoutes from "app/views/portfolio/portfolio-routes";
import fundamentosRoutes from "app/views/fundamentos/fundamentos-routes";
import longshortRoutes from "app/views/longshort/longshort-routes";
import opcoesRoutes from "app/views/opcoes/opcoes-routes";
import mlRoutes from "app/views/machinelearning/machinelearning-routes";
import mcRoutes from "app/views/mc/mc-routes";

// Lazy-load the PricingPage component
const PricingPage = Loadable(lazy(() => import("./components/PricingPage")));
const UpgradePlan = Loadable(lazy(() => import("./views/sessions/UpgradePlan")));
const Unauthorized = Loadable(lazy(() => import("./views/sessions/Unauthorized")));

// Aplicar roles às rotas
const applyRolesToRoutes = (routes, roles) => {
  return routes.map(route => ({
    ...route,
    element: (
      <RoleBasedGuard allowedRoles={roles}>
        {route.element}
      </RoleBasedGuard>
    )
  }));
};

const routes = [
  { path: "/", element: <Navigate to="zboard/dashboard" /> },
  {
    element: (
      <AuthGuard>
        <MatxLayout />
      </AuthGuard>
    ),
    children: [
      // Rotas básicas acessíveis para todos os usuários autenticados
      ...zboardRoutes,

      // Rotas para usuários free ou superiores
      ...applyRolesToRoutes([
        ...recomendationsRoutes,
        ...longshortRoutes,
        ...opcoesRoutes,
        ...mlRoutes,
        ...portfolioRoutes,
        ...rrgRoutes,
        ...fundamentosRoutes,
        ...screenerRoutes,
        ...volatilidadeRoutes,
        ...mcRoutes,
      ], authRoles.free),

      // Rotas para usuários básicos ou superiores
      ...applyRolesToRoutes([
        ...portfolioRoutes,
        ...rrgRoutes,
        ...fundamentosRoutes,
      ], authRoles.basic),
      
      // Rotas para usuários pro ou superiores
      ...applyRolesToRoutes([
        ...screenerRoutes,
      ], authRoles.pro),
      
      // Rotas para usuários admin ou superiores
      ...applyRolesToRoutes([
        ...volatilidadeRoutes,
        ...survivalRoutes,
      ], authRoles.admin),
      
    ]
  },
  // Add the pricing route (acessível para todos, mesmo não autenticados)
  { path: "/pricing", element: <PricingPage /> },
  { path: "/session/upgradeplan", element: <UpgradePlan /> },
  
  // Página de acesso não autorizado
  { path: "/session/unauthorized", element: <Unauthorized /> },

  
  // session pages route
  ...sessionRoutes
];

export default routes;