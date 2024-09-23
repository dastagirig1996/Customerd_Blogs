import React, { useState } from 'react';
import axiosInstance from '../../utils/axiosConfig';
import { useNavigate } from 'react-router-dom';
import './Login.css';
 
const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
 
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axiosInstance.post('http://backend:8000/customers/login/', {
        username,
        password,
      });
      const { access_token, refresh_token } = response.data;
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);
      navigate('/add-customer');
    } catch (err) {
      setError('Invalid username or password.');
    }
  };
 
  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
};
 
export default Login;