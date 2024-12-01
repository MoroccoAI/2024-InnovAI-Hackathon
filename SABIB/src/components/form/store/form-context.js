import React from "react";

const FormContext = React.createContext({
    formData: {},
    page: 0,
    numOfPages: 0,
    finalData: [],
    validation: {},
    setCurrentPage() {},
    setFormData() {},
    resetDataState() {},
    setFinalData() {},
    setValidation() {},
    validate() {}
});

export default FormContext;