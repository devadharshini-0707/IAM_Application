import api from "./api";

export const getUsers = async () => {
    const token = localStorage.getItem("access_token");

    const response = await api.get("/users", {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    return response.data;
};