import React, { useState, useEffect } from 'react';
import axiosInstance from '../../utils/axiosConfig';
import { Navigate, useParams } from 'react-router-dom';
import './Customer.css';
import LogoutButton from '../logout/Logout';
 
const CustomerEdit = () => {
  const { id } = useParams();
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [dob, setDob] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
 
  const token = localStorage.getItem('access_token');
 
  useEffect(() => {
    const fetchCustomer = async () => {
      try {
        const response = await axiosInstance.get(`http://34.47.142.65:8500//customers/customer/${id}/`, {
          headers: { Authorization: `Token ${token}` },
        });
        setFirstName(response.data.first_name);
        setLastName(response.data.last_name);
        setDob(response.data.date_of_birth);
        setPhone(response.data.phone_number);
      } catch (err) {
        // Handle customer not found (404) error
        if (err.response && err.response.status === 404) {
          setError('Customer ID does not exist.');
        } else {
          setError('Failed to fetch customer data.');
        }
      }
    };
    fetchCustomer();
  }, [id, token]);
 
  const handleUpdate = async (e) => {
    e.preventDefault();
    const updatedCustomer = { first_name: firstName, last_name: lastName, date_of_birth: dob, phone_number: phone };
 
    try {
      await axiosInstance.put(`http://35.200.248.136:9500/customers/customer/${id}/`, updatedCustomer, {
        headers: { Authorization: `Token ${token}` },
      });
      setSuccess('Customer updated successfully!');
      setError('');
      setFirstName('');
      setLastName('');
      setDob('');
      setPhone('');
    } catch (err) {
      if (err.response && err.response.status === 404) {
        setError('Customer ID does not exist.');
      } else {
       
        setError('Failed to update customer.');
      }
      setSuccess('');
    }
  };
 
  return (
    <div className="customer-container">
      <h2>Edit Customer</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleUpdate}>
        <div className="form-group">
          <label>First Name:</label>
          <input
            type="text"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Last Name:</label>
          <input
            type="text"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Date of Birth:</label>
          <input
            type="date"
            value={dob}
            onChange={(e) => setDob(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Phone Number:</label>
          <input
            type="text"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
          />
        </div>
        <button type="submit">Update Customer</button>
      </form>
      {success && <p className="success">{success}</p>}
      <LogoutButton />
    </div>
  );
};
 
export default CustomerEdit;