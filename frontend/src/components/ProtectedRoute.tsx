import { Navigate } from "react-router-dom";

interface Props {
    children: JSX.Element;
}

function ProtectedRoute({ children }: Props) {
    const token = localStorage.getItem("access_token");

    if (!token) {
        return <Navigate to="/login" replace />;
    }

    return children;
}

export default ProtectedRoute;