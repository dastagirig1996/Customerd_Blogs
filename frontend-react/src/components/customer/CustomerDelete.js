import React, { useState, useEffect } from 'react';
import axiosInstance from '../../utils/axiosConfig';
import { useParams, useNavigate } from 'react-router-dom';
import './Customer.css';
import LogoutButton from '../logout/Logout';
 
const CustomerDelete = () => {
  const { id } = useParams();
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [customerExists, setCustomerExists] = useState(true);
  const navigate = useNavigate();
  const token = localStorage.getItem('access_token');
 
  const checkCustomerExists = async () => {
    try {
      const response = await axiosInstance.get(`http://34.47.142.65:8500/customers/customer/${id}/`, {
        headers: { Authorization: `Token ${token}` },
      });
      if (!response.data) {
        setCustomerExists(false);
        setError('Customer ID does not exist.');
      }
    } catch (err) {
      if (err.response && err.response.status === 404) {
        setCustomerExists(false);
        setError('Customer ID does not exist.');
      }
       else {
        setError('Failed to check customer existence.');
      }
     
    }
  };
 
 
  const handleDelete = async () => {
    if (!customerExists) {
      setError('Customer ID does not exist.');
      return;
    }
 
    try {
      await axiosInstance.delete(`http://35.200.248.136:9500/customers/customer/${id}/`, {
        headers: { Authorization: `Token ${token}` },
      });
      setSuccess('Customer deleted successfully!');
      setError('');
      navigate('/customers')
    } catch (err) {
      setError('Failed to delete customer.');
      setSuccess('');
    }
  };
 
 
  useEffect(() => {
    if (id) {
      checkCustomerExists();
    }
  }, [id]);
 
  return (
    <div className="customer-container">
      <h2>Delete Customer</h2>
 
     
      {!customerExists && <p className="error">Customer ID does not exist.</p>}
      {customerExists && (
        <>
          <p>Are you sure you want to delete this customer?</p>
          <button onClick={handleDelete} className="delete-btn">Confirm Delete</button>
        </>
      )}
 
      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}
 
      <LogoutButton />
    </div>
  );
};
 
export default CustomerDelete;