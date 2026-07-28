import api from "./api";

const getAuthHeader = () => {
    const token = localStorage.getItem("access_token");

    return {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    };
};

export const getCurrentUser = async () => {
    const response = await api.get(
        "/users/me",
        getAuthHeader()
    );

    return response.data;
};

export const getUsers = async () => {
    const response = await api.get(
        "/users",
        getAuthHeader()
    );

    return response.data;
};

export const getUser = async (userId: string) => {
    const response = await api.get(
        `/users/${userId}`,
        getAuthHeader()
    );

    return response.data;
};

export const createUser = async (data: {
    username: string;
    email: string;
    primary_organization_id: string;
}) => {
    const response = await api.post(
        "/users",
        data,
        getAuthHeader()
    );

    return response.data;
};

export const updateUser = async (
    userId: string,
    data: {
        username?: string;
        email?: string;
    }
) => {
    const response = await api.put(
        `/users/${userId}`,
        data,
        getAuthHeader()
    );

    return response.data;
};

export const enableUser = async (userId: string) => {
    const response = await api.put(
        `/users/${userId}/enable`,
        {},
        getAuthHeader()
    );

    return response.data;
};

export const disableUser = async (userId: string) => {
    const response = await api.put(
        `/users/${userId}/disable`,
        {},
        getAuthHeader()
    );

    return response.data;
};

export const deleteUser = async (userId: string) => {
    const response = await api.delete(
        `/users/${userId}`,
        getAuthHeader()
    );

    return response.data;
};