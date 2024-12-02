function sendDataToAPI() {
    // Récupérer les valeurs des champs input
    const title = document.getElementById('title')?.value || "";
    const description = document.getElementById('description')?.value || "";
    const name_company = document.getElementById('name_company')?.value || "";

    // Vérifier si tous les champs sont remplis
    if (!title.trim() || !description.trim() || !name_company.trim()) {
        alert("Veuillez remplir tous les champs.");
        return;
    }

    // Stocker les données dans le localStorage
    try {
        localStorage.setItem('title', title);
        localStorage.setItem('description', description);
        localStorage.setItem('name_company', name_company);
    } catch (error) {
        console.error("Erreur lors de l'enregistrement dans le localStorage :", error);
        alert("Une erreur est survenue lors de l'enregistrement des données. Veuillez réessayer.");
        return;
    }

    // Redirection après succès
    try {
        window.location.href = "http://127.0.0.1:8000/next";
    } catch (error) {
        console.error("Erreur lors de la redirection :", error);
        alert("Une erreur est survenue lors de la redirection. Veuillez vérifier l'URL.");
    }
}
