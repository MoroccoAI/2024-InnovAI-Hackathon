import { lazy } from "react";
import { Navigate } from "react-router-dom";
import FormProvider from "../../form/FromProvider.jsx";
import Data from "../Data.js";

/****Layouts*****/
const FullLayout = lazy(() => import("../../UI/Dashboard/FullLayout.js"));

/***** Pages ****/

const Starter = lazy(() => import("../../UI/Dashboard/Starter.js"));
const Alerts = lazy(() => import("../../UI/Dashboard/ui/Alerts.js"));
const Tables = lazy(() => import("../../UI/Dashboard/ui/Tables"));

/*****Routes******/

const ThemeRoutes = [
  {
    path: "/",
    element: <FullLayout />,
    children: [
      { path: "/", element: <Navigate to="starter" /> },
      { path: "starter", exact: true, element: <Starter /> },
      { path: "alerts", exact: true, element: <Alerts /> },
      { path: "table", exact: true, element: <Tables /> },
      { path: "add-house", exact: true, element: <FormProvider /> },
      { path: "data", exact: true, element: <Data /> },
      
      
    ],
  },
];

export default ThemeRoutes;
