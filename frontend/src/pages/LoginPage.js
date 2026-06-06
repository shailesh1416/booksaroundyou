import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/api';
import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
  const navigate = useNavigate();
  const { user, setUser } = useAuth();
  const [error, setError] = useState(null);

  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  useEffect(() => {
    const clientId = process.env.REACT_APP_GOOGLE_CLIENT_ID;
    if (!clientId) {
      setError('Add REACT_APP_GOOGLE_CLIENT_ID to frontend/.env');
      return;
    }

    const handleCredentialResponse = async (response) => {
      try {
        const result = await authService.login(response.credential);
        setUser(result.data.user);
        navigate('/dashboard');
      } catch (err) {
        setError('Login failed. Please try again.');
      }
    };

    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = () => {
      if (window.google) {
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: handleCredentialResponse,
        });
        window.google.accounts.id.renderButton(
          document.getElementById('google-signin-button'),
          { theme: 'outline', size: 'large', width: '100%' }
        );
      }
    };
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, [navigate, setUser]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-8">BookAroundMe</h1>
        <div className="space-y-4">
          <p className="text-gray-600 text-center">
            Login with Google to access your books and local center dashboard.
          </p>
          {error && (
            <div className="text-sm text-red-600 bg-red-100 p-3 rounded">
              {error}
            </div>
          )}
          <div id="google-signin-button" className="w-full" />
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
