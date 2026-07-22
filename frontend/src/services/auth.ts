import api from "./api";

export interface LoginRequest {
    email: string;
    password: string;
}

export interface SignupRequest {
    organization_name: string;
    organization_slug: string;
    organization_tier: string;
    display_name: string;
    username: string;
    email: string;
    password: string;
}

export const login = async (request: LoginRequest) => {
    const response = await api.post("/auth/login", request);
    return response.data;
};

export const signup = async (request: SignupRequest) => {
    const response = await api.post("/auth/signup", request);
    return response.data;
};