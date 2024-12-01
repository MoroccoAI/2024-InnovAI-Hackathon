import React from 'react'
import FormProvider from "../form/store/FormProvider";
import LogoHeader from "../../components/form/LogoHeader";
import LandingFormPage from "../../components/form/LandingFormPage";
import PaginateBar from "./PaginateBar";

function FromProvider() {
  return (
<div style={{ minWidth: '100px', maxHeight: 'calc(100vh - 100px)' }}>
<FormProvider style={{ width: '100%', height: '100%' }}>
     <div className="app">
       <LogoHeader />
       <PaginateBar />
       <LandingFormPage />
     </div>
    </FormProvider>
</div>);
}

export default FromProvider