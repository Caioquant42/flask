// machinelearning-routes.jsx
import { lazy } from "react";
import Loadable from "app/components/Loadable";

const FrequencyPage = Loadable(lazy(() => import("./FrequencyPage")));

const mlRoutes = [
  { path: "/ml/frequency", element: <FrequencyPage /> },
];

export default mlRoutes;