// import axios from "axios";

// const fetchData = async () => {
//   try {
//     const token = localStorage.getItem("access_token"); // Assurez-vous que vous stockez le token dans localStorage
//     const response = await axios.get(
//       "http://127.0.0.1:8000/api/protected-endpoint/",
//       {
//         headers: {
//           Authorization: `Bearer ${token}`, // Ajouter le token dans l'en-tête
//         },
//       }
//     );
//     return response.data;
//   } catch (err) {
//     console.error("Error fetching data:", err);
//     throw err; // Vous pouvez choisir de lancer l'erreur ou de la gérer autrement.
//   }
// };

// export default fetchData;
