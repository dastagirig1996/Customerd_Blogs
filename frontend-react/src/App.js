import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import CustomerAdd from './components/customer/CustomerAdd';
import CustomerDelete from './components/customer/CustomerDelete';
import CustomerEdit from './components/customer/CustomerEdit';
import CustomerList from './components/customer/CustomerList';
import Login from './components/login/Login';
import { axiosInstance } from './utils/axiosConfig';
 
 
const App = () => {
 
  const isAuthenticated = localStorage.getItem('token') !== null;
 
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/add-customer" element={isAuthenticated ? <CustomerAdd /> : <Navigate to="/login" />} />
        <Route path="/customers" element={isAuthenticated ? <CustomerList /> : <Navigate to="/login" />} />
        <Route path="/customers/:id" element={isAuthenticated ? <CustomerList /> : <Navigate to="/login" />} />
        <Route path="/edit-customer/:id" element={isAuthenticated ? <CustomerEdit /> : <Navigate to="/login" />} />
        <Route path="/delete-customer/:id" element={isAuthenticated ? <CustomerDelete /> : <Navigate to="/login" />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
};
export default App;