import React, { Suspense } from "react";
import { useRoutes } from "react-router-dom";
import ThemeRoutes from "../dashboard/routes/Router";
import "../../assets/scss/style.scss";
import Loader from '../UI/Dashboard/loader/Loader'; // Assuming you have a Loader component

function Dashboard() {
  const routing = useRoutes(ThemeRoutes);

  return (
    <div className="dark">
      <Suspense fallback={<Loader />}>
        {routing}
      </Suspense>
    </div>
  );
}

export default Dashboard;