import React, { useState, useEffect } from 'react';
import { supabase } from './supabaseClient';
import './App.css';

function App() {
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [organization, setOrganization] = useState('');
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [subscribers, setSubscribers] = useState([]);
  const [showSubscribers, setShowSubscribers] = useState(false);

  // Fetch subscribers for admin view
  const fetchSubscribers = async () => {
    const { data, error } = await supabase
      .from('mailing_list')
      .select('*')
      .order('created_at', { ascending: false });
    
    if (error) {
      console.error('Error fetching subscribers:', error);
    } else {
      setSubscribers(data);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const { data, error } = await supabase
        .from('mailing_list')
        .insert([
          {
            email,
            first_name: firstName,
            last_name: lastName,
            organization: organization || null,
            title: title || null
          }
        ]);

      if (error) {
        if (error.code === '23505') {
          setMessage('This email is already subscribed to our mailing list.');
        } else {
          setMessage('Error: ' + error.message);
        }
      } else {
        setMessage('Successfully subscribed! You will receive monthly CSRR faculty media reports.');
        setEmail('');
        setFirstName('');
        setLastName('');
        setOrganization('');
        setTitle('');
      }
    } catch (error) {
      setMessage('Error: ' + error.message);
    }

    setLoading(false);
  };

  // Export to CSV function
  const exportToCSV = () => {
    const csvContent = [
      ['Email', 'First Name', 'Last Name', 'Organization', 'Title', 'Subscribed Date'],
      ...subscribers.map(sub => [
        sub.email,
        sub.first_name,
        sub.last_name,
        sub.organization || '',
        sub.title || '',
        new Date(sub.created_at).toLocaleDateString()
      ])
    ].map(row => row.map(field => `"${field}"`).join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `csrr_mailing_list_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="App">
      <header className="header">
        <h1>CSRR Faculty Media Reports</h1>
        <p>Center for Security, Race and Rights - Rutgers Law School</p>
      </header>

      <main className="main-content">
        <section className="signup-section">
          <h2>Subscribe to Monthly Media Reports</h2>
          <p>Receive comprehensive reports of CSRR faculty media mentions, op-eds, and interviews.</p>
          
          <form onSubmit={handleSubmit} className="signup-form">
            <div className="form-row">
              <input
                type="text"
                placeholder="First Name *"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
                className="form-input"
              />
              <input
                type="text"
                placeholder="Last Name *"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
                className="form-input"
              />
            </div>
            
            <input
              type="email"
              placeholder="Email Address *"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="form-input full-width"
            />
            
            <div className="form-row">
              <input
                type="text"
                placeholder="Organization (optional)"
                value={organization}
                onChange={(e) => setOrganization(e.target.value)}
                className="form-input"
              />
              <input
                type="text"
                placeholder="Title (optional)"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="form-input"
              />
            </div>
            
            <button 
              type="submit" 
              disabled={loading}
              className="submit-button"
            >
              {loading ? 'Subscribing...' : 'Subscribe to Reports'}
            </button>
          </form>
          
          {message && (
            <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
              {message}
            </div>
          )}
        </section>

        <section className="info-section">
          <h3>About Our Reports</h3>
          <ul>
            <li>Monthly compilation of faculty media appearances</li>
            <li>Coverage from major outlets: CNN, New York Times, Washington Post, BBC, NPR, and more</li>
            <li>Op-eds, interviews, articles, podcasts, and TV appearances</li>
            <li>Delivered directly to your inbox</li>
          </ul>
        </section>

        {/* Admin section - hidden by default */}
        <section className="admin-section">
          <button 
            onClick={() => {
              setShowSubscribers(!showSubscribers);
              if (!showSubscribers) fetchSubscribers();
            }}
            className="admin-button"
          >
            {showSubscribers ? 'Hide' : 'Show'} Subscriber List (Admin)
          </button>
          
          {showSubscribers && (
            <div className="subscribers-list">
              <div className="subscribers-header">
                <h3>Subscribers ({subscribers.length})</h3>
                <button onClick={exportToCSV} className="export-button">
                  Export to CSV
                </button>
              </div>
              
              <div className="subscribers-table">
                <table>
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Organization</th>
                      <th>Title</th>
                      <th>Subscribed</th>
                    </tr>
                  </thead>
                  <tbody>
                    {subscribers.map((subscriber, index) => (
                      <tr key={index}>
                        <td>{subscriber.first_name} {subscriber.last_name}</td>
                        <td>{subscriber.email}</td>
                        <td>{subscriber.organization || '-'}</td>
                        <td>{subscriber.title || '-'}</td>
                        <td>{new Date(subscriber.created_at).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <p>&copy; 2025 Center for Security, Race and Rights - Rutgers Law School</p>
      </footer>
    </div>
  );
}

export default App;
