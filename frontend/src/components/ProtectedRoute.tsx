import { Navigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { session, loading } = useAuth();

  if (loading) {
    return (
      <div style={{
        minHeight: "100vh",
        background: "#0a0a0f",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}>
        <style>{`@keyframes pr-spin { to { transform: rotate(360deg); } }`}</style>
        <div style={{
          width: 28, height: 28,
          border: "2px solid rgba(255,255,255,0.08)",
          borderTop: "2px solid #7c3aed",
          borderRadius: "50%",
          animation: "pr-spin 0.7s linear infinite",
        }} />
      </div>
    );
  }

  if (!session) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
