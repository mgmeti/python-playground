import axios from "axios";

const API_URL = "http://localhost:8000";

export const extractJobInfo = async (formData) => {
  return axios.post(`${API_URL}/extract`, formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
};
