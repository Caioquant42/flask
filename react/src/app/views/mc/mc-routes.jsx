// mc-routes.jsx
import { lazy } from "react";
import Loadable from "app/components/Loadable";

const MCplotPage = Loadable(lazy(() => import("./MCplotPage")));

const mcRoutes = [
  { path: "/mc/bootstrap", element: <MCplotPage /> },
];

export default mcRoutes;