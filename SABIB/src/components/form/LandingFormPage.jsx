import React, { useContext } from "react";
import classes from "./css/LandingFormPage.module.css";
import TypeOfLocation from "./TypeOfLocation";
import CongratzPage from "./CongratzPage";
import FormContext from "./store/form-context";
import './css/global.css';
import UsagePage from "./UsagePage";
import NicknamePage from "./NicknamePage";
import LocationAddressPage from "./LocationAddressPage";
import LocationSizePage from "./LocationSizePage";
import FloorsAndBathroomsPage from "./FloorsAndBathroomsPage";
import ApplianceAndAmenitiesPage from "./ApplianceAndAmenitiesPage";
import PeopleCountPage from "./PeopleCountPage";

function LandingFormPage() {
  const { page, numOfPages } = useContext(FormContext);

  return (
    <div >
    <div className={classes.form}>
      
      <div className="card-form">
        {page === 1 && <TypeOfLocation />}
        {page === 2 && <UsagePage />}
        {page === 3 && <NicknamePage />}
        {page === 4 && <LocationAddressPage />}
        {page === 5 && <LocationSizePage />}
        {page === 6 && <FloorsAndBathroomsPage />}
        {page === 7 && <ApplianceAndAmenitiesPage />}
        {page === 8 && <PeopleCountPage />}
        {page === 9 && <CongratzPage />}
      </div>
    </div>
    </div>

  );
}

export default LandingFormPage;
