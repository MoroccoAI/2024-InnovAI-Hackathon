// FormProvider.js

import React, { useState } from "react";
import FormContext from "./form-context";

function FormProvider({ children }) {
  // Define default data and validation states for each page
  const defaultDataState = {
    usage: "", // Add the "usage" field here
    nickname: "",
    address: "",
    city: "",
    region: "",
    postalCode: "",
    size: "",
    floors: "",
    bathrooms: "",
    appliances: [],
    amenities: [],
    peopleCount: 0,
  };

  const defaultValidationState = {
    usage: false, // Add the "usage" field here
    nickname: false,
    address: false,
    city: false,
    region: false,
    postalCode: false,
    size: false,
    floors: false,
    bathrooms: false,
    appliances: false,
    amenities: false,
    peopleCount: false,
  };

  const [page, setPage] = useState(1);
  const [finalData, setFinalData] = useState([]);
  const [formData, setFormData] = useState(defaultDataState);
  const [validation, setValidation] = useState(defaultValidationState);

  const validate = (a) => Object.values(a).reduce((sum, next) => sum && next, true);

  const resetDataState = () => {
    setFormData(defaultDataState);
    setValidation(defaultValidationState);
  };

  const setCurrentPage = (val) => {
    setPage(val);
  };

  const initialValue = {
    formData,
    page,
    numOfPages: 9,
    finalData,
    validation,
    setCurrentPage,
    setFormData,
    resetDataState,
    setFinalData,
    setValidation,
    validate,
  };

  return <FormContext.Provider value={initialValue}>{children}</FormContext.Provider>;
}

export default FormProvider;
