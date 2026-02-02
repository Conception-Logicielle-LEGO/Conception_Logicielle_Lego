import axios from "axios";

const apiUrl = import.meta.env.VITE_API_URL;
console.debug(`API URL : ${apiUrl}`);
export default axios.create({
  baseURL: apiUrl ?? "http://localhost:8000",
});