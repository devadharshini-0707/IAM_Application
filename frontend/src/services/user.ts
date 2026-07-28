import api from "./api";

export interface CreateUserRequest {
    username: string;
    email: string;
    primary_organization_id: string;
}

export interface UpdateUserRequest {
    username?: string;
    email?: string;
}

export interface PaginatedUsersResponse {
    items: any[];
    total: number;
    page: number;
    page_size: number;
    total_pages: number;
}

export const getCurrentUser = async () => {
    const response = await api.get("/users/me");
    return response.data;
};

export const getUsers = async (
    page = 1,
    pageSize = 10,
    search = ""
): Promise<PaginatedUsersResponse> => {
    const response = await api.get("/users", {
        params: {
            page,
            page_size: pageSize,
            search: search || undefined,
        },
    });

    return response.data;
};

export const createUser = async (
    request: CreateUserRequest
) => {
    const response = await api.post("/users", request);
    return response.data;
};

export const updateUser = async (
    userId: string,
    request: UpdateUserRequest
) => {
    const response = await api.put(
        `/users/${userId}`,
        request
    );

    return response.data;
};

export const enableUser = async (
    userId: string
) => {
    const response = await api.put(
        `/users/${userId}/enable`
    );

    return response.data;
};

export const disableUser = async (
    userId: string
) => {
    const response = await api.put(
        `/users/${userId}/disable`
    );

    return response.data;
};

export const deleteUser = async (
    userId: string
) => {
    const response = await api.delete(
        `/users/${userId}`
    );

    return response.data;
};