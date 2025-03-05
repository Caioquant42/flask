import { lazy } from "react";
import Loadable from "app/components/Loadable";

const CollarPage = Loadable(lazy(() => import("./CollarPage")));

const opcoesRoutes = [
  { path: "/opcoes/riscozero", element: <CollarPage /> },
];

export default opcoesRoutes;