import { lazy } from "react";
import Loadable from "app/components/Loadable";

const CollarPage = Loadable(lazy(() => import("./CollarPage")));
const OTMCollarPage = Loadable(lazy(() => import("./OTMCollarPage")));
const InvertedCollarPage = Loadable(lazy(() => import("./InvertedCollarPage")));
const InvertedOTMCollarPage = Loadable(lazy(() => import("./InvertedOTMCollarPage")));
const CoveredCallPage = Loadable(lazy(() => import("./CoveredCallPage")));

const opcoesRoutes = [
  { path: "/opcoes/riscozero", element: <CollarPage /> },
  { path: "/opcoes/riscozero/otm", element: <OTMCollarPage /> },
  { path: "/opcoes/riscozero/inverted", element: <InvertedCollarPage /> },
  { path: "/opcoes/riscozero/otm/inverted", element: <InvertedOTMCollarPage /> },
  { path: "/opcoes/financiamento/calls", element: <CoveredCallPage /> },
];

export default opcoesRoutes;