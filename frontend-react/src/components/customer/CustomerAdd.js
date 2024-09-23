import React, { useState } from 'react';
import axiosInstance from '../../utils/axiosConfig';
import './Customer.css';
import LogoutButton from '../logout/Logout';
 
const CustomerAdd = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [dob, setDob] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
 
  const validateCustomerData = () => {
    const nameRegex = /^[a-zA-Z]+$/;
    const phoneRegex = /^[0-9]{6,15}$/;
 
    if (!nameRegex.test(firstName)) return 'First name can only contain letters.';
    if (!nameRegex.test(lastName)) return 'Last name can only contain letters.';
    if (!phoneRegex.test(phone)) return 'Phone number contain only numbers';
    if (!dob) return 'Date of birth is required.';
    return null;
  };
 
  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationError = validateCustomerData();
    if (validationError) {
      setError(validationError);
      return;
    }
 
    const token = localStorage.getItem('access_token');
   
   
    try {
      await axiosInstance.post(
        'http://34.47.142.65:8500/customers/customer/',
        { first_name: firstName, last_name: lastName, date_of_birth: dob, phone_number: phone },
        { headers: { Authorization: `Token ${token}` } }
      );
      setSuccess('Customer data saved successfully!');
      setError('');
      setFirstName('');
      setLastName('');
      setDob('');
      setPhone('');
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.error || 'Failed to save customer data.');
      } else {
        setError('Failed to save customer data.');
      }
    }
  };
 
  return (
    <div className="customer-container">
      <h2>Add Customer</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>First Name:</label>
          <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Last Name:</label>
          <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Date of Birth:</label>
          <input type="date" value={dob} onChange={(e) => setDob(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Phone Number:</label>
          <input type="text" value={phone} onChange={(e) => setPhone(e.target.value)} required />
        </div>
        <button type="submit">Add Customer</button>
      </form>
      {success && <p className="success">{success}</p>}
      {error && <p className="error">{error}</p>}
      <LogoutButton />
    </div>
  );
};
 
export default CustomerAdd;